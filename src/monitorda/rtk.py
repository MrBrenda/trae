"""RTK 单位线拟合：定量分离快速入流与慢速入渗。

方法来源：
  EPA RDII Analysis (RTK method)
  SSOAP Toolbox (Sanitary Sewer Overflow Analysis and Planning), 2008
  参考：WEF MOP 60, 德国 ATV-DVWK A-118

三角形单位线三参数：
  R  — 降雨转化比例（m/mm，液位升幅代用流量）
  T  — 峰值时间（小时，降雨开始到响应峰值）
  K  — 退水倍数（退水时间 = K × T）

两分量模型（fast + slow），分别对应：
  快速入流 (R1, T1, K1): T1 ≤ 12h — 直连、混接（雨水直接灌入）
  慢速入渗 (R2, T2, K2): T2 > 12h — 地下水/管壁渗漏

输入数据分辨率：1 小时（level 从 10min 重采样；rainfall 原本 1h）。
"""

from __future__ import annotations

import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
from scipy.optimize import minimize

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# 参数上下界（物理约束）
# ---------------------------------------------------------------------------

_BOUNDS = [
    (0.0, 0.30),   # R1: m/mm，快速分量
    (0.5, 12.0),   # T1: h，快速峰值时间（直连 < 2h；混接 2–12h）
    (1.0, 10.0),   # K1: 退水倍数
    (0.0, 0.30),   # R2: m/mm，慢速分量
    (24.0, 168.0), # T2: h，慢速峰值时间（地下水入渗 ≥ 24h；与 T1 范围不重叠）
    (1.0, 20.0),   # K2: 退水倍数
]

# 最少非 NaN 观测点数才允许参与拟合
_MIN_OBS_PER_EVENT = 12   # 小时
_MIN_EVENTS = 2            # 至少 2 场事件
_MIN_R2 = 0.05             # R² 低于此值视为拟合不可靠，保留参数但加注警告


# ---------------------------------------------------------------------------
# 核心：三角形单位线
# ---------------------------------------------------------------------------

def _triangular_uh(T_h: float, K: float, dt_h: float = 1.0) -> np.ndarray:  # noqa: N803
    """单个分量的三角形单位线，按 dt_h 采样。

    uh 在时间轴上的积分 = 1（dt_h 为时间步长时，∑uh * dt_h = 1）。
    """
    total_h = T_h * (1.0 + K)
    n = max(3, int(np.ceil(total_h / dt_h)) + 2)
    t = np.arange(n, dtype=float) * dt_h
    peak = 2.0 / (T_h * (1.0 + K))   # 单位：1/h

    uh = np.where(
        t < T_h,
        peak * t / T_h,
        np.where(
            t < T_h * (1.0 + K),
            peak * (T_h * (1.0 + K) - t) / (K * T_h),
            0.0,
        ),
    )
    return uh   # 单位：1/h


def _predict_rdii(  # noqa: N803
    rain_mm_h: np.ndarray,
    R1: float, T1: float, K1: float,  # noqa: N803
    R2: float, T2: float, K2: float,  # noqa: N803
    dt_h: float = 1.0,
) -> np.ndarray:
    """两分量 RTK 模型预测液位 RDII（单位：m）。

    Parameters
    ----------
    rain_mm_h : hourly rainfall array, shape (N,), mm/h
    其余参数见模块说明。

    Returns
    -------
    rdii_m : predicted RDII level, shape (N,), m
    """
    n = len(rain_mm_h)
    uh1 = _triangular_uh(T1, K1, dt_h) * dt_h   # 无量纲（已乘 dt）
    uh2 = _triangular_uh(T2, K2, dt_h) * dt_h

    c1 = np.convolve(rain_mm_h, uh1)[:n]
    c2 = np.convolve(rain_mm_h, uh2)[:n]

    return R1 * c1 + R2 * c2


# ---------------------------------------------------------------------------
# 拟合
# ---------------------------------------------------------------------------

@dataclass
class RTKResult:
    node_id: str
    n_events_used: int
    R1: float | None
    T1_h: float | None
    K1: float | None
    R2: float | None
    T2_h: float | None
    K2: float | None
    r2: float | None          # 决定系数
    rmse_m: float | None      # 均方根误差，m
    fast_fraction: float | None   # R1/(R1+R2)，越高越"入流"主导
    category_rtk: str         # fast_inflow / mixed / slow_infiltration / data_insufficient
    fit_notes: str = ""


def _r2(obs: np.ndarray, pred: np.ndarray) -> float:
    ss_res = np.nansum((obs - pred) ** 2)
    ss_tot = np.nansum((obs - np.nanmean(obs)) ** 2)
    if ss_tot == 0:
        return float("nan")
    return float(1.0 - ss_res / ss_tot)


def fit_rtk_node(
    node_id: str,
    level_series: pd.Series,              # DatetimeIndex, 10min, good-only
    rain_series_dict: dict[str, pd.Series],  # station_id → hourly rain
    events_df: pd.DataFrame,
    bwf_df: pd.DataFrame,
    station_id: str | None = None,
    n_starts: int = 8,
    dt_h: float = 1.0,
) -> RTKResult:
    """对单个节点进行 2-分量 RTK 拟合。

    拟合步骤：
    1. 对每个事件窗口，将 10min 液位重采样到 hourly，减去 BWF 得观测 RDII。
    2. 获取同期小时降雨（若节点有指定站，用指定站；否则取所有站最大值）。
    3. 将所有事件拼成一条时间序列（gap 置 NaN），做联合最小二乘拟合。
    4. 多随机起点 L-BFGS-B 优化，取最优。
    """
    no_fit = RTKResult(
        node_id=node_id, n_events_used=0,
        R1=None, T1_h=None, K1=None,
        R2=None, T2_h=None, K2=None,
        r2=None, rmse_m=None,
        fast_fraction=None,
        category_rtk="data_insufficient",
    )

    if level_series.empty:
        return no_fit

    # ── 每场事件构建对齐窗口 ─────────────────────────────────────────────
    rain_avail = list(rain_series_dict.keys())
    if not rain_avail:
        return no_fit

    tail_h = 72  # 事件结束后延伸 72h 以捕获慢速入渗退水
    obs_segs: list[np.ndarray] = []
    rain_segs: list[np.ndarray] = []
    events_used: int = 0

    for _, ev in events_df.iterrows():
        eid = ev["event_id"]
        bwf_row = bwf_df[(bwf_df["node_id"] == node_id) & (bwf_df["event_id"] == eid)]
        if bwf_row.empty:
            continue
        bwf_level = bwf_row.iloc[0]["bwf_level_m"]
        if bwf_level is None or (isinstance(bwf_level, float) and np.isnan(bwf_level)):
            continue

        t0 = pd.Timestamp(ev["t_start"])
        t1 = pd.Timestamp(ev["t_end"]) + pd.Timedelta(hours=tail_h)
        t_range = pd.date_range(t0, t1, freq="h")

        # 液位：10min → hourly 重采样
        win_lv = level_series.loc[t0 - pd.Timedelta(hours=1): t1]
        if win_lv.empty:
            continue
        level_h = (
            win_lv.resample("h").mean()
            .reindex(t_range)
            .interpolate(method="time", limit=3)
        )
        obs_rdii = (level_h - bwf_level).clip(lower=0.0).to_numpy()

        # 降雨：选站（指定优先；否则取最大值合并）
        sids = [station_id] if station_id and station_id in rain_series_dict else rain_avail

        rain_h = np.zeros(len(t_range))
        for sid in sids:
            r = rain_series_dict[sid].reindex(t_range).fillna(0.0).to_numpy()
            rain_h = np.maximum(rain_h, r)

        # 延伸前置 24h 的降雨（预加载卷积用），但只拟合 t0 之后
        lead_range = pd.date_range(t0 - pd.Timedelta(hours=24), t0 - pd.Timedelta(hours=1), freq="h")
        rain_lead = np.zeros(len(lead_range))
        for sid in sids:
            r = rain_series_dict[sid].reindex(lead_range).fillna(0.0).to_numpy()
            rain_lead = np.maximum(rain_lead, r)

        rain_full = np.concatenate([rain_lead, rain_h])
        obs_full = np.concatenate([np.full(len(lead_range), np.nan), obs_rdii])

        n_valid = np.sum(~np.isnan(obs_rdii))
        if n_valid < _MIN_OBS_PER_EVENT:
            continue

        obs_segs.append(obs_full)
        rain_segs.append(rain_full)
        events_used += 1

    if events_used < _MIN_EVENTS:
        no_fit.n_events_used = events_used
        return no_fit

    # ── 构建联合训练向量 ─────────────────────────────────────────────────
    # 为每个事件独立卷积（不跨事件累积），拼接成一条大向量后拟合
    def _loss(params):  # noqa: N806
        R1, T1, K1, R2, T2, K2 = params  # noqa: N806
        total_sse = 0.0
        total_n = 0
        for obs_f, rain_f in zip(obs_segs, rain_segs, strict=False):
            # obs_full 和 rain_full 等长；前 24 行是预加载期（obs=NaN），NaN mask 自动排除
            pred_full = _predict_rdii(rain_f, R1, T1, K1, R2, T2, K2, dt_h)
            valid = ~np.isnan(obs_f)
            if valid.sum() == 0:
                continue
            diff = obs_f[valid] - pred_full[valid]
            total_sse += float(np.sum(diff ** 2))
            total_n += valid.sum()
        return total_sse / max(total_n, 1)

    # 多起点随机搜索
    rng = np.random.default_rng(42)
    best_loss = np.inf
    best_params = None

    for _ in range(n_starts):
        x0 = np.array([
            rng.uniform(0.005, 0.15),   # R1
            rng.uniform(0.5, 10.0),     # T1
            rng.uniform(1.5, 8.0),      # K1
            rng.uniform(0.002, 0.10),   # R2
            rng.uniform(10.0, 100.0),   # T2
            rng.uniform(2.0, 15.0),     # K2
        ])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = minimize(
                _loss, x0, method="L-BFGS-B",
                bounds=_BOUNDS,
                options={"maxiter": 500, "ftol": 1e-10, "gtol": 1e-6},
            )
        if res.fun < best_loss:
            best_loss = res.fun
            best_params = res.x

    if best_params is None:
        no_fit.n_events_used = events_used
        return no_fit

    R1, T1, K1, R2, T2, K2 = best_params  # noqa: N806

    # ── 计算拟合质量 ─────────────────────────────────────────────────────
    all_obs, all_pred = [], []
    for obs_f, rain_f in zip(obs_segs, rain_segs, strict=False):
        pred_full = _predict_rdii(rain_f, R1, T1, K1, R2, T2, K2, dt_h)
        valid = ~np.isnan(obs_f)
        all_obs.extend(obs_f[valid])
        all_pred.extend(pred_full[valid])

    all_obs = np.array(all_obs)
    all_pred = np.array(all_pred)
    r2_val = _r2(all_obs, all_pred)
    rmse = float(np.sqrt(np.mean((all_obs - all_pred) ** 2)))

    # ── 分类 ─────────────────────────────────────────────────────────────
    fast_frac = R1 / (R1 + R2) if (R1 + R2) > 1e-9 else 0.0
    reliable = r2_val >= _MIN_R2
    if not reliable:
        cat = "fit_unreliable"
    elif fast_frac >= 0.65:
        cat = "fast_inflow"
    elif fast_frac <= 0.30:
        cat = "slow_infiltration"
    else:
        cat = "mixed"

    notes = (
        f"R1={R1:.4f} T1={T1:.1f}h K1={K1:.1f}  "
        f"R2={R2:.4f} T2={T2:.1f}h K2={K2:.1f}  "
        f"R²={r2_val:.3f} RMSE={rmse:.3f}m"
        + ("  [可靠]" if reliable else "  [R²不足，仅供参考]")
    )

    return RTKResult(
        node_id=node_id,
        n_events_used=events_used,
        R1=float(R1), T1_h=float(T1), K1=float(K1),
        R2=float(R2), T2_h=float(T2), K2=float(K2),
        r2=float(r2_val), rmse_m=float(rmse),
        fast_fraction=float(fast_frac),
        category_rtk=cat,
        fit_notes=notes,
    )


# ---------------------------------------------------------------------------
# 管线入口
# ---------------------------------------------------------------------------

def run_rtk() -> pd.DataFrame:
    """读取 processed parquet → 对所有节点拟合 RTK → 写 rtk_by_node.parquet。"""
    from .io_paths import paths, sites
    from .spatial import station_for_node

    p = paths()

    for required in ("events", "bwf_by_node", "node_level_10min", "rainfall_hourly"):
        src = p.parquet(required)
        if not src.exists():
            raise FileNotFoundError(f"找不到 {src}，请先运行上游 stage")

    events_df = pd.read_parquet(p.parquet("events"))
    bwf_df = pd.read_parquet(p.parquet("bwf_by_node"))
    lv_all = pd.read_parquet(p.parquet("node_level_10min"))
    rain_all = pd.read_parquet(p.parquet("rainfall_hourly"))

    # 预处理：rain → dict[station_id → pd.Series(DatetimeIndex, rain_mm_h)]
    rain_dict: dict[str, pd.Series] = {}
    for sid, grp in rain_all.groupby("station_id"):
        s = grp.set_index("ts")["rain_mm_h"].sort_index()
        rain_dict[str(sid)] = s

    node_ids = sorted((sites().get("nodes") or {}).keys())
    results = []

    for nid in node_ids:
        lv_node = (
            lv_all[(lv_all["node_id"] == nid) & (lv_all["qc_flag"] == "good")]
            .set_index("ts")["level_m"]
            .sort_index()
        )
        sid = station_for_node(nid)
        result = fit_rtk_node(
            node_id=nid,
            level_series=lv_node,
            rain_series_dict=rain_dict,
            events_df=events_df,
            bwf_df=bwf_df,
            station_id=sid,
        )
        results.append({
            "node_id":        result.node_id,
            "n_events_used":  result.n_events_used,
            "R1":             result.R1,
            "T1_h":           result.T1_h,
            "K1":             result.K1,
            "R2":             result.R2,
            "T2_h":           result.T2_h,
            "K2":             result.K2,
            "r2":             result.r2,
            "rmse_m":         result.rmse_m,
            "fast_fraction":  result.fast_fraction,
            "category_rtk":   result.category_rtk,
            "fit_notes":      result.fit_notes,
        })

    df = pd.DataFrame(results).sort_values("node_id").reset_index(drop=True)
    out_path = p.parquet("rtk_by_node")
    df.to_parquet(out_path, index=False)
    return df
