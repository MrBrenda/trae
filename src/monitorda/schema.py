"""规范化数据表的 pandera schema。"""

from __future__ import annotations

import pandera as pa
from pandera import Check, Column, DataFrameSchema

# qc_flag 取值
QC_FLAGS = ("good", "null", "stuck0", "impossible", "outlier", "communication_loss")
NODE_KINDS = ("stormwater", "sewage")
GRADE_VALUES = ("High", "Medium", "Low", "NA")
CATEGORY_VALUES = ("混接", "入渗", "直连", "雨水管低效", "未定", "数据不足")


PLANT_INLET_10MIN = DataFrameSchema({
    "ts": Column(pa.DateTime, nullable=False),
    "flow_m3s": Column(float, nullable=True),
    "ph": Column(float, nullable=True),
    "cod_mgL": Column(float, nullable=True),
    "nh3n_mgL": Column(float, nullable=True),
    "temp_c": Column(float, nullable=True),
    "qc_flag": Column(str, Check.isin(QC_FLAGS)),
}, strict=False, coerce=True)


NODE_LEVEL_10MIN = DataFrameSchema({
    "node_id": Column(str, Check.str_matches(r"^[SW]\d{2}$")),
    "ts": Column(pa.DateTime, nullable=False),
    "level_m": Column(float, nullable=True),
    "qc_flag": Column(str, Check.isin(QC_FLAGS)),
}, strict=False, coerce=True)


NODE_FLOW_10MIN = DataFrameSchema({
    "node_id": Column(str, Check.str_matches(r"^[SW]\d{2}$")),
    "ts": Column(pa.DateTime, nullable=False),
    "flow_m3s": Column(float, nullable=True),
    "velocity_ms": Column(float, nullable=True),
    "qc_flag": Column(str, Check.isin(QC_FLAGS)),
}, strict=False, coerce=True)


RAINFALL_HOURLY = DataFrameSchema({
    "station_id": Column(str, nullable=False),
    "ts": Column(pa.DateTime, nullable=False),
    "rain_mm_h": Column(float, nullable=True, checks=Check.ge(0)),
    "rain_mm_cum": Column(float, nullable=True),
    "qc_flag": Column(str, Check.isin(QC_FLAGS)),
}, strict=False, coerce=True)


EVENTS = DataFrameSchema({
    "event_id": Column(str, Check.str_matches(r"^E\d{8}-")),
    "station_id": Column(str),
    "t_start": Column(pa.DateTime),
    "t_peak": Column(pa.DateTime, nullable=True),
    "t_end": Column(pa.DateTime),
    "duration_h": Column(float, Check.gt(0)),
    "total_mm": Column(float, Check.ge(0)),
    "max_intensity_mmh": Column(float, Check.ge(0)),
    "antecedent_dry_d": Column(float, Check.ge(0), nullable=True),
    "compound": Column(bool),
}, strict=False, coerce=True)


BWF_BY_NODE = DataFrameSchema({
    "node_id": Column(str),
    "event_id": Column(str),
    "bwf_q_m3s": Column(float, nullable=True),
    "bwf_level_m": Column(float, nullable=True),
    "window_start": Column(pa.DateTime),
    "window_end": Column(pa.DateTime),
    "n_samples": Column(int, Check.ge(0)),
}, strict=False, coerce=True)


RDII_BY_EVENT_NODE = DataFrameSchema({
    "node_id": Column(str),
    "event_id": Column(str),
    "v_rdii_m3": Column(float, nullable=True),
    "rdii_peak_m3s": Column(float, nullable=True),
    "rise_amp_m": Column(float, nullable=True),
    "lag_start_h": Column(float, nullable=True),
    "lag_peak_h": Column(float, nullable=True),
    "recession_halflife_h": Column(float, nullable=True),
    "illicit_area_km2_low": Column(float, nullable=True),
    "illicit_area_km2_high": Column(float, nullable=True),
    "qrl": Column(float, nullable=True),
    "grade": Column(str, Check.isin(GRADE_VALUES)),
}, strict=False, coerce=True)


NODE_DIAGNOSTICS = DataFrameSchema({
    "node_id": Column(str),
    "name_zh": Column(str),
    "kind": Column(str, Check.isin(NODE_KINDS)),
    "n_events": Column(int, Check.ge(0)),
    "mean_qrl": Column(float, nullable=True),
    "mean_illicit_area_km2": Column(float, nullable=True),
    "mean_rise_amp_m": Column(float, nullable=True),
    "median_lag_start_h": Column(float, nullable=True),
    "median_halflife_h": Column(float, nullable=True),
    "category": Column(str, Check.isin(CATEGORY_VALUES)),
    "evidence_score": Column(float, Check.in_range(0, 1)),
    "notes": Column(str, nullable=True),
}, strict=False, coerce=True)
