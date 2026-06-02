Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
CONTENTS
Disclaimer ................................................................................................................................................ vi
Acknowledgments .................................................................................................................................. vii
Purpose of This Document ..................................................................................................................... viii
Acronyms and Abbreviations ................................................................................................................... ix
Glossary ....................................................................................................................................................x
1. Introduction ................................................................................................................................ 1
2. Smart Data Infrastructure ............................................................................................................ 2
3. Smart Data Infrastructure and Technologies: Information Inputs ................................................. 4
3.1 Continuous Monitoring ................................................................................................... 4
3.2 Level Monitoring ............................................................................................................. 5
3.3 Flow Monitoring ............................................................................................................. 5
3.4 Rainfall Monitoring ......................................................................................................... 7
4. Collection System Optimization ................................................................................................... 8
4.1 CMOM and I/I Control................................................................................................... 10
5. RTC Systems .............................................................................................................................. 11
5.1 Components of an RTC System ...................................................................................... 12
5.2 RTDSS ........................................................................................................................... 13
5.3 Level of Control............................................................................................................. 13
5.4 Guidelines for Applying RTC .......................................................................................... 16
5.5 Key Considerations for RTC Systems .............................................................................. 17
6. Data Management and Sharing ................................................................................................. 18
6.1 Big Data Management .................................................................................................. 18
6.2 Data Sharing ................................................................................................................. 18
6.3 Real-Time Public Notification and Transparency ............................................................ 19
7. Data Analytics ........................................................................................................................... 20
7.1 Data Validation and Filtering ......................................................................................... 20
7.2 KPIs ............................................................................................................................... 21
8. Data Visualization and DSS ........................................................................................................ 23
9. The Future of Data Gathering Technology for Wet Weather Control and Decision-Making ........ 25
10. References ................................................................................................................................ 26
ii

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
APPENDIX A: CASE STUDIES
Albany, New York: CSO and Flood Mitigation ............................................................................................ A-1
Beckley, West Virginia: Flood Risk Mitigation ............................................................................................ A-3
Bordeaux, France: Real-Time Pollution and Flood Control ........................................................................ A-5
Buffalo, New York: Real-Time Control of Inline Storage ............................................................................ A-7
Cincinnati, Ohio: Intelligent Urban Watershed Technology ....................................................................... A-9
Falcon Heights, Minnesota: Predictive Flood Control System ................................................................. A-11
Fort Wayne, Indiana: Maximizing Infrastructure Performance to Reduce CSO Volume and Costs ......... A-13
Grand Rapids, Michigan: Mitigating Inflow and Infiltration with Real-Time Control ............................... A-15
Green Bay, Wisconsin: Reducing Overflows with Real-Time Monitoring ................................................ A-17
Hawthorne, California: Real-Time Monitoring to Prevent Sewer Overflows ........................................... A-19
La Mesa, California: Optimizing Cleaning Maintenance with Smart Monitoring Technology ................. A-20
Louisville, Kentucky: Real-Time Control for Integrated Overflow Abatement ......................................... A-23
Newburgh, New York: Real-Time Control for CSO Reporting/Public Notification ................................... A-26
Ormond Beach, Florida: Flood Risk Mitigation—Extreme Events ............................................................ A-28
Philadelphia, Pennsylvania: Real-Time Control to Manage Retention Pond Discharge ........................... A-30
Rutland, Vermont: Real-Time Control to Meet Public Notification Requirements .................................. A-33
San Antonio, Texas: Smart Sewers to Fulfill Consent Decrees ................................................................. A-35
San Diego, California: Stormwater Harvesting Augmentation Analysis ................................................... A-37
San Francisco, California: Real-Time Control to Model Combined Sewer System ................................... A-39
South Bend, Indiana: Real-Time Control and Real-Time Decision Support .............................................. A-41
Washington, D.C.: Real-Time Controls for Rainwater Harvesting and CSOs ............................................ A-43
Wilmington, Delaware: Real-Time Control to Reduce CSOs .................................................................... A-45
iii

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Disclaimer
The material and case studies presented in this document are intended solely for informational
purposes. This document is not intended, nor can it be relied on, to create any rights enforceable by any
party in litigation with the United States. Case studies used in this document are unique and site-specific,
and they may not be as effective as demonstrated. This document may be revised or updated without
public notice to reflect changes in the technologies and to update and/or add case studies. The U.S.
Environmental Protection Agency (EPA) and its employees do not endorse any products, services, or
enterprises.
Mention of trade names or commercial products in this document does not constitute an endorsement
or recommendation for use.
iv

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Acknowledgments
EPA would like to thank everyone who supported the development of this document. Many stakeholders
and subject matter experts contributed by sharing their technical knowledge of smart data infrastructure
and case studies that highlight the wet weather control and decision support technologies, including:
• Michael Armes, ADS • Keith Hodsden, Innovyze
• Michael Bonomo, ADS • Kerim Kollu, Real Tech Water
• Jay Boyd, ADS • Conor Lewellyn, Opti
• Tim Braun, Xylem • Dayton Marchese, Opti
• James Brescol, Tetra Tech • Luis Montestruque, Xylem
• Geoff Brown, METER Group • Diana Qing Tao, Tetra Tech
• Colin Campbell, METER Group • Marcus Quigley, EcoLucid
• Vanessa Centeno, Opti • Isaac Sachs, Ayyeka
• Sean Cohen, CSL Services • Edward Speer, CDM Smith
• David Drake, SmartCover • Ariel Stern, Ayyeka
• Kevin Enfinger, ADS • Pat Stevens, ADS
• Drew Evans, Real Tech Water • Heather Towsley, SmartCover
• Missy Gatterdam, Metropolitan Sewer • Kaitlin Vacca, Opti
District of Greater Cincinnati • Hari Vasupuram, Opti
• Jonathan Hasson, ADS • Bryan Wacker, METER Group
• Nicole Hathorn, Innovyze • Jeff Wennberg, City of Rutland, Vermont
• Scott Helfrick, ADS
The document was developed under EPA Contracts EP-C-11-009 and EP-C-16-003.
v

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Purpose of This Document
This document was originally developed in August 2018 to share how municipalities, utilities, and related
organizations can use advanced technologies and monitoring data to support both wet weather control
and decision-making in real time or near real time. Advanced wet weather control includes dynamic
systems that remotely adjust facility operations in response to evolving field conditions to manage
combined sewer overflows, sanitary sewer overflows, sewer backups, street flooding, and stormwater
discharges. Technological advancements to support decision-making generally involve a remote
monitoring component that communicates the status and condition of the system. This document
highlights the technologies currently available and provides case studies to describe some of the possible
ways municipalities and utilities implement the technologies. The capabilities of such technologies are
broad and continue to expand and evolve over time.
EPA considers this a living document that is continually updated as new technology and case studies
emerge. The March 2021 version updated existing case studies with new information and added the
following case studies:
• Albany, New York • Green Bay, Wisconsin
• Beckley, West Virginia • La Mesa, California
• Bordeaux, France • Ormond Beach, Florida
• Cincinnati, Ohio • Rutland, Vermont
• Fort Wayne, Indiana • San Francisco, California
• Grand Rapids, Michigan
If you have questions or would like more information regarding this document, please contact:
Mohammed Billah
U.S. EPA Office of Wastewater Management
1200 Pennsylvania Avenue NW
Washington, DC 20460
202-564-2228
Billah.Mohammed@epa.gov
vi

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Acronyms and Abbreviations
BSA Buffalo Sewer Authority
BSB Beckley Sanitary Board
cfs Cubic Feet per Second
CMAC Continuous Monitoring and Adaptive Control
CMOM Capacity Management Operation and Maintenance
CPU Central Processing Unit
CSO Combined Sewer Overflow
DMS Decision-Making Software
DSS Decision Support System
EGLE Michigan Department of Environment, Great Lakes, and Energy
ELTCP Enhanced Long-Term Control Plan
EPA U.S. Environmental Protection Agency
FOG Fats, Oils, and Grease
GUI Graphical User Interface
ICS Industrial Control System
I/I Inflow and Infiltration
IOAP Integrated Overflow Abatement Plan
IoT Internet of Things
IT Information Technology
KPI Key Performance Indicator
LTCP Long-Term Control Plan
LTE-M Long-Term Evolution Category M
MG Million Gallons
MGD Million Gallons per Day
MMSD Milwaukee Metropolitan Sewerage District
MSD Metropolitan Sewer District (Louisville or Greater Cincinnati)
NPDES National Pollutant Discharge Elimination System
O&M Operation and Maintenance
PID Proportional, Integral, Derivative
PLC Programmable Logic Controller
PWD Philadelphia Water Department
RTC Real-Time Control
RTDSS Real-Time Decision Support System
SAWS San Antonio Water System
SCADA Supervisory Control and Data Acquisition
SFPUC San Francisco Public Utilities Commission
SMP Stormwater Management Pond
SSO Sanitary Sewer Overflow
STF Storage and Treatment Facility
VFD Variable-Frequency Drive
WPCP Water Pollution Control Plant
WWTP Wastewater Treatment Plant
vi i

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Glossary
Agent-Based Control: System with locally interacting components that achieve a coherent global
behavior. Through the simple interaction of buying and selling among individual agents, the system
promotes a desirable global effect such as fair allocation of resources.
Big Data: Data sets that are so large or complex that traditional data processing application software is
inadequate to deal with them.
Cloud: System that stores data in large-scale, offsite facilities.
Cognitive Computing: Use of computerized models to simulate the human thought process in complex
situations where the answers may be ambiguous and uncertain.
EPA SUSTAIN: A decision support system that assists stormwater management professionals with
developing and implementing plans for flow and pollution control measures to protect source waters
and meet water quality goals.
Gray Infrastructure: Engineering projects that use concrete and steel.
Green Infrastructure: Projects that depend on plants and ecosystem services.
Internet of Things: Process in which hardware is connected to a network (the internet) so that it can
better communicate with other systems.
Long-Term Control Plan: Written strategy required by the Clean Water Act for communities with
combined sewer systems to reduce and/or eliminate combined sewer overflow discharges in the long
term.
Machine Learning: An application of artificial intelligence that provides systems the ability to
automatically learn and improve from experience without being explicitly programed.
Manning’s Equation: An empirical formula used to estimate the average velocity of a liquid in open
channel flow as a function of channel slope, roughness, and shape.
Model Predictive Control: Model-based control strategy that predicts the system response to establish a
proper control action. This strategy explicitly uses a mathematical model of the process to generate a
sequence of future actions within a finite prediction horizon that minimizes a given cost function.
Real-Time Control: The ability of water infrastructure (valves, weirs, pumps, etc.) to be self-adjusting or
remotely adjusted in response to current weather conditions.
SCADA Historian: A service that collects and stores data from various devices in a supervisory control
and data acquisition network.
Smart Water and Smart Data Infrastructure: The ecosystem of technology tools and solutions focused
on the collection, storage, and/or analysis of water-related data.
Time of Concentration: The time required for runoff to travel from the hydraulically most distant point in
a watershed to the outlet. The hydraulically most distant point is the point with the longest travel time to
the watershed outlet and not necessarily the point with the longest flow distance to the outlet.
v iii

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
1. Introduction
Wet weather—that is, rain and snowmelt—can
What Is in This Document?
significantly increase flows at wastewater
This document summarizes key aspects of utility
treatment facilities, creating operational
operations where smart data systems can provide
challenges and potentially affecting treatment
significant benefits. It is organized as follows:
efficiency, reliability, and control of treatment
Section 2 presents an overview of smart data
units at these facilities.
infrastructure, its relationship with green and gray
Current approaches to wet weather control rely infrastructure, its benefits, and a general “roadmap”
for implementation.
mainly on gray or green infrastructure, or a
combination of the two. In recent years, Section 3 describes technologies applied specifically
however, municipalities and utilities have been to wastewater collection and stormwater systems
considering how they can improve their and key considerations for selection, design,
operations and infrastructure by drawing on implementation, and O&M requirements.
recent technological advances. These advances Section 4 describes the use of smart data
include: infrastructure to promote collection system
optimization, as well as LTCP implementation,
• Faster computer processing and network
modification, and development.
speeds, providing ready access to reliable
Section 5 discusses the use of RTC systems to
information for informed decisions.
maintain and meet operational objectives.
• Smaller, more accurate, less expensive
Section 6 discusses data management, data sharing,
sensors.
and public notification when using smart data
• Low-cost storage of large quantities of data. systems.
• The advent of the IoT, allowing sensors to Section 7 describes data analysis in smart data
systems, including data validation/filtering and the
be connected over large geographic areas.
use of KPIs.
• Smaller, higher-capacity batteries and
Section 8 discusses data visualization and DSS.
photovoltaics, reducing dependence on
Section 9 discusses the future of data gathering
permanent hard-wired power sources.
technology for wet weather control and decision-
• Wireless transmittal of acquired data, making.
reducing the need for continuous or dial-up
Appendix A includes 22 case studies about
hard-wired communications systems.
communities across the country that have
implemented smart data infrastructure
This document focuses on how municipalities,
technologies.
utilities, and related organizations can use
advances in technology to implement “smart
data infrastructure” for wet weather control—
that is, how they can use advanced monitoring
data to support wet weather control and
decision-making in real time or near real time.
Case studies about communities that have done
this across the country are included as
appendices and referenced where applicable
throughout the report.
1

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
2. Smart Data Infrastructure
Smart data infrastructure is the integration of • Prioritizing critical assets and future
emerging and advancing technology to enhance capital planning.
the collection, storage, and/or analysis of water-
• Providing the ability to optimize
related data. These solutions can generally be
collection system storage capacity to
grouped into a framework that consists of
reduce peak flows and the occ urrence of
hardware, communications, and management
overflows.
systems.
• Enabling effective customer service and
• Hardware includes the devices that enhancing public notification.
measure and collect water-related data,
such as level meters, flow monitors, valve Smart data infrastructure can be used to inform
actuators, and pump-run monitors. operational decisions that ultimately improve
the efficiency, reliability, and lifespan of physical
• Communications refers to networks,
assets (e.g., pipes,
including wireless communications, that
pumps, reservoirs,
migrate data from the hardware to the
valves). According
systems that perform analysis.
to Global Water
• Management refers to the software tools Intelligence
and analytical solutions that perform Magazine,
analysis and provide actionable information. implementing digital
It also includes data visualization to give solutions by
managers real-time information for consolidating
decision-making and to communicate with monitoring, data
the public. analytics,
automation, and
Smart data infrastructure leverages hardware,
control could save
communication, and management to provide
up to $320 billion in
real and tangible benefits to utilities, including:
total expected
• Maximizing existing infrastructure and capital expenditures
optimizing operations and responses to be and operating
proactive, not reactive. expenses for
different water and wastewater utilities over
• Providing savings in capital and operational
the five years from 2016 to 2020 (GWI 2016).
spending.
• Improving asset management and The potential cost savings and other factors,
understanding of collection and treatment such as regulations related to water quality, w ill
system performance. likely stimulate the water industry to invest in
smart data infrastructure and increasingly adopt
• Improving LTCP implementation ,
data-driven monitoring and control systems in
modification, and development.
the operation of various combined sewer,
• Meeting regulatory requirements. separate sewer, and municipal separate storm
sewer systems.
2

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
In the future, data feeds and cognitive
computing could significantly help system
managers—both municipal and industrial—by
providing near-instantaneous support
information for many of the routine and
immediate response decisions they must make.
Transformation may help water and wastewater
utilities take advantage of innovations and
opportunities in future O&M (see Figure 1).
Figure 1. Better information and data can lead to
more effective O&M.
Roadmap for Implementing Smart Data Infrastructure
There are few, if any, insurmountable technological barriers to implementing the various technologies
described in this document. RTC technology (Section 5), for example, has been around for nearly 30 years.
While its implementation in collection systems remains relatively limited, its effectiveness has been proven in
many successful applications in WWTPs (U.S. EPA 2006).
When selecting technology and level of complexity, it is important to understand the utility’s priorities and
needs (e.g., O&M, IT, security, data usage requirements). It is also important to remember that smart data
infrastructure is scalable. A utility can start small, applying technology that is compatible with its existing
capacity to ensure full acceptance and utilization of that technology, then move toward a more comprehensive
approach with higher degrees of performance.
Regardless of the size or age of their infrastructure, utilities can benefit from this general roadmap for
implementing smart data infrastructure:
1. Vision for a utility of the future: Imagine how data, assets, and technology could be leveraged to benefit
the utility.
2. Schedule: Understand the capacity and timeframe for staff to accept change.
3. Technology evaluation: Validate data, prove benefits, and understand delivery.
4. Detailed planning: Seek funding and develop an implementation plan.
5. Phased implementation: Deploy the technology and associated platform.
6. Continuous improvement and innovation: Evaluate phase 1 performance and adapt the planning if
necessary.
Key considerations for developing and implementing the roadmap include the following:
• Ensure organizational commitment for staffing and budget needs. There will be initial investment, as well as
annual costs associated with the adoption of a technology.
• Communicate to ensure buy-in and support from all levels of management and foster strategic
partnerships.
• Establish clear authority, roles, responsibilities, and communication channels.
• Define performance expectations.
• Educate and integrate team members early in the project.
• Provide continuous training and technical support to build the existing workforce’s capacity and attract a
new generation of workers.
3

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
3. Smart Data Infrastructure and Technologies:
Information Inputs
Smart data infrastructure can generate highly 3.1 Continuous Monitoring
informative data sets to support wastewater
Continuous monitoring uses permanent
and stormwater collection system decision-
monitoring systems that report data back to a
making. These data sets help to answer critical
central system. The physical quantities to be
questions that allow operators to maximize the
monitored in a wastewater and stormwater
effectiveness and efficiency of system operation
collection system for proper operation and
(Figure 2); however, the usefulness of the data
control are relatively basic and typically consist
generated relies on accurate and relevant
of flows, water levels, and rainfall conditions for
information inputs.
dry and wet weather operations. In addition, the
The following sections describe specific status of equipment (such as pumps, gates, and
strategies and technologies for generating valves) needs to be monitored to ensure safe
useful wastewater and stormwater collection O&M.
system data, including key considerations for
Continuous monitoring, combined with proper
selection, design, implementation, and O&M.
data analytics and effective visualization, can
These strategies and technologies include:
generate significant O&M savings by providing
• Continuous monitoring (Section 3.1) real-time insight into system conditions, which
allows operators to prioritize asset management
• Level monitoring (Section 3.2)
with effective targeted maintenance. Examples
• Flow monitoring (Section 3.3)
include level trend detections that trigger
• Rainfall monitoring (Section 3.4) alarms for equipment maintenance (e.g.,
cleaning), proactive I/I risk assessment, and
data-driven work scheduling and asset
management.
Continuous Monitoring in Practice
MMSD is using continuous monitoring to
monitor the performance, value, and health of
green infrastructure throughout Milwaukee.
MMSD is monitoring 11 separate sites, including
installations in public rights of way, allowing
managers to see the combined and individual
performance of green roofs and bioretention
cells in real time. Every storm is recorded,
performance can be reported in aggregate or by
Figure 2. Operational process supported by information
event, and the data can be used to fine-tune
inputs.
maintenance intervals and maximize
performance.
Key considerations for continuous monitoring of
wastewater collection systems include the
following:
4

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
• The nature of wastewater systems presents the location of measurement. Stilling wells are
a harsh and largely variable environment for usually recommended, as a way to install
monitoring equipment. pressure probes away from potential debris in
the water flow and for easier maintenance.
• In choosing and installing equipment,
operators need to consider physical and Ultrasonic level meters, mounted above the
hydraulic conditions, humidity, grit, water surface, are also very common in
sedimentation, debris, and corrosion, as wastewater applications. They are usually
well as confined spaces and maintenance preferred when space is available above the
access. For example, permanent monitoring monitoring location and minimal obstacles, FOG,
equipment should meet explosive zone or foam are present above the water surface.
classifications. The sensor must be mounted far enough from
• A sensor’s advertised measurement sidewalls to avoid bad readings due to
soundwave reflections.
accuracy may not represent its actual
performance; as such, it will need to be
When monitoring space is small or FOG is
calibrated/verified.
present above the water surface, Doppler radar
• Maintenance requirements, as well as microwave meters are recommended. Their
hydraulic and physical conditions around narrower signal beams lead to more reliable
the monitoring equipment, should be measurements under such conditions.
considered to balance out the increase in
Capacitive probes are particularly suitable for
cost and complexity to provide accurate
multi-point water level monitoring and are
measurements. For example, forgoing some
preferred when a high spatial resolution (of a
level of accuracy by selecting equipment
few millimeters) is necessary—e.g., for a reliable
with easier maintenance needs can ensure
evaluation of stored volumes in large, flat
more reliable readings.
storage facilities. These probes are easy to clean
3.2 Level Monitoring and can handle temperature and pressure
variations. However, they can significantly
Multiple technologies are used to monitor water
disturb flow and should not be used in small
level in wastewater infrastructures. The most
pipes.
common types of sensors are pressure
transducers, ultrasonic level meters, microwave In general, sensors above the water surface
meters, and capacitive probes. Other discrete require less O&M, but are subject to corrosion
devices, such as floating devices and vibrating and may experience issues with ice in cold
level sensors, could be used in some cases. The environments.
most important criteria for choosing a specific
For locations where monitoring the water level
technology will depend on the environment and
is critical, redundant sensors based on different
infrastructure where water level must be
technologies are recommended. For example,
monitored. More precisely, conditions such as
using an ultrasonic meter and a pressure sensor
turbulence, sedimentation, or FOG in the water;
in a storage facility would ensure water level
foam; or obstacles in the air space above the
monitoring in all conditions.
monitoring location must be considered.
3.3 Flow Monitoring
Pressure transducers need to be submerged in
the water where the level must be monitored; Operators can use several technologies and
they are therefore convenient where methods of flow monitoring to better
sedimentation is not a significant issue. They are understand the characteristics of their collection
typically used where water can be turbulent at systems.
5

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
3.3.1 Physical Flow Monitoring 3.3.2 Alternative Flow Monitoring
Typical commercial flow meters available on the Technologies
market include ultrasonic Doppler devices, In some cases, where installing a physical flow
acoustic Doppler sensors, transit time effect meter is too complex or expensive, indirect
sensors, and newer technologies such as means of flow monitoring can be developed
Doppler radar sensors and laser Doppler meters. depending on specific hydraulic conditions.
Transit time effect technologies consist
Level to flow relationship: When pipe flows
exclusively of one or multiple pairs of probes (a
remain under “free surface flow” conditions,
pair includes one transmitter and one receiver)
Manning’s equation can be used to estimate
in a crossing path within the water stream.
flow (based on water level sensor data) and
These probes can measure water velocity at
physical attributes (pipe shape and dimensions,
different layers in the conduit to compute flow
slope, pipe material for the roughness factor) at
values according to water level and pipe section.
the level sensor location. However, the flow
Flow meter technology has been developed to estimation is invalid when the pipe is flowing full
fit a variety of applications; submerged and and under pressure or experiencing backwater
“non-contacting” devices (sensors above the effects.
water surface) are available. Submerged
Equations of flow under the gate: When
technologies are generally recognized as being
modulating gates are used for flow control, gate
more accurate because they can measure the
position and water level data upstream and
different velocities that can co-exist within a
downstream from the gate can be used to
water flow section at the same time, while non-
efficiently compute the flow regulated through
contacting technologies can only measure the
the gate. The mathematical formula would also
velocity from the surface of the water stream.
consider the gate’s hydraulic conditions and
Practical experiences of wastewater flow physical dimensions, the regulation chamber,
monitoring within sewer pipes ranging from 24 and connection pipes. Optimal gate position
inches to 120 inches in diameter and above (i.e., amount of submergence) can vary
have shown that submerged flow meter depending on gate size and flow velocity and
technologies will generally provide must be determined through hydraulic analysis.
measurements with an accuracy from ±10
percent to 20 percent. Non-contacting flow Improving Operations with Monitoring
meter technologies will provide flow Technology
measurements with an accuracy typically SAWS recently participated in a study on the use of
monitoring to inform cleaning maintenance
ranging from ±15 percent to 30 percent. Non-
programs. SAWS equipped 10 high-frequency
contacting devices have lower costs for
cleanout sites with remote field monitoring units
procurement, installation, and maintenance
and used analytical software to monitor day-over-
than submerged technologies. A permanent
day level trend changes and receive messages for
flow meter installation in sewers typically costs
trend anomalies. This analysis of the real-time
from $15,000 to $75,000, or even more if
monitoring data detected small but potentially
significant work is needed for the infrastructures
important changes in water levels. The data
and the electrical utilities. Regular maintenance enabled users to consider actions such as a site
for cleaning, inspection, and calibration is inspection or cleaning. According to the data, SAWS
recommended at least twice a year to keep reduced cleaning frequency by 94 percent in the
monitoring reliable and accurate. study areas. Other than a short period in May/June
2016 when nearly 16 inches of rain overwhelmed
the SAWS system, there were zero SSOs at the pilot
locations.
6

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Based on several facilities’ operations using this on real-time rainfall and level data or forecasted
method, the relative error is under 5 percent radar rainfall, to provide flow values virtually
during dry flow conditions and around 15 everywhere within the wastewater collection or
percent in wet weather conditions. stormwater system. A well-calibrated hydraulic
model provides flow values within an accuracy
Weir relationship: A common mathematical
range from -15 percent to +25 percent (WEF
means of computing flow values uses level
2011).
monitoring data from a static weir upstream.
Specific formulas must be used depending on 3.4 Rainfall Monitoring
the weir’s shape, its dimensions (length, width),
A typical rainfall monitoring system deploys a
and the angle of the flow stream according to
network of rain gauges spaced out to allow for
the weir. This method can provide fairly
representative measurement of rainfall
accurate flow values for weirs under six feet in
quantities over a region. On average, 1 rain
length; weir relationship calculations involve
gauge is recommended for every 500 hectares
significant uncertainties for longer weirs.
(1,235 acres) of coverage (Campisano et al.
Bending weir relationship: A bending weir 2013), although coverage needs vary depending
consists of a mechanical flap gate device with on local climate and need for predictive
pre-determined weights designed to maintain a accuracy.
specified water level on the weir’s upstream
Common rain gauges use tipping bucket
side. When inflows cause the upstream level to
systems—either optical or mechanical—that
rise, the weir opens to evacuate excess flow. An
count the quantity of rain trapped in a
inclinometer can be installed on the bending
calibrated cylinder. Each bucket tip counts a
weir’s flap gate to monitor the gate’s angular
specific quantity of rain (e.g., 0.005 inches) over
opening. Flow can then be estimated using the
a specific time increment.
corresponding flow and weir angle relationship
charts provided by the manufacturer. Such rainfall monitoring can be made available
in real time and can be used as an input to a
Flap gate equations: As with bending weir
hydraulic model to compute flow predictions in
relationships, mathematical functions can be
the sewer collection system. The flow
developed to compute flows through flap gates.
predictions can then be used to determine the
Such a computation requires installing an
time of concentration of the area tributary to
inclinometer on the flap gate and a level meter
the monitoring location. In addition, when
upstream of the gate. A downstream level
combined with radar reflectivity data and
meter will also be needed if the flap gate can
rainfall predictions, rainfall monitoring can help
become submerged. Typically, a temporary flow
produce flow forecasts with a more accurate
meter calibrates and validates the equation.
level over the entire territory. Generally, rainfall
Model-based flow computations: Most utilities forecasting windows and grid sizes should be
have developed calibrated hydrological and proportional to the hydrologic element’s longest
hydraulic models (e.g., EPA SWMM 5) to time of concentration in the tributary collection
adequately represent their wastewater systems. system where control is desired—e.g., a large
These models are typically used to plan, design, CSO. Rainfall forecasts should cover at least two
and produce engineering diagnostics. They can hours ahead.
be configured for real-time simulations, based
7

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
4. Collection System Optimization
A key benefit of smart data infrastructure is its facilities in real time, a process often
application in system optimization to maximize referred to as RTC. RTC systems are
the effectiveness of existing infrastructure discussed in greater detail in Section 5 of
investments and reduce the need for future this document.
capital investment. It provides a framework for
optimizing the design and O&M of wastewater Optimizing Collection System Capacity and
and stormwater systems by collecting and Performance
PWD has committed to reducing 7.9 billion
analyzing large data sets.
gallons of overflows in Philadelphia by 2036
There are two types of system optimization: through better stormwater runoff management.
As part of this effort, PWD and a private
• Offline improvements (Muleta and Boulos corporation have collaborated to use smart data
2007). Examples include raising weirs to technology to monitor and maximize the
reduce overflow discharge, developing best performance of an existing stormwater
efficiency curves to minimize energy costs retention basin. The basin was retrofitted with
technology to monitor water level and
and reduce equipment breakdowns, and
precipitation, as well as to provide real-time
optimizing the placement of localized
active control to selectively discharge from the
stormwater management and green
basin during optimal times, effectively
infrastructure control. For example, the EPA
increasing the useful capacity of the asset.
SUSTAIN modeling framework uses an
optimization approach to identify the least- Table 1 presents the data used in a smart data
cost and highest-benefit solutions to infrastructure approach, regardless of
achieve user-defined objectives (U.S. EPA optimization type.
2009).
• Online optimization to actively manage the
operation of wastewater networks and
8

Smart  Data Infrastructure  for Wet Weather Control and Decision Support   March  2021
Table  1. Data Required to Optimize the Design, Operation, and Maintenance of Wastewater and
Stormwater Systems
Data Required
| Objective   | Cause of  Problem   | Potential Intervention   |     |
| ----------- | ------------------- | ------------------------ | --- |
for System  Optimization
Eliminate  SSOs   •   Rainfall-derived I/I   •   Pipe replacement   •   Level and flow measurements
•   Undersized pipes   •   I/I mitigation measures    •   Sewer and land characteristics
•
Cost of potential  interventions
•   Grease, debris, and   •   Improved operating   •   Level, velocity, and flow
|     | sedimentation   | procedures                       | measurements                           |
| --- | --------------- | -------------------------------- | -------------------------------------- |
|     | buildup         | •   Pipe replacement             | •   Camera inspection                  |
|     |                 | •   Cleaning (pipes,  streets)   | •   Cost of potential  interventions   |
•   Flushing systems
|     | •   Pipe breaks   | •   Repairs   | •   Flow measurements   |
| --- | ----------------- | ------------- | ----------------------- |
•   Leaking manholes   •   Pipe  replacement   •   Camera inspections
|     | •               |     | •               |
| --- | --------------- | --- | --------------- |
|     | Offset joints   |     | Smoke testing   |
•   Cost of potential  interventions
Minimize   •   High electricity   •   Pump replacement   •   Time-of-use electricity tariffs
| operating costs   | consumption for   |                   |                                   |
| ----------------- | ----------------- | ----------------- | --------------------------------- |
|                   |                   | •   Use of VFDs   | •   Level and flow measurements   |
pumps  and gate
|     |     | •   Improved set points   | •   Critical elevation for  basement  |
| --- | --- | ------------------------- | ------------------------------------- |
operation
and  street flooding
•   Improved controller
|     |     | parameters   | •   Gate, pumps, and actuator   |
| --- | --- | ------------ | ------------------------------- |
characteristics
•   Cost of potential  interventions
Minimize   •   High equipment and   •   Repairs   •   Level and flow measurements
| maintenance   | sensor failure rate   | •             | •                               |
| ------------- | --------------------- | ------------- | ------------------------------- |
|               |                       | Replacement   | Equipment and sensor history    |
costs
|     |     | •   Re-localization            | •   Equipment inventory  and cost   |
| --- | --- | ------------------------------ | ----------------------------------- |
|     |     | •   Preventive and predictive  | •   Detailed alarms                 |
maintenance
•   Maintenance and  calibration
|     |     | •   Best efficiency point    | history   |
| --- | --- | ---------------------------- | --------- |
•   Cost of potential  interventions
•   Sedimentation issues   •   Improved  operating level   •   Level and velocity
|     |     | •   | measurements   |
| --- | --- | --- | -------------- |
Sewer modification to
|     |     | increase velocities    | •   Camera inspections                 |
| --- | --- | ---------------------- | -------------------------------------- |
|     |     | •   Flushing devices   | •   Cost of potential  interventions   |
|     | •   | •                      | •                                      |
Minimize CSOs   Rainfall-derived  I/I   Upgrade of existing   Level and flow measurements
•   Undersized facilities   facilities   •   Sewer and land characteristics
•
(conveyance, storage,   Addition of green and   •   Operational and  physical
|     | treatment)   | gray infrastructure   | constraints   |
| --- | ------------ | --------------------- | ------------- |
•
|     |     | RTC implementation   | •   Cost of potential  interventions   |
| --- | --- | -------------------- | -------------------------------------- |
Reduce flooding   •   Rainfall-derived  I/I   •   Upgrade of existing   •   Level and flow  measurements
| risks   |     | facilities    |     |
| ------- | --- | ------------- | --- |
•   Undersized facilities   •   Sewer and land characteristics
|     | (conveyance, storage)   | •   Addition of green and   | •   |
| --- | ----------------------- | --------------------------- | --- |
Operational and physical
gray infrastructure
constraints
|     |     | •   RTC implementation   | •   |
| --- | --- | ------------------------ | --- |
Critical elevation for  basement
and street flooding
•
Cost of potential  interventions

9

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
4.1 CMOM and I/I Control
Optimizing the performance of the collection approaches help ensure that the collection
system is the key component in CMOM system capacity is maximized for wastewater
programs. CMOM programs combine standard conveyance, which is a critical component of all
O&M activities with an increased level of data CMOM programs. In addition to direct
gathering and information management to monitoring, flow rate and level metering data
operate collection systems more effectively. can be used along with asset management data
Smart data infrastructure, equipped with the to predict the “unmetered” portions of a
data input tools described in Section 3, can help collection system and determine other areas at
accomplish this. Successful CMOM programs are risk of capacity-related issues, such as high I/I.
used to identify and mediate capacity-related
Facilities can use smart data infrastructure
issues in a system, reducing the risk of system
tools—such as real-time metering and
failures such as SSOs.
information analysis—to understand the
CMOM includes control of I/I, the process by variables that affect collection system capacity
which unintended clearwater sources (e.g., and performance. This knowledge would allow
groundwater and excess stormwater) exceed utilities to better plan for necessary capital
the design capacity of a collection system, expenditures and optimize system performance
typically due to antiquated, deteriorating, or for current and future needs.
inadequately maintained infrastructure. Long-
term flow and level metering data can be
analyzed to determine performance trends over Using Smart Data Infrastructure and RTC to
a long period. Historical trends of I/I peak flow Reduce CSOs
The Louisville MSD was an early adopter of RTC,
rates and volumes can be used to identify areas
applying inline storage since the 1990s and
with high rates of I/I, prioritize removal efforts,
pioneering global, optimal, and predictive RTC
and evaluate the costs/benefits of those efforts.
that has been in operation since 2006. The RTC
system is key to maximizing the MSD’s
Real-time flow rate and level data collection can
conveyance, storage, and treatment capacity to
be used to identify localized capacity limitations,
reduce CSOs, with consistent operational results
blockages, and sediment accumulation. These
capturing more than 1 billion gallons of CSO
data can then inform more proactive volume annually. Incorporating RTC into MSD’s
management approaches that can reduce LTCP has resulted in about $200 million in
overflows in both dry and wet weather. Such savings compared to traditional methods.
10

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
5. RTC Systems
RTC can be broadly defined as a system that
Using RTC to Maximize Capacity and
dynamically adjusts facility operations in Performance
response to online measurements in the field to In 2008, South Bend, Indiana, installed and
maintain and meet operational objectives commissioned a real-time monitoring system of
during both dry and wet weather conditions more than 120 sensor locations throughout the
(U.S. EPA 2006). city. In 2012, the city and its partners
commissioned and distributed a global, optimal
Wastewater systems are often purposely RTC system to maximize the capacity and
oversized. This extra capacity can provide short- performance of the city’s collection system. Since
term storage in the conveyance and treatment 2012, the city has added additional sensor
system when rain falls unevenly across the locations and rain gauges, bringing the total
collection system and runoff lag times vary. RTC number to 152 sites. It also added automated
gates at several stormwater retention basins to
presents opportunities to optimize full system
better control when and at what rate stormwater
capacity for both existing and proposed
is released downstream into the combined
facilities. Potential benefits include receiving
system. In the period from 2008 through 2014,
water quality protection, energy savings (Tan et
South Bend eliminated illicit dry weather
al. 1988), flow equalization, reduced flooding,
overflows and reduced its total CSO volume by
integrated operations, and better facility
roughly 70 percent, or about 1 billion gallons per
planning (Gonwa et al. 1993). Real-time or near-
year.
real-time reporting can also help utilities meet
the public notification requirements for CSO and The application of RTC in a stormwater system is
SSO discharges. similar to that of a wastewater system. It
requires continuous monitoring (e.g., water
A well-designed RTC system can address a
level, rainfall, weather forecast), control devices
number of different operational goals at
(e.g., valves, gates), and data communication to
different times. Examples of operational goals
actively manage flows and adapt to changing
include (U.S. EPA 2006):
conditions. If required, temperature, infiltration
• Reducing or eliminating sewer backups and rate, and water quality parameters (e.g., total
street flooding. suspended solids, nitrogen) can be monitored in
real time and integrated into the RTC
• Reducing or eliminating SSOs.
management strategy.
• Reducing or eliminating CSOs.
• Managing/reducing energy consumption. Benefits of using RTC in stormwater
management include:
• Avoiding excessive sediment deposition in
the sewers. • Optimizing the design and sizing of control
• Managing flows during a planned measures.
(anticipated) system disturbance (e.g., • Reducing the frequency of flooding.
major construction).
• Improving water quality with extended
• Managing flows during an unplanned (not residence time.
anticipated) system disturbance, such as
• Increasing stormwater harvesting and reuse.
major equipment failure or security-related
• Adapting to evolving conditions through
incidents.
operation change rather than new
• Managing the rate of flow arriving at the
infrastructure.
WWTP.
11

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
• Providing auditable performance and components are essential for RTC (e.g., sensors,
supporting data from the monitoring system meters), while others may be optional
components without additional costs. depending on the desired level of control. The
• Reducing O&M costs by issuing alerts in real components are represented with boxes, and
the arrows that connect them indicate the
time.
communications and data that are passed on
Figure 3 presents a typical layout of the possible between the components.
components of an RTC system. Some
Figure 3. Components of an RTC system.
5.1 Components of an RTC System into it. These rules are feedback algorithms that
base action on the difference between a set
An RTC system, at a minimum, includes sensors
point and the measured variable. For example, a
that measure the process, control elements that
PLC may be programmed to maintain a certain
adjust the process, and data communication
level in the wet well and will reduce the flow
between them (Schilling 1989). Typical control
through the pump if the level is too low or
elements for a wastewater system are
increase it if the level is too high. The PLC
regulators, such as pumps (constant or variable
programs can include set points that are defined
speed drives), gates (sluice, radial, sliding,
locally and receive “remote” set points from a
inflatable), and adjustable weirs (bending weir,
central server.
weir gates).
5.1.1 SCADA Systems
At each remote site, sensors are connected to
SCADA systems have become more prevalent in
the inputs of the local RTC device—in most
the wastewater industry for collecting and
cases, a PLC or remote terminal unit. The PLC
managing monitoring data. SCADA is a control
provides outputs (control set points and signals)
system architecture that uses computers,
to the control elements (e.g., gates, pumps)
networked data communications, and GUIs for
based on the rules embedded (programmed)
12

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
high-level process supervisory management.
RTC and CSO Control
Large SCADA systems have evolved to be
The MSD of Greater Cincinnati has one of the most
increasingly similar in function to distributed
challenging collection systems in the country to
control systems, which are widely used for
manage during wet weather, as it contains more
process control at the treatment plants. SCADA
than 200 CSO points. Together, these overflows
system designs have taken full advantage of
discharge over 11 billion gallons of sewage into the
advances in IT to collect, archive, and process
Ohio River and its tributaries annually. In 2014, MSD
large amounts of data. began installing sensors throughout its largest
watershed. By early 2016, MSD had gained real-time
A SCADA system’s fundamental purpose is to
visibility and control of its wastewater system in this
communicate data and control commands from
watershed and transformed the wastewater
a centrally located operator to geographically
collection system into a “smart sewers” network. To
dispersed remote locations in real time. The date, MSD’s smart sewer system covers over 150
communication technology options include square miles (about half) of its service area,
telephone-based transmission (used in early incorporating 2 major treatment plants, 6 wet
SCADA systems due to low cost), fiber-optic weather STFs, 4 major interceptor sewers, 164
cable, radio system, cellular-based overflow points, and 32 rain gauges and river level
communication, wireless internet access, and sites. Remote monitoring has improved the
maintenance of wet weather facilities and enabled
satellite-based systems.
upstream facilities to account for downstream
Designing a SCADA system depends on a wide interceptor conditions, increasing overflow capture
range of practical considerations, including but basin-wide during wet weather.
not limited to equipment enclosures,
environmental conditioning, field interface
5.2 RTDSS
wiring, system documentation requirements, An RTDSS generally overlays the SCADA system.
system testing requirements, IT requirements, It is connected to the SCADA database to
and cybersecurity. retrieve system status information. An RTDSS
can use a SCADA historian and GUI to program
As utilities invest in continuous monitoring and
and display system status and trends (e.g.,
SCADA, the generated data must be regarded as
abnormal flow, critical water level alarm) or
an important investment to extract maximum
provide additional dashboards involving data
values. According to the U.S. Geological Survey,
analytics to support O&M decision-making. In an
“poor data quality, redundant data, and lost
RTC system, an RTDSS performs complex
data can cost organizations 15 percent to 25
calculations based on information inputs to
percent of their operating budget” (USGS n.d.).
inform operational decisions and help
Information captured in the field needs to be determine optimal system set points (e.g., flow
communicated from the remote stations to the to be pumped, water level to be maintained in a
computers and systems that will process, store, wet well or pipe length). Typically, decision
and archive it. The SCADA system is considered support uses advanced computing algorithms
the backbone of an RTC system. It includes that are interactive and multi-objective and
standard GUI tools that operators can access, often involve using an online model for weather
and it allows them to manually override any forecasting.
remote site control actions at any time. As the
5.3 Level of Control
needs for real-time or near-real-time public
notifications rise, centralized data management The RTC system can be automated with a
can facilitate data sharing and enable greater centralized or distributed control technology.
transparency.
13

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
The main difference is the control and the algorithms used to determine control logics and
input/output subsystems: set points vary in complexity from simple
operating rules to complex mathematical
• In distributed control architectures, the
optimization techniques (Garcia-Gutierrez et al.
number and quality of CPUs is determined
2014). It is a good solution only if the control
by the number of modules. Each module has
objectives can be reached without transferring
a controller, though the system usually
any information between other remote sites.
features a central master PLC. The module
PLCs automate their respective areas and Regional control is similar to local control
usually do not include visualization features. except in that a telemetry system exchanges
data with other remote sites. Regional control
• A central architecture usually features a
can be implemented as a distributed or
computer that deals with all tasks such as
centralized system built on a SCADA system. A
input/output connections, PLC, and control.
municipality might design its own DSS to control
Computing capacity, therefore, must be
the collection system based on the specific
significantly higher than that of a distributed
constraints and opportunities at each control
control technology system. There is only
site. However, the control remains reactive, not
one CPU, which means that only one such
predictive. This limits the distances between the
spare part is needed. RTC system design
control structures and measurements; as such,
criteria drive the selection of a control
the operation must remain conservative and
system platform based on the physical and
suboptimal.
logical components of the system.
Global control is necessary when the control
Regardless of the control platform, RTC can be
objectives require strong coordination of the
implemented using local, regional, or global
control actions at numerous remote sites on a
control. The levels of control are classified
system-wide level. The set points are usually
according to progressive increases in
computed and refreshed periodically (e.g., every
complexity, performance, and benefits (Schütze
5 to 15 minutes). The global strategy used to
et al. 2004).
determine the set points includes rule-based
Local control, or a local reactive control system, and optimization-based techniques (Figure 4).
is the simplest form of automatic control. Local Rule-based control considers scenarios that can
control is used to solve specific issues that only occur during wastewater system operation and
require information collected near a regulator determines appropriate control actions based
and is usually implemented as a single-input, on experience. The rules are generally easy for
single-output feedback loop designed to operators to implement and understand.
maintain prescribed set points (e.g., flow or However, the quality and the performance of
level set points). These set points can be those rules depend highly on the available
displayed to the operator for manual control or expert knowledge. For large and complex
be sent back to the SCADA system in real time wastewater systems, the strategy may demand
for automated control of remote sites. The many rules.
14

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Figure 4. Control strategies for wastewater utilities.
An optimization-based strategy involves an Optimizing the collection system requires
optimization problem that represents the continuous and strategic adjustment of control
desired behavior of the wastewater system. devices, as well as predictions of upcoming
Various algorithms can be used to solve the inflows and their spatial distribution (Cartensen
optimization problem (e.g., model predictive et al. 1998). With proper conditions being
control, agent-based optimization). More monitored, acknowledged, and controlled, a
detailed descriptions of optimization strategies global RTC system considers the distribution of
and mathematical models can be found in flow in the entire system, both under current
Papageorgiou (1988) and Garcia-Gutierrez et al. conditions and in the future. Using a global RTC,
(2014). a utility can open and close gates or pumps to
transfer flows between sites, providing
In the last 20 years, model predictive control has
temporary storage and controlled release of
been the most extensively used optimization-
significant volumes of wastewater.
based strategy. This approach uses a
mathematical model of the wastewater system Table 2 summarizes which components of the
to generate a sequence of future actions— overall system must work properly to support
within a finite prediction horizon—that different control modes/levels (U.S. EPA 2006).
minimizes a cost function (Gelormino and Ricker Notably, forecasting may be part of a rule-based
1994). Interest in model predictive control is system, but it is not mandatory. A global RTC
justified by its ability to explicitly express system often involves a mixture of lower levels
constraints in the system, anticipate future of RTC and static controls.
system behavior, and consider non-ideal
elements such as delays and disturbances.
15

Smart Data Infrastructure for Wet Weather Control and Decision Support        March 2021
| Table 2. Components Needed for Different Control Modes    |     |     |     |     |     |     |     |     |     |
| --------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
snoitacinummoC/ADACS

revreS ADACS lartneC
gnitsaceroF llafniaR
|     |     |     |     |     |     |     | revreS CTR lartneC   |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- |
gnirotinoM ,tupnI
rotarepO evitcA
|     | Control Mode  |     |     |     |     |     |     |     |  ledoM enilnO   |
| --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --------------- |
  stnemurtsnI

sCLP
| Local manual control                 |     |     |     | X       |           |   X    |      |     |     |
| ------------------------------------ | --- | --- | --- | ------- | --------- | ------ | ---- | --- | --- |
| Local automatic control              |     |     |     | X    X  |           |        |      |     |     |
| Regional automatic control           |     |     |     | X    X  |   X    X  |        |      |     |     |
| Supervisory remote control           |     |     |     | X    X  |   X       |   X    |      |     |     |
| Global automatic control—rule-based  |     |     |     |         |           |        |      |     |     |
|                                      |     |     |     | X    X  |   X    X  |        | X    |     |     |
Global automatic control—optimization    X    X    X    X      X    X    X
|                                     |     |     |     |     | engineers, and other stakeholders; and  |     |     |     |     |
| ----------------------------------- | --- | --- | --- | --- | --------------------------------------- | --- | --- | --- | --- |
| 5.4    Guidelines for Applying RTC  |     |     |     |     |                                         |     |     |     |     |
|                                     |     |     |     |     | equipment surveys.                      |     |     |     |     |
In most cases, RTC implementation can offer
benefits and improve the performance of urban    If the simulation shows that RTC would be
wastewater or stormwater systems. The costs    feasible and beneficial, the third step involves
and extent of these benefits may differ from    detailed planning of the RTC system and its
| one system to the next.  |     |     |     |     | implementation, including:  |     |     |     |     |
| ------------------------ | --- | --- | --- | --- | --------------------------- | --- | --- | --- | --- |
The first step in evaluating if RTC is suitable and      •    Detailed planning of control infrastructures.
| viable for a utility is to develop criteria for a    |     |     |     |     | •                                         |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | ----------------------------------------- | --- | --- | --- | --- |
|                                                      |     |     |     |     |   Detailed design of control algorithms.  |     |     |     |     |
| macroscopic evaluation using a scoring system        |     |     |     |     |                                           |     |     |     |     |
|                                                      |     |     |     |     | •    Risk and failure analysis.           |     |     |     |     |
| (Erbe et al. 2007, Schütze et al. 2004). Criteria    |     |     |     |     |                                           |     |     |     |     |
•    Detailed design of data infrastructure (or
| may include environmental and financial            |     |     |     |     |                                              |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | -------------------------------------------- | --- | --- | --- | --- |
|                                                    |     |     |     |     | gap analysis if data infrastructure already  |     |     |     |     |
| objectives, the topology of the catchment area,    |     |     |     |     |                                              |     |     |     |     |
|                                                    |     |     |     |     | exists).                                     |     |     |     |     |
| collection system characteristics and conditions,  |     |     |     |     |                                              |     |     |     |     |
operational system behaviors, etc.     •    Staff training and other organizational
|     |     |     |     |     | planning (i.e., new roles and  |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | --- |
The utility may, however, skip the first step if it
|                                                 |     |     |     |     | responsibilities).                              |     |     |     |     |
| ----------------------------------------------- | --- | --- | --- | --- | ----------------------------------------------- | --- | --- | --- | --- |
| has already invested in a hydrological and      |     |     |     |     |                                                 |     |     |     |     |
|                                                 |     |     |     |     | •    Preparations for getting consent from the  |     |     |     |     |
| hydraulic model that adequately represents its  |     |     |     |     |                                                 |     |     |     |     |
|                                                 |     |     |     |     | regulatory authorities.                         |     |     |     |     |
| system and operation and/or has substantial     |     |     |     |     |                                                 |     |     |     |     |
monitoring coverage (which provides good    It is critical to involve operator input from the
system understanding and condition    beginning of the design process. The operators
| assessment). The utility can use these existing   |     |     |     |     |                                               |     |     |     |     |
| ------------------------------------------------- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- |
|                                                   |     |     |     |     | are ultimately responsible for the system     |     |     |     |     |
| tools and data in the second step, which          |     |     |     |     |                                               |     |     |     |     |
|                                                   |     |     |     |     | operation and performance. Early involvement  |     |     |     |     |
| involves a preliminary analysis of RTC potential  |     |     |     |     | will ensure that the system design addresses  |     |     |     |     |
and costs/benefits. The analysis should include a    their O&M concerns, and that they buy into the
| simulation study of a full range of RTC control  |     |     |     |     |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
system.
| levels to determine which is the most          |     |     |     |     |     |     |     |     |     |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| appropriate; staff interviews with operators,  |     |     |     |     |     |     |     |     |     |
|                                                |     |     |     | 16  |     |     |     |     |     |

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
5.5 Key Considerations for RTC change operational mode by giving the operator
Systems a standard operating procedure.
An RTC system should have robust operation,
Using Smart Data Infrastructure to Promote
adequate communication, supervisory manual Resiliency
override, operational confidence, and In response to the historic drought conditions
adaptability (Gonwa et al. 1993, Colas et al. recently experienced in California, the City of San
2004). The system must be designed and Diego has decided to quantify the potential nexus
configured to ensure a high level of between stormwater capture and its ongoing effort
to reclaim wastewater as a drinking water resource
performance under normal conditions and safe
(San Diego currently imports more than 80 percent
operation under downgraded conditions. Its
of its water supply). The city equipped its
performance should be better than or equal to
stormwater control measures with RTCs and
the system that existed before RTC
assessed them to optimize the management of
implementation.
stormwater storage and release to the reclaimed
water system. The simulations suggested that
Under all conditions, there are critical
stormwater harvesting could substantially augment
constraints, such as operating safely, avoiding
local water supplies while complying with
equipment damage, and avoiding flooding. A
stormwater quality regulations.
well-designed RTC system must effectively
manage different operational objectives and
The reliability of all RTC system components is
transition between different operational modes
key to successful implementation. In addition to
to operate reliably and efficiently; at a
failsafe and risk management procedures,
minimum, it must address externally caused
system effectiveness can be obtained through
equipment failures and emergency conditions.
the following:
The failsafe procedures must be configured so
• Proper selection, location, and number of
that they are triggered when the requirements
sensors to ensure accurate and adequate
for the system’s current operational mode
measurements.
cannot be met. They should automatically place
• Installation of redundant equipment at key
the system into the next (lower) mode/level of
locations using different technologies.
operation that can be fully supported. For
example, if the system is operating in local • Real-time validation of monitoring data to
automatic control mode and the PLCs minimize the amount of low-quality data
malfunction or lose power, it would need to entering the decision-making process.
revert to local manual control. • Design of safety features, including
emergency isolation gates, power supplies,
RTC system risk management procedures must
generators, and equipment interlocks
include the ability to deal with emergency
specifically designed for safe operation
conditions detected using field measurements.
when a critical alarm is activated.
Special rules can be defined to react to • Preventive and targeted maintenance to
conditions such as rapidly rising levels within the ensure equipment availability.
system. The emergency response can be either
• Stock of replacement pieces for critical
to adjust the automatic control strategy or
infrastructure.
17

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
6. Data Management and Sharing
Good data management and sharing can allow various departments within an organization to
operators and control systems to integrate data improve efficiency and interoperability.
faster and more effectively. Organized and Organizations must also be able to securely
carefully designed data management systems exchange data with outside administrative
readily obtain and act on data from various domains for transparency and for integrated
sources, reducing redundancy and the cost of solutions on city-wide or region-wide scales.
collection system operation.
As more data have moved to cloud-based
6.1 Big Data Management storage, the protection and encryption of off-
site data has become more important. While
More monitoring requires more data
there are still cybersecurity risks, significant
management and storage. To address the
improvements have made it much more difficult
challenges of storing, processing, recovering,
for outside parties to access critical data and
sharing, and updating large data sets,
information.
organizations are finding smarter data
management approaches that enable them to
Cybersecurity
effectively corral and optimize their data use.
The interconnectivity of hardware and data
management has increased the need for utilities to
Some of the best practices for big data
plan and manage cybersecurity. Although
management are to reduce the data amount
networking multiple systems provides operational
(because the vast majority of big data is either
value, it can also expose systems to new data
duplicated or synthesized), to virtualize the
security risks. As utilities move to advanced data
reuse and storage of the data, and to centralize
storage solutions, addressing cybersecurity will be
management of the data set to transform big an essential aspect of master planning activities.
data into small data (Ashutosh and Savitz 2012). Cybersecurity provides insurance to protect utility
assets against attacks, outages, and threats, and it
A smarter data management approach not only
reduces the costs of downtime.
allows big data to be backed up far more
effectively, but also makes it more easily Key considerations for data infrastructure and
recoverable and accessible at significantly lower data sharing include the following:
cost. Other benefits include the following:
• As organizations become more dependent
• Applications need less computing time to on cloud-based systems and other internet-
process data. based solutions, a robust, maintainable, and
• Data can be better secured because secure network infrastructure becomes
critical. Nothing works when the network
management is centralized, even though
access is distributed. goes down. Secure, redundant, and scalable
internet connections are now required for
• Data analysis results are more accurate
day-to-day business as essential processing
because all copies of data are visible.
is moved off site.
6.2 Data Sharing • Network architecture is increasingly
important: robust, secure solutions must be
In addition to the needs of public notification
designed into systems to manage devices
and regulatory reporting (e.g., post-construction
potentially numbering in the thousands,
performance monitoring, permit compliance),
there is a rising need for data sharing among
18

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
each with multiple data points. Simply using
Real-Time Public Notification
a “firewall” to secure a network is no longer The City of Newburgh, New York, replaced its
feasible. combined sewer telemetry system with a
wireless system. The prior telemetry system
• Formerly isolated SCADA/ICS must now
used pressure sensors that had to be located
communicate over the internet. To securely
beneath the influent channel, in direct contact
realize the vast benefits of cloud computing
with the flow and in the combined sewer
and the IoT, secure data interconnectivity is regulator environment where debris would
essential. Standards have been produced to regularly damage or displace them. The new
ensure a high degree of interoperability and system’s sensors hang from the manhole cover
security for evolving SCADA/ICS solutions. above and do not contact the water, avoiding
damage. The new system’s wireless satellite
Emerging Technologies for Big Data connectivity is more reliable than land phone
Management lines at a lower cost. Any computer, tablet, or
For big data management, all types of data smartphone with internet access can
analytics will be more widespread and communicate with the telemetry system,
incorporate more artificial intelligence. Already, allowing for real-time staff and public
machine learning has been applied in predictive notification of CSO events.
analytics for I/I characterization, based on
analysis of long-term data trends. be shared to better inform the end user. A
common example includes the public
6.3 Real-Time Public Notification and notification for current/recent overflow activity
Transparency to local receiving waters. The real-time
notification of overflow activity informs the
Implementation of a smart data infrastructure
public that recreational uses may be temporarily
allows utilities to disseminate relevant and
compromised, potentially reducing public health
current information to ratepayers and
issues. Public notification can also include
stakeholders. Public notification is becoming the
automated notification to the regulating
norm for informing interested parties of current
agencies as part of permit requirements.
utility conditions. While some data must be kept
private due to security issues related to
protecting treatment processes, some data can
19

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
7. Data Analytics
Most utilities already generate a substantial Utilities that have already invested heavily in
amount of process and monitoring data for continuous monitoring could use data analytics
various purposes. As the amount of data to get significant value from the data they
generated each year increases at an exponential collect.
rate, it is increasingly critical to convert those
There are many data analysis and data mining
data into useful information (Greiner 2011).
solutions, which also incorporate data
Technical advancements in complex
warehousing, database management systems,
multidimensional data analysis and data mining
and online analytical processing.
can help utilities analyze incredible amounts of
data to detect common patterns or learn new 7.1 Data Validation and Filtering
things. This can lead to significant operational
Data validation is an important consideration for
improvements and dollar savings for
wastewater utilities, particularly for monitoring
wastewater systems.
data within the harsh environment of a
Big data analytics, a well-established concept, wastewater collection system. Raw monitoring
involves analyzing the data collected to discover data can contain erroneous readings, which
trends and correlations, uncover hidden could be due to one or a combination of the
patterns and other insights to understand why following:
certain behavior or incidents happened, and
• Noise (high frequency fluctuations)
then use that insight to predict what will
happen. Today’s technology and advancements • Missing values
in big data analytics bring speed and efficiency, • Values out of range
which enable utilities to analyze large quantities • Outliers (sudden peaks)
of data and identify insights for immediate
• Constant (or frozen) values
decisions (Figure 5).
• Drifting values (changes in values over a
longer period)
As the quality of the insights gained from data
analytics or the control system’s performance
will be directly linked to the quality of the data
used, raw data from the sensors needs to be
validated and possibly filtered before being used
for further analysis or control purposes. This is
Emerging Technologies for Data Analytics
The IoT industry trend is to provide more
accessibility through cloud computing platforms
and open source technologies. The digital platform
will streamline the integration of data from
various legacy systems and eliminate data
duplication and bad data for more effective and
Figure 5. Big data analytics support enhanced
powerful data analytics and insight. Cloud-based
decision-making and more effective, less costly
computing has already been implemented for
operations.
SCADA system applications and RTC applications.
20

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
an important step to improving the data’s Cross-validation methods are used when it is
reliability. possible to develop a model or relation between
two or more values. The simplest cases are
Data validation can be carried out on a single
where some sensors are redundant and
variable (single data validation methods) or by
measure the same value or where software can
comparing two variables when two or more
be used to produce another sensor’s estimate. A
measures are correlated (cross-validation) (U.S.
range or rate of change validation can then be
EPA 2006, Sun et al. 2011).
carried on the difference between the two
Single data validation methods include the values. In more complex cases, the redundancy
following: can come from combining sensor data with a
model to produce many estimates of a specific
• Range validation: The values that are variable (soft sensors or virtual sensors). The
outside an expected range are flagged as
data reconciliation technique can then be used
invalid. The expected range is based on the
to better estimate the variable.
working range of the sensor itself and on
the process monitored. For example, a Filtering can be used to reduce the
water level in a collection system cannot be measurement noise inherent to sensor data.
lower than the bottom of the chamber This produces smoother, easier-to-analyze data
where the sensor is located and can seldom and usually leads to better results with control
exceed ground level. processes.
• Gap filling: When data are missing (due to All RTC system data should be validated in real
communication failure, sensor automatic time. Data validation can be implemented at the
calibration, etc.), it is possible to use an local PLC and at the central control station.
estimate instead. In a real-time context, the Whenever possible, data validation processes
last valid value can be used. If correlation should take advantage of the correlation
exists with other measurements, cross- between the measurements (i.e., cross-
validation techniques can also be used to validation methods). At minimum, the data
produce better estimates (see below). In a validation algorithms should use sensor alarms
post-event analysis, a simple linear and be able to detect missing data, out-of-range
interpolation between the values before values, outliers, and frozen measurements.
and after the gap can often be used.
7.2 KPIs
• Rate of change validation: If a value
Developing KPIs based on computations of
changes at a greater rate than a probable
validated data can provide a quick and general
change in measured conditions and sensor
understanding of the system’s performance.
noise, it is marked as invalid.
Some of the meaningful KPIs applied for
• Running variance validation: A value is wastewater and stormwater systems include
flagged as invalid if the variation over a past the following:
value is too small. A frozen value is often
due to a sensor failure. • Precipitation frequency: The average
recurrence of rainfall can be assessed using
• Long-term drift: Expected mean check and
rain gauge readings (NOAA n.d.). Maximum
acceptable trend check are two methods to
rainfall depth over various durations is
detect long-term drift. Once bias or drift is
calculated and compared to precipitation
detected, its source needs to be identified—
frequency estimates for the area and
it could be caused by sensor drift or be a
precipitation data used for hydraulic model
genuine long-term trend.
development and calibration.
21

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
• Treated flow: Maximum flow conveyed to only partial treatment before discharge can
the WWTP is compared to the WWTP’s be used to assess system performance and
treatment capacity. If CSOs or significant compliance.
retention occur while the treatment
• Retention volume: Maximum stored
capacity is not met, it can signal a
volume can be presented relative to full
suboptimal system or control.
capacity. If CSOs occur while the full
• Untreated flow: Estimated or measured retention capacity is not met, it can signal a
overflow from the collection system prior to suboptimal system or control.
treatment is compared to total flow treated
• Retention duration: Exceedingly long
at the WWTP. This is typically measured as
durations can lead to odor problems in
number of overflows and/or the volume of
wastewater storage systems.
overflows. These values can be compared to
those projected or allowed under an • CSO/SSO volume and duration: Overflow
discharges can be reported to the public in a
approved LTCP or NPDES permit to assess
timely manner.
system performance and compliance.
• Partially treated flow: Estimated or
measured volume of wastewater receiving
22

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
8. Data Visualization and DSS
Data visualization is the use of charts or graphs analyze monitoring data, run model simulations,
to present large amounts of complex data—and and assess the impact of potential decisions by
thus to convey concepts quickly, easily, and using “what if” scenarios. While the data can be
universally. It enables data users and decision- displayed and analyzed in real time to identify
makers to visually explore analytics, so they can areas that need attention or improvement, the
grasp difficult concepts or identify new patterns. appropriate actions can be taken at a later time.
Interactive visualization allows the user to take For example, DSS can display real-time level
the concept a step further by using technology data correlating to expected flow behavior.
to drill down into charts and graphs for more Abnormally high-level data would indicate a
detail, to interactively change the data displayed potential debris blockage, and the
and how it is processed (SAS n.d.). corresponding response decision would be to
schedule a maintenance crew to perform a field
Data visualization is a key component of the
investigation. However, this action could be
user interface for any DSS. A DSS (also known as
optimized with other work orders to improve
a DMS) is a computer-based information system
maintenance efficiency.
that supports business or organizational
decision-making activities. DSS has three main An RTDSS allows decision-makers to respond to
functions: information management, data short-term variations in wastewater and
quantification, and model manipulation. stormwater systems where lead times for
decisions vary from a few hours to a few days at
• Information management is the storage,
most. Typical RTDSS examples include:
retrieval, and reporting of information in a
structured format convenient to the user. • Hydraulic flow diversions
• Data quantification is the process by which • Storage basins to manage levels or volumes
large amounts of information are • CSO or SSO discharge warnings
condensed and analytically manipulated • Flood forecasting and warnings
into a few core indicators that extract the
information’s essence. See Section 5.2 for additional details on the
RTDSS.
• Model manipulation refers to the
construction and resolution of various Before buying the various computer systems
scenarios to answer “what if” questions. It and software needed to create a DSS, utilities
includes the processes of model should consider (Inc. n.d., WERF 2005):
formulation, alternatives generation and
• Establishing business needs and value for
solution of the proposed models, often
DSS, such as providing guidance for complex
through several operations
operation.
research/management science approaches
(Inc. n.d.). Its main objective is to convert • Evaluating the development of DSS
data into usable and actionable knowledge. applications using available software, such
as spreadsheets, SCADA, or asset
There are two main types of DSS tools, one for
management software.
planning purposes and another for real-time
decision support (Hydrology Project n.d.). For • Integrating information spanning more than
wastewater and stormwater applications, DSS is just one functional domain into the DSS, as
typically structured to allow users to access and well as support decisions from multiple
domains.
23

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
• Creating user-friendly DSS for easy viewing • Understanding how the DSS is used, such as
and access, as well as allowing users to the limitations or assumptions of the
create scenarios and to simulate and mathematical calculations or processing
analyze the impacts of different scenarios. model used within the DSS.
• Ensuring the investment in terms of time • Examining other factors, such as future
and effort to incorporate DSS into daily interest rates and new legislation, in the
operations. decision-making process.
• Providing necessary training and knowledge
to use DSS effectively.
24

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
9. The Future of Data Gathering Technology for
Wet Weather Control and Decision-Making
Rapid advancements in data gathering related to the frequency, volume, and duration
technologies have already led to substantial of wet weather events. Operators will have
improvements for real-time operational support increasingly better information to determine the
and decision-making systems. Future occurrence of wet weather discharges and to
advancements will continue to be made in the calculate the impact of wet weather events on
following areas: collection system capacity. Better understanding
these system characteristics will lead to
• Monitoring the frequency, volume, and
improved infrastructure design and
duration of overflows and discharges within
management, and ultimately the prevention of
combined and separate sanitary sewer
failures and overflows.
systems.
Pollutant sensor technology will also continue to
• Water quality of flows within sewer
improve, and operators will be able to monitor
systems, discharges, and receiving streams;
pollutant impacts on water quality more often
specifically, real-time measurements of
and in real time. Operators will also be able to
bacteria, nutrients, suspended solids, and
more closely monitor pollutants (such as
possibly emerging pollutants.
bacteria) of particular concern to public and
• Operational data to inform asset environmental health.
management systems and long-term
Continued improvements in data gathering will
planning.
increase the effectiveness and reliability of data-
The advancement and proliferation of new
informed operations, and ultimately change the
technologies for gathering and analyzing wet
pace at which operational decisions can be
weather infrastructure data will lead to the
made, moving increasingly toward real time.
generation of more accurate information and
Increasing the amount and frequency of reliable
provide for lower-cost operations. With more
data will also enhance asset management
accurate data, operators will be able to make
programs and promote more informed capital
more informed decisions, increasing efficiency
planning. Wet weather system O&M was at one
and reducing risks.
time conducted on a solely reactive basis. As
technology and operational strategies have
Technology advancements will continue to
improve our ability to quantify wet weather advanced, and more precise and accurate data
events and monitor water quality in ways we are more readily available, operators have now
have never been able to before. In the future, shifted their approaches toward preventive and,
better technology will exist for generating data in some cases, predictive O&M practices.
25

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
10. References
Ashutosh, A., and E. Savitz. 2012. Best practices for managing big data. Forbes Magazine. Accessed Feb.
14, 2017. <http://www.forbes.com/sites/ciocentral/2012/07/05/best-practices-for-managing-big-
data/#58202fdeef02>
Campisano, A., J. Cabot, D. Muschalla, M. Pleau, and P.-A. Vanrolleghem. 2013. Potential and limitations of
modern equipment for real time control of urban wastewater systems. Urban Water Journal.
doi:10.1080/1573062X.2013.763996.
Cartensen, J., M.K. Nielsen, and H. Strandbaek. 1998. Prediction of hydraulic load for urban storm control
of a municipal WWT plant. Water, Science and Technology 37(12): 363–370.
Colas, H., M. Pleau, J. Lamarre, G. Pelletier, and P. Lavallée. 2004. Practical perspective on real time
control. Water Quality Research Journal of Canada 39(4): 466–478.
Erbe, V., M. Schutze, and U. Haas. 2007. Application of a guideline document for sewer system real time
control. Novatech Conference, Lyon, France: 761–768.
Garcia-Gutierrez, L., E. Escobar, J. Barrero-Gomez, N. Quijano, C. Ocampo-Martinez, and D. Tellez. 2014.
On the modelling and real time control of urban drainage systems: A survey. 11th International
Conference on Hydroinformatics, HIC 2014, New-York City, USA.
Gelormino, M.S., and N.L. Ricker. 1994. Model-predictive control of a combined sewer system/
International Journal of Control 59(3): 793–816.
Gonwa, W., A.G. Capodaglio, and V. Novotny. 1993. New tools for implementing real time control in sewer
systems. Proceedings of 6th International Conference on Urban Storm Drainage, Niagara Falls,
Ontario Canada: 1374–1380. Reference No. I6226.
Greiner, L. 2011. What is data analysis and data mining? Accessed February 15, 2017.
<http://www.dbta.com/Editorial/Trends-and-Applications/What-is-Data-Analysis-and-Data-Mining-
73503.aspx>
GWI. 2016. Need to know. Global Water Intelligence Magazine 17(12): 4–5.
Hydrology Project. n.d. Decision Support Systems—Decision Support System-Planning (DSS-P). Accessed
February 15, 2017. <http://hydrology-
project.gov.in/Decision%20Support%20System%20Planning.html>
Inc. n.d. Decision support systems. Accessed February 14, 2017.
<http://www.inc.com/encyclopedia/decision-support-systems.html>
Muleta, M., and P. Boulos. 2007. Multiobjective optimization for optimal design of urban drainage
systems. World Environmental and Water Resources Congress: 1–10.
NOAA. n.d. Precipitation frequency data server (PFDS). National Oceanic and Atmospheric Administration.
Accessed February 15, 2017. <http://hdsc.nws.noaa.gov/hdsc/pfds/index.html>
Papageorgiou, M. 1988. Certainty equivalent open-loop feedback control applied to multireservoir
networks. IEEE Transcripts on Automatic Control 33(4): 392–399.
26

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
SAS. n.d. Data visualization: What it is and why it matters. Accessed February 10, 2017.
<https://www.sas.com/en_us/insights/big-data/data-visualization.html>
Schilling, W. 1989. Real time control of urban drainage system. The State-of the-Art IAWPRC Task Group
on Real Time Control of Urban Drainage System, Pergamon Press, London.
Schütze, M., A. Campisano, H. Colas, W. Schilling, and P. Vanrolleghem. 2004. Real time control of urban
wastewater systems—Where do we stand today? Journal of Hydrology 299: 335–348.
Sun, S., J.-L. Bertrand-Krajewski, A. Lynggaard-Jensen, J. van den Broeke, F. Edthofer, M. do Céu Almeida,
À. Silva Ribeiro, and J. Menaia. 2011. Literature review of data validation methods.
Tan, P.C., K.P. Dabke, and R.G. Mein. 1988. Modelling and control of sewer flow for reduced cost
operation of a sewage pumping station. IEE Transcripts on Systems, Man, and Cybernetics 18(5):
807–813.
U.S. EPA. 2006. Real time control of urban drainage networks. U.S. Environmental Protection Agency. EPA-
600-R-06-120.
U.S. EPA. 2009. SUSTAIN—A framework for placement of best management practices in urban watersheds
to protect water quality. U.S. Environmental Protection Agency. EPA-600-R-09-095.
<https://www.epa.gov/sites/production/files/2015-10/documents/sustain_complex_tools.pdf>
USGS. n.d. Value of data management. U.S. Geological Survey. Accessed February 15, 2017.
<https://www2.usgs.gov/datamanagement/why-dm/value.php>
WEF. 2011. Prevention and control of sewer system overflows. WEF Manual of Practice No. FD-17, Third
Edition. Water Environment Federation, Prevention and Control of Sewer System Overflows Task
Force.
WERF. 2005. Decision support systems for wastewater facilities management. Water Environment
Research Foundation. WERF Report 00-CTS-7.
27

Smart Data Infrastructure for Wet Weather Control and Decision Support March 2021
Appendix A
Case Studies

OWNER LOCATION INCEPTION
City of Albany Albany, New York October 2016
KEY FEATURES
 Wet weather flows reduced 6.5 times more than a traditional passive design would.
 Better understanding of asset condition, performance, and maintenance needs.
 Better pre-event planning and emergency management.
PROJECT DESCRIPTION
Beaver Creek District, the largest sewershed in Albany’s
“As we implement plans for future CSO
combined sewer system, discharges over 530 MG of CSOs
abatement and flood mitigation
annually to the Hudson River. The city has invested in capital
projects, we will continue to expand
projects as part of its LTCP to address its CSO and flash
flooding issues and mitigate property damage and potential this smart infrastructure network
safety hazards. One such project is a smart infrastructure across the city.”
network and a number of interconnected CMAC sites (see
Figure 1). The technology has provided the city with —Joseph E. Coffey, Jr., P.E.
increased infrastructure performance, improved resilience, Commissioner, Albany Water Board
and data-driven operations and planning. Using CMAC, the
Albany Water Board reduced wet weather flows by 6.5 times as much as a traditional passive design
while only increasing project capital cost by 6.5 percent. With the ability to observe watershed behavior
and optimize infrastructure performance, the Albany Water Board is improving stormwater management
for the community.
Figure 1. The Albany Water Board uses CMAC to optimize the use of storage throughout the
collection system.
Appendix A: Case Studies A-1
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Albany, New York
In the past, Albany’s CSOs, flash flooding, and system surcharging issues caused significant damage and
created potential health hazards in both the city and several downstream communities. The Albany
Water Board and its design consultants took a progressive approach to these issues, merging innovative
technology with traditional gray strategies and green infrastructure practices. At the heart of the solution
is a smart infrastructure network, with products that integrate sensors, flow controls, and the weather
forecast to optimize discharge rates from stormwater storage infrastructure to the collection system. In
addition, the smart infrastructure network:
 Provides the city with visibility into asset condition, performance, and maintenance needs.
 Informs the city about pre-event planning activities and emergency management.
 Provides autonomous control of flows during critical wet weather periods.
The use of digital solutions for data-driven stormwater management has helped Albany improve
environmental outcomes, comply with regulatory requirements, and enhance customer service. Strong
performance and return on investment have supported Albany’s decision to deploy additional
monitoring and control sites and grow the interconnected smart watershed—a resilient, data-driven
approach to solving the city’s most critical stormwater challenges.
The addition of CMAC technology enhanced the storage infrastructure’s wet weather performance by 6.5
times as compared to passive control, at a fraction of the cost. Table 1 presents a comparison of cost and
performance between the CMAC and passive solutions at three storage sites in the collection system.
Table 1. Cost and Performance Comparison Between the CMAC and Passive Solutions
Hansen Ryckman Washington All
Description
Passive CMAC Passive CMAC Passive CMAC Passive CMAC
Capital cost $1.35M $0.1M $0.750M $0.1M $2.50M $0.1M $4.60M $0.3M
Incremental wet
weather flow reduction 0.996 2.75 1.31 4.75 7.45 56.1 9.75 63.6
(MG/year)
Unit cost ($/gallon/year) $1.35 $0.04 $0.57 $0.02 $0.34 $0.002 $0.47 $0.005
CMAC incremental
7.4% 13.3% 4.0% 6.5%
capital investment
CMAC performance
improvement compared 2.8x 3.6x 7.5x 6.5x
to passive control
Appendix A: Case Studies A-2
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
Beckley Sanitary Board Beckley, West Virginia July 2016
KEY FEATURES
 Adaptive controls used to optimize an undersized stormwater pond for which few other options
were available.
 Downstream flooding potential reduced from four to five events per year to nearly none per
year, while deferring millions of dollars of stormwater conveyance upgrades.
 Wet weather flow reduced by 57 percent, compared to 3 percent without adaptive controls.
PROJECT DESCRIPTION
Two urban watersheds converge at the intersection of Robert C. Byrd Drive and Ewart Avenue in Beckley,
West Virginia. This has created a longstanding flooding issue: four or five times a year, stormwater
overwhelmed the pipe’s capacity and flooded five lanes along State Route 16, causing a significant risk to
traffic and damaging the road and nearby infrastructure. BSB partnered with state and federal agencies
to address the problem.
The cost of upgrading the existing roadway stormwater conveyance system was estimated to exceed
$2.5 million. BSB proposed a stormwater retrofit alternative: a detention pond located on existing city-
owned property to capture and detain runoff from the Ewart Avenue watershed. This property was
relatively small, which meant that the pond’s size and passive outlet structure limited the alternative
system’s capacity to manage all the anticipated runoff from the contributing watershed. Due to these
limitations, roadway flooding was only marginally improved. The dry detention structure also had limited
function to address state water quality and total maximum daily load requirements that had been
instituted due to bank erosion and sedimentation. To improve the performance of the Ewart Avenue
stormwater pond, BSB implemented CMAC technology in 2016.
Appendix A: Case Studies A--3
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Beckley, West Virginia
Figure 1. Pre- and post-storm conditions at the Ewart Avenue stormwater pond.
By implementing CMAC at the Ewart Avenue stormwater pond, BSB was able to improve water quality,
increase channel protection, and significantly reduce flood risk without building any new downstream
stormwater conveyance and management facilities. The pond is conservatively configured to prevent
drawdown and to aggressively respond to a broad range of forecasted precipitation events. Figure 1
shows the stormwater pond empty in preparation for a storm and at full capacity after a storm.
BSB used wet weather flow reduction and other environmental metrics to compare CMAC to the passive
design. CMAC reduced wet weather flow by 57 percent, versus 3 percent with the passive design. Its
average retention time was 32 hours, while the passive design’s was 7 hours. Peak flow reduction was 84
percent with CMAC versus 36 percent with the passive design. As Figure 2 shows, retaining more runoff
in the pond than the outflow reduced downstream wet weather flow. The annual cost to reduce wet
weather flow was estimated to be $0.02 per gallon with CMAC versus $0.36 per gallon with the passive
design.
Figure 2. Ewart Avenue stormwater pond performance (data set for all sites, August 2018
to August 2019).
Appendix A: Case Studies A--4
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

|     | OWNER   |     |     |     | LOCATION   |     |     |     | INCEPTION   |
| --- | ------- | --- | --- | --- | ---------- | --- | --- | --- | ----------- |

| Bordeaux Métropole   |     |     |     |     | Bordeaux, France   |     |     |     | 2005   |
| -------------------- | --- | --- | --- | --- | ------------------ | --- | --- | --- | ------ |

KEY FEATURES

 75 percent average reduction of CSO volume.
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
 82 percent reduction in CSO frequency.
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

222 million euros ($263 million USD) in capital investment savings.
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
PROJECT DESCRIPTION

Figure 1. Recreation on the Garonne River in Bordeaux, France.

Bordeaux Métropole services 578 square kilometers (223 square miles) along the Garonne River (shown
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
in Figure 1), including more than 150 open streams. About one-fourth of the habitable area is below the
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
river’s high water line, and many floods have occurred since the 1980s. Like many old communities in the
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
United States, Bordeaux mainly has combined sewers that convey both sewage and stormwater—which
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
may be loaded with heavy metals and oil and grease from roadway runoff.

When rainfall exceeds the capacity of the sewer system, CSOs discharge to local waterbodies. To protect

the population against flooding and control pollution in receiving waterbodies, namely the Garonne River

and Bordeaux Lake, Bordeaux Métropole embarked on an LTCP to implement an intelligent central water
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
management system. The LTCP included the construction of several large stormwater and wastewater
storage facilities, tunnel interceptors, and large pumping stations.

In 2013, Bordeaux Métropole began to invest in a capital improvement project plan worth 18 million
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
euros ($21.4 million USD) to integrate RTC into their sewer system. The RTC plan identified three phases
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
for implementation:

1. Offline storage basin capacity of 42,000 cubic meters (11.1 MG) and inline storage capacity of
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
40,000 cubic meters (10.6 MG). Phase 1 was commissioned in 2012–2014 and has reduced CSO

volume by 40 percent annually.

|     |     |     |     |     |     |     | Appendix A: Case Studies  |     | A-5    |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | ------ |
|     |     |     |     |     |     |     |                           |     |    -   |
Any mention of trade names or commercial products does not constitute an endorsement or
|     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.
|     |     |     |     |     |     |     |       |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |

Project Profile Bordeaux, France
2. 200,600 cubic meters (53 MG) of additional storage in existing retention basins built for flood
protection. Phase 2 was commissioned in 2018 and has reduced CSO volume by more than 75
percent annually.
3. Integration of the Garonne River’s right shore area with a storage tank volume of 14,300 cubic
meters (3.8 MG). Phase 3 is anticipated to be completed by 2022.
Bordeaux Métropole has existing storage reserved for 10-year rainfall events. But rainfall from smaller
storms (i.e., storms that occur about once a month) can cause CSOs if not captured. The flood control
storage has capacity to reduce CSOs as well, but the two objectives must not conflict—the system needs
to stay prepared for flood mitigation in anticipation of intense rain (i.e., dewater storage basins, empty
pump station wet wells). This requires a sophisticated RTC system with predictive capabilities. Study
results confirmed that optimizing existing facilities before building new infrastructures generated
significant environmental and cost benefits. The study found retention capacity for CSO reduction in the
existing system’s storage basins was 256,900 cubic meters (67.9 MG) and 40,000 cubic meters (10.6 MG)
for inline storage.
According to Bordeaux Métropole, the overall implementation of RTC cost 8 million euros ($9.5 million
USD) to manage 15 sites, including pump stations and storage facilities, in real time. To achieve
equivalent storage using traditional methods would have required building 230,000 cubic meters (60
MG) of storage at a cost of about 222 million euros ($263 million USD). The savings have allowed
Bordeaux Métropole to invest in restoring the Garonne River’s city shore by converting abandoned
storage and old industrial sites to boardwalks, biking trails, and public parks.
The RTC approach did present several challenges:
 It relies on an online model and real-time rain gauges to predict upcoming inflows and their
spatial distribution. This requires periodic calibration and updating of the hydrologic and
hydraulic model to represent the wastewater system adequately.
 The control strategy and decisions need to account for inaccuracy in rainfall distributions and
real-time monitoring data.
 Meteorological forecast data are provided for a period of one hour, while the RTC prediction
horizon has to be set at four hours to account for flow conveyance delays. Forecasts beyond the
one-hour horizon have to be extrapolated based on a normal curve to correspond with the one-
hour prediction horizon.
 The level of water infiltration varies seasonally and based on specific areas. To help mitigate this
issue, a specialized external model was developed to feed the RTC optimization algorithm with
these varying inputs.
Lessons learned from this project include the following:
 The adoption of RTC technology requires organizational commitment and staff buy-in.
 Hydraulic modeling and system planning are the keys to successful implementation.
 The baseline scenario and rainfall references must be well chosen, as they will be useful during
the entire life cycle of the project for performance comparison purposes.
 The utility needs to consider O&M issues and constraints when choosing the level of RTC
implementation.
 It is important to involve system operators early in planning and design. It is also important to
identify and communicate roles and responsibilities at every stage.
 Documentation such as standard operation procedures and post-event analysis is critical in
properly operating, maintaining, and improving an RTC system.
Appendix A: Case Studies A-6
-
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
Buffalo Sewer Authority Buffalo, New York Commissioned winter 2016;
study period March–May 2016
KEY FEATURES
 CSO volume reduced by 450 MG over 12 months by the first 3 sites—100 MG more than
originally projected for the entire project.
 $145 million saved to date from initial enforcement action, due in large part to reductions in CSO
activations and volume.
 More sewage captured and treated safely instead of overflowing during wet weather into
Buffalo’s receiving waters.
PROJECT DESCRIPTION
At the turn of the century, Buffalo was the eighth largest city in the United States, a gateway for
commerce and manufacturing due to its early embrace of hydroelectric power from nearby Niagara Falls.
To accommodate its projected growth, Buffalo built a state-of-the-art combined sewer system that
collected and transmitted sanitary and stormwater flows in a single pipe system to the Buffalo River,
Scajaquada Creek, and the Niagara River.
By mid-century, the city added a massive wastewater treatment facility and upgraded its sewer system
to accommodate at least 750,000 people. This allowed the city to capture dry weather sewer flows and
send them to the plant, but the combined sewer system was still designed to send the vast majority of
wet weather flows to the city’s receiving waters.
Due to its mid-20th-century sewer design, Buffalo still typically experiences nearly 2 billion gallons of
CSOs annually, discharging into its receiving waterways.
As the level of national awareness of the need to protect water resources continued to grow, federal and
state regulators began pursuing a consent decree in 2006 requiring further improvements to Buffalo’s
collection system. Recognizing the generally inadequate stormwater capabilities of the existing combined
sewer system, the BSA began to prepare a comprehensive watershed improvement plan with gray,
green, and smart sewer solutions. After years of negotiations, the city and its partners came to an agree-
ment; in 2014 BSA received approval of its LTCP for CSO abatement, which had an earlier estimated
budget of $525 million. With the city facing limited funds from a reduced taxpayer base, BSA needed an
innovative approach to address CSOs.
City officials knew they could not continue operating their collection system the same way they had been
since the 1950s, and costly investments in new gray infrastructure like tunnels and storage tanks were
equally infeasible. BSA and its contractors began designing and implementing an RTDSS across the city.
Appendix A: Case Studies A--7
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Buffalo, New York
The RTDSS strategy focused on building and controlling inline storage vaults to transform Buffalo’s
massive gravity sewer system into a managed conveyance and storage system. The goal of the RTDSS
program is to minimize and/or eliminate CSOs by retrofitting the operational behavior of the existing
infrastructure. Sixteen RTDSS sites were identified for inline storage and optimal conveyance throughout
the city. These sites were chosen for maximum return on investment; the first 2 sites were selected as a
representative sample of all 16. Figure 1 shows a visualization of the Bird RTC Chamber, one of the inline
storage vaults in Buffalo’s sewer system.
Figure 1. Visualization of the Bird RTC Chamber.
By 2019, four storage sites were live. BSA is working to build and commission most of the rest by the end
of 2020. The first 3 sites alone have reduced Buffalo’s CSO volume by 450 MG over the 12 months ending
June 30, 2019. This nominal volume is already 100 MG more than what was anticipated for all 16 sites
according to a typical-year simulation—that is, the BSA RTDSS program could end up reducing CSOs by 3
or 4 times as much as originally projected.
As each wet weather event provides more data, BSA can expect increasing levels of system intelligence,
resulting in additional O&M cost reductions as well as further reductions in CSOs. BSA’s RTC program is
achieving outcomes unpredicted in the original design, with even more sewage than estimated now
capable of being safely stored, conveyed, treated, and released to receiving waters as clean water
effluent in a wider variety of weather conditions.
BSA was able to present a revised LTCP with a $145 million reduction in budget due to its RTDSS
program. The RTDSS retrofits, and additional minimally invasive green and gray infrastructure
improvements, will enable critical environmental progress at a far more sustainable cost to residents.
The success of BSA’s RTDSS program may mean even more capital infrastructure savings in the future as
BSA achieves its ongoing environmental, economic, and water equity objectives.
Appendix A: Case Studies A--8
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
Metr opolitan Sewer District
Cincinnati, Ohio 2015
of Greater Cincinnati
KEY FEATURES
 Overflow volumes reduced by 247 MG annually.
 Cost reduced more than 90 percent compared to initial capital work estimated at $38 million.
 CSO mitigation achieved at a price of less than $0.01/gallon.
PROJECT DESCRIPTION
The MSD of Greater Cincinnati serves an Ohio population of more than 850,000 spread out across 290
square miles. Like many large cities, Cincinnati has combined and sanitary sewer systems, some of which
were built more than a century ago. Whether by design or due to I/I of stormwater, these systems tend
to overflow, discharging untreated sewage into local waterways or flooding streets and basements.
Cincinnati’s sewers discharge an average of 11.5 billion gallons of combined sewage every year into the
Ohio River and its tributary streams within Cincinnati’s urban watershed. In 2002, the U.S. EPA entered
into a federal consent decree with MSD, mandating the elimination of SSOs and significant mitigation of
CSOs into receiving waterways. Engineers estimated the cost to mitigate the sewer overflows at $3.1
billion, an unacceptable capital expense to pass along to MSD’s customers.
Recognizing the generally inadequate stormwater management capabilities of the existing combined
sewer system, MSD prepared a comprehensive wet weather improvement plan. MSD knew that full
sewer separation and deep tunnel construction are massive capital investments with very low return:
they create only episodic benefits during peak flow and are single-use assets with little additional
community wealth creation. Instead, MSD sought to use decision intelligence to maximize existing
capital assets such as sewer interceptors, STFs, and pump stations—to reduce overflows and gain
system-wide benefits through advanced control logic that would optimally operate MSD’s urban
watershed.
MSD began by focusing on the Mill Creek Interceptor (a major carrier of flows through the MSD service
area) and its most upstream asset, the SSO 700 STF. This facility and four other control sites were
originally designed to reduce overflow volumes from the constructed outfall at the river. SSO 700 STF
has 3.6 MG of storage and a 10 MGD high rate treatment capacity. These assets, combined with the RTC
facilities downstream on the Mill Creek Interceptor, provide multiple points to control sewage along the
length of the interceptor.
Historically, SSO 700 STF and the RTC facilities have been controlled locally without any coordination
between them and other facilities. To cost-effectively increase performance and capacity utilization,
Appendix A: Case Studies A--9
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

| Project Profile   |     |     |     | Cincinnati, Ohio   |     |
| ----------------- | --- | --- | --- | ------------------ | --- |
MSD implemented a RT-DSS that  combines sensors, weather data, and artificial intellige nce. The RT-DSS
delivers automated, optimized control of existing assets to reduce sewage overflows, maximize stora ge,
| and maximize treatment during wet we ather.  |     |     |     |     |     |
| -------------------------------------------- | --- | --- | --- | --- | --- |
|                                              |     |     |     |     |     |
SSO 700 STF is now controlled based on real-time upstream and downstream conditions, along with
|     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- |
real-time feedback on what is happening at two of the downstream RTC facilities (Ross Run and Mitchell
Avenue) . This allows MSD to use analytics in deciding whether to activate or deactivate high-rate
treatment and when to fill or drain tanks. Figure 1 p  resents the flow analytics application da shboard for
| the SSO 700 STF.  |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- |
|                   |     |     |     |     |     |
|                   |     |     |     |     |     |
Figure 1. Flow analytics  application dashboard for  the  SSO -700  treatment facility.
The project was an overwhelming success. After MSD implemented the coordinated  RTC program,
overflow volumes  dropped  by 247  million gallons annually (based  on 2015 rainfall). Implementation of
the  control system, compared to work estimated to cost  more than $38 million, meant a 90 percent  cost
savings was realized by  MSD’s  ratepayers. Moreover, CSO mitigation was achieved at a price of less than
$0.01/gallon.
This  approach enabled MSD to achieve significant reductions in both the capital and operating costs of
collecting and treating wastewater in compliance with environmental regulations.
|     |     |     | Appendix A:  Case Studies    |     | A--10   |
| --- | --- | --- | ---------------------------- | --- | ------- |
Any mention of trade names or commercial products does not  constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products,  services or enterprises.

OWNER LOCATION INCEPTION
Capitol Region Watershed District Falcon Heights, Minnesota July 2015
KEY FEATURES
 Optimized stormwater management using RTC and adaptive logic.
 Doubled flood control capacity in an existing wet pond.
 Less risk to nearby residential areas and infrastructure.
PROJECT DESCRIPTION
Curtiss Pond in Falcon Heights, Minnesota, collects runoff from a 38-acre watershed. A playground and
residential area surround the pond. Large storms have caused pond overflows and several feet of
standing water in the surrounding area, threatening infrastructure and private property. To eliminate
this flooding, which poses an imminent safety concern, the Capitol Region Watershed District designed a
network of perforated pipes, 10 feet in diameter, to temporarily store and infiltrate the overflow.
However, the physical space for the pipe network was limited.
To eliminate the flooding, the District installed an
“Did you know that innovative
intelligent retention system that uses weather forecasts to
technology can automatically check
predict the amount of runoff from a watershed and
the weather and activate water
prepare the pond to receive the forecasted water. The
system autonomously draws down the pond during dry management structures that protect
periods, maximizing available capacity in advance of wet your neighborhood from flooding? The
weather. This active control allows for a smaller design system will reduce flooding in the park
volume while using the pond’s full storage capacity to
and reduce the risk of damage to
reduce flood risk.
surrounding properties.”
An eight-inch butterfly valve was installed to allow the
—Capitol Region Watershed District
system to control water draining to the infiltration pipe.
The system decreased the storage requirement by 226 feet
of pipe, effectively increasing storage volume by 58 percent without changing the project
footprint. The system also measures temperature and infiltration rates to improve stormwater
management during freezing/thawing cycles.
increase in
gallons managed
effective storage
Appendix A: Case Studies A--11
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Falcon Heights, Minnesota
Since deployment in July 2015, the system has successfully collected stormwater runoff from the
watershed and prevented the costly flooding of the surrounding area, which limited park use,
damaged infrastructure, and created public safety concerns. The system also provides real-time and
historical data of site performance. At any time, staff can remotely monitor the system and modify
what is happening. This high-efficiency solution has enabled the Capitol Region Watershed District to
achieve its stormwater management objectives within the constraints of a highly developed
urban/suburban area. It also holds potential for expansion to stormwater facilities throughout
Falcon Heights to effectively manage storms at the local watershed scale.
Appendix A: Case Studies A--12
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
City of Fort Wayne Fort Wayne, Indiana 2015
KEY FEATURES
 Smart use of near-real-time flow/depth data to reduce CSOs.
 Flow data and a hydraulic model used to develop an innovative way to capitalize on the
difference in timing between combined and sanitary flow.
PROJECT DESCRIPTION
Fort Wayne, Indiana, is located at the junction of
the St. Joseph and St. Mary Rivers, which join to
form the Maumee River flowing east through
Ohio to Lake Erie. The city operates a collection
system of both combined and separated sewers
along with a 95 MGD WPCP. The system also
includes two storage ponds along the Maumee
River to store wet weather flow, shown in Figure
1, for later discharge to the WPCP across the
river. Wet weather flows reach the ponds
through two diversion structures, a high-level
passive overflow on the Wayne Street
Storage
Interceptor and a controllable weir in the St. Ponds
Joseph Diversion Structure.
The city’s LTCP, developed pursuant to a consent
decree, called for projects estimated at $240
million (2005 dollars). One LTCP project was a
Figure 1. Map of Fort Wayne’s combined sewer system and
collection of satellite STFs along the St. Joseph
storage ponds.
River in the northern portion of the combined
sewer system. St. Joseph CSOs 45, 51, 52, 53, and 68 were all to be controlled using satellite storage or
treatment facilities.
The city began a system-wide monitoring program over 2 decades ago, and now has a network of over
100 flow meters, 10 depth-only devices, and 29 rain gauges, all of which feed data to the city’s data
management platform. The city uses the data to support daily operational decisions, and to manage
flood control during high river events. These activities use the data in near real time, with managers
viewing the data as needed to support manual adjustments of system control features; managers also
use the data offline to maintain calibration of the city’s hydraulic model.
Appendix A: Case Studies A--13
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Fort Wayne, Indiana
The data have also been used to identify opportunities to refine the LTCP. Early on in the LTCP
implementation process, the flow data from the St. Joseph Diversion Structure revealed that the
downstream CSO response was much faster than the upstream sanitary sewer response and, in many
cases, the CSO response was over by the time the sanitary response reached the downstream end of the
system.
This observation gave city staff the opportunity to reassess the St. Joseph CSO solution. Comprehensive
modeling analyses combined with some innovative design revealed that the city could maximize the
benefit of the St. Joseph Diversion Structure to capture the CSO volume without jeopardizing overall
system performance. By lowering the diversion weir at the beginning of the storm, the hydraulic grade
line in the St. Joseph Diversion Structure drops and its effective capacity increases. That increase in
capacity is sufficient to capture the required CSO volume before the sanitary flow from further upstream
begins to arrive.
The operating strategy today is to lower the weir at the onset of the storm to capture additional CSO
volume in the ponds and raise the weir at the correct time to convey the maximum flow to the WPCP
(see Figure 2). This operation must be managed carefully, as the diversion structure hydraulic grade line
affects performance at several key locations the system. Therefore, proper implementation of this
strategy relies on data feeds from these key locations. Although the majority of this process is controlled
manually, it is operated in near
real time using the city’s data
management system
dashboard.
One of the keys to near-real-
time operation is that the city’s
network of battery-powered
flow meters and depth-only
devices can automatically “shift
gears” from the normal 6-hour
data download frequency to 15
minutes during storm events.
Another is that all sensor
locations can send data directly
to the city’s data management
system without any
intermediary hardware.
The original LTCP for the St.
Figure 2. Hydraulic grade line lowered by the St. Joseph control structure,
Joseph CSO solution called for
allowing more CSO volume to be stored for treatment.
the expenditure of $23.2 million
for storage, disinfection, and
other support components. The smart use of near-real-time flow data has allowed the city to eliminate
the need for 5 satellite facilities and comply with the consent decree requirements at the St. Joseph CSO
outfalls for an expenditure of $5.2 million.
The city’s remaining CSOs are being addressed with a storage tunnel and other facilities, and their
network of smart flow meters will be used to monitor those facilities and ultimately support a future
RTC system.
Appendix A: Case Studies A--14
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
City of Grand Rapids Grand Rapids, Michigan 2015
KEY FEATURES
 RTDSS to help the city with sanitary system separation.
 Data showing that the I/I problem could be solved for $30–$50 million as opposed to the
original $1 billion estimate.
 Sensor network expanded to more parts of the system.
PROJECT DESCRIPTION
Grand Rapids, Michigan, has garnered accolades in the clean water industry for taking significant
proactive steps to improve its sewer system. In the early 1990s, “River City” invested in transforming its
collection system from a combined sewer system to separate storm and sanitary sewers. By moving
from a single pipe for both stormwater and wastewater conveyance to separate pipes, the city avoided
the introduction of sewage into its waterways, reducing overflows and subsequent pollution into the
landmark Grand River that flows to Lake Michigan 40 miles downstream.
After nearly 25 years, Grand Rapids finished retrofitting its CSO system to a separate sanitary and
stormwater system, completing its LTCP in 2015. But now the city needed to better understand the I/I
into these newly separated sanitary sewers to ensure compliance with a mandate from EGLE. This
mandate allowed zero overflow events of any kind, except as part of a wet weather event of a
magnitude in excess of a 24-hour, 25-year storm.
For compliance purposes, the city needed analytic data to certify performance and understand how the
system behaved during a wide variety of wet and dry weather conditions. While gathering this
information, the city was also presented with a hydraulic report stating that areas of the community
were experiencing excessive surcharging and flooding. The city suspected otherwise, but needed proof
to answer regulators: mitigation to eliminate the surcharging and flooding was estimated to cost as
much as $1 billion; a capital expense it could ill afford.
To satisfy regulators, Grand Rapids turned to smart data infrastructure to understand how the separate
sewers behaved, with the goal of modeling the performance in a computer environment to better
predict how the system would perform with less costly improvements to existing infrastructure.
Appendix A: Case Studies A--15
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Grand Rapids, Michigan
First, the city deployed a sensor network of 90 flow meters and 10 rain gauges to collect real-time data
from the sanitary lines. This data was analyzed using an integrated RTDSS, which collected, organized,
analyzed, and served the data via dashboards, giving city operators visual cues to understand and
regulate the operation of their sewer systems (see Figures 1 and 2). Once built, the model was
compared against ongoing sensor data, generating a higher level of system intelligence that is
continuously improving with each wet weather event.
Figure 1. An example of the data collection software, a real-time database and data analytics tool that offers full SCADA
integration.
Upon completion of the investigation through the RTDSS, the city demonstrated to EGLE regulators that,
by focusing on a few critical areas needing improvement, its I/I problem could be solved for $30–$50
million as opposed to the original $1 billion estimate.
Since implementing the
RTDSS solution, Grand Rapids
has achieved the
performance required by the
LTCP and continues working
toward final certification with
EGLE. Encouraged by those
results, it has expanded the
RTDSS sensor network by 70
sensors, many of which are
now delivering real-time data
from the city’s stormwater
network. Over the next few
years, the city will also
embark on a multi-phased
program to improve
sustainability and improve
Figure 2. A Grand Rapids I/I analytics dashboard showing the intensity and
water quality for wildlife and
characterization of their I/I sites.
recreational use in the Grand
River.
Appendix A: Case Studies A--16
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
C ity of Green Bay Green Bay, Wisconsin Fall 2017
KEY FEATURES
 RTC technology using I/I data to prevent sewer spills.
 RTC technology that identifies river level changes to protect bridges from flooding.
PROJECT DESCRIPTION
Since 2016, Green Bay has monitored several manhole locations throughout the city, analyzing the data
for a much better understanding of when and where water infiltrates the system during rain events.
During heavy rainfall, RTC technology monitors and notifies the city of quickly changing water levels.
This monitoring has made it clear that the city would also benefit from information about dynamic
water level changes due to infiltration from rivers.
Therefore, in addition to the units at key
manhole locations, Green Bay deployed
RTC technology to monitor the East River
and Fox River. The data help determine
how upstream flow and river level changes
are affecting downstream flooding in the
sewer and stormwater collection systems.
In particular, the East River system uses an
innovative configuration in which the RTC
unit monitors the water level under the
Mason Street Bridge (see Figure 1). During
significant rainfall events, the bridge-
mounted unit plays an important role in
identifying river level changes.
At one point, the East River registered Figure 1. During heavy rainfall episodes, RTC technology monitors
“high” at 74 inches below the sensor and and notifies the city of rapidly changing water levels at the Mason
just 7 inches below the bridge. Street Bridge.
By monitoring the rapid rise and fall of the East River, combined with data from the Fox River, Green Bay
can correlate river level changes with stormwater infiltration into the collection system. The ability to
aggregate and analyze storm and river data is helping Green Bay more clearly understand the dynamic
relationship between upstream flows and downstream infiltration impacts.
Appendix A: Case Studies A--17
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Green Bay, Wisconsin
This underground visibility provides valuable I/I water surge data when heavy rainfall hits Green Bay (see
Figure 2). Combined with data on quickly rising river levels, the real-time notifications help the city make
decisions about allocation of valuable resources in times of urgency.
Figure 2. I/I detection displayed by the RTC system.
Appendix A: Case Studies A--18
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Hawthorne, California:
Real-Time Monitoring to
Prevent Sewer Overflows
OWNER LOCATION INCEPTION
City of Hawthorne Hawthorne, California 2006
KEY FEATURES
 RTC technology that provides early warning of pre-flow events.
 Sewer overflows reduced by 99 percent.
 Savings estimated at $2 million in fines and mitigation costs since 2006.
PROJECT DESCRIPTION
The City of Hawthorne operates a small gravity-
only sewer system southwest of the Los Angeles
Airport. This system includes 94 miles of gravity
pipeline, no lift stations, no treatment, and just 2
full-time collection staff. Before 2006, Hawthorne
was experiencing about 10 sewer overflows per
year in its sanitary sewer collection system. The
city estimated that these spills cost it $400,000
annually in fines, cleanup and mitigation costs,
and legal costs.
In late 2006, the city positioned 50 real-time
Figure 1. Graph showing a rise in water level, alerting
remote level monitoring sensors covering 66 of
managers to a potential issue.
the “hot spots” in the collection system. These
systems give managers real-time early warning of
pre-flow events using alarms and a data analytics tool, which indicates when pipes begin to accumulate
dirt, grit, FOG, or tree roots, thereby changing the daily pattern of water flow in the pipes (see Figure 1).
Since the installation of the real-time monitoring system, the city has experienced only one overflow in
its sewer collection system, at a previously unmonitored location. This represents a decrease in sewer
overflows of 99 percent. Using its 2-man crew and the RTC technology, Hawthorne has been able to
virtually eliminate sewer overflows in its collection system, saving an estimated $2 million in fines and
mitigation costs since 2006.
Appendix A: Case Studies A--19
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
City of La Mesa La Mesa, California 2018
KEY FEATURES
 10 segments monitored with analytics to determine cleaning frequency.
 Total cleaning reduced by 80 percent with no SSOs.
 Savings of $19,200.
PROJECT DESCRIPTION
La Mesa, located just east of San Diego, employs a highly rigorous cleaning process as part of its
preventative maintenance program. The city maintains 153 miles of sanitary sewer and 53 miles of
storm pipes. Its maintenance routine includes annually cleaning the entire system and cleaning nearly
100 monthly and quarterly scheduled “hot spots.” A small group of field technicians perform the
cleaning, as well as a full range of other tasks to maintain the city’s low SSO track record. The city is
committed to further SSO reduction; however, it is challenged by the rigorous cleaning regimen, often
juggling staff to meet all maintenance needs.
Seeking a better balance, the city questioned whether many of the high-frequency cleaning segments
were being overcleaned and, if reduced, would alleviate maintenance pressures. It lacked data to
answer these questions, though.
The city was introduced to a potential solution with real-time, remote segment monitors. This smart
technology gathered data, provided redundant SSO alarms, and used predictive software to drive
decisions on when to clean based on remote segment-conditions. The city partnered with a supplier and
set up a pilot with the following goals:
 Right-size cleaning frequency based on actual segment conditions.
 Enhanced overflow protection.
The city chose 10 segments being cleaned monthly and deployed depth-only monitors with ultrasonic
depth, pressure depth, and alignment sensors. Monitors were equipped with advanced, cellular LTE-M
communications, important for limiting installation and movement to less than 15 minutes (average).
LTE-M enabled antennae to be installed in the manhole without drilling. Cloud-based software collected
data and provided continuous access via computers, tablets, and mobile devices.
Appendix A: Case Studies A--20
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile La Mesa, California
These systems enabled the city to shift from a schedule-driven process to one driven by segment (site)
condition. Maintenance teams were instructed to clean based on segment conditions as illustrated by
the hydrograph (Figure 1).
Figure 1: One-month hydrograph showing no necessity to clean.
The results in the first six months revealed that the city had indeed been over-cleaning. Using the
schedule-driven process, the 10 segments would have been cleaned 60 times over 6 months. During the
pilot and using the site-condition process with smart monitoring, the city cleaned 12 times—an 80
percent reduction. Moreover, during that time, a developing blockage and potential SSO was detected
and prevented.
A cost analysis demonstrated that this reduction had a significant productivity savings. The cost per
segment cleaned was $400 including such factors as the amortized truck cost, insurance, maintenance,
fuel, tools, and consumables and the fully burdened cost of the 2-person crew. Table 1 compares the
schedule-driven versus segment (site) condition–driven costs and potential savings for the six-month
period.
Table 1. Cost Savings Achieved Through Segment (Site) Condition–Driven Process.
*Equipment, communications, software, installation, training, ongoing field service, warranty
Appendix A: Case Studies A--21
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile La Mesa, California
Outcomes of the process change included the following:
 Productivity savings due to labor reallocation and more work per unit of time. Utilities
challenged by labor availability—e.g., hiring constraints, retirements, staff turnover—can
effectively fill the gap with technology.
 Addition of continuous SSO monitoring has protected against SSOs. While costs cannot be pre-
determined, they would include remediation, regulatory fines, and administration.
 Less use of high-pressure cleaning sprays may extend the asset life by avoiding the deleterious
effects on pipes that such cleaning can have.
 Continuous data acquisition from the collection system has been used for other applications,
like hydraulic model validation.
Smart technology can enable utilities to optimize their cleaning processes by giving visibility to remote
site conditions. The resulting benefits can include increased operations productivity, ongoing SSO
prevention, and reduced wear on pipes. Investments to implement smart technology are shown to
provide payback well within the first year.
Appendix A: Case Studies A--22
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
Lou isville and Jefferson
Louisville, Kentucky 2006
County Metropolitan Sewer District
KEY FEATURES
 More sustainable sewer systems and better quality of receiving waters, thanks to smart use of
RTC technology.
 Maximized conveyance, storage, and treatment capacity, consistently capturing 1 billion gallons
of CSO annually.
 Overall cost savings estimated at $117 million from the original CSO LTCP, a 58 percent
reduction in capital investment.
PROJECT DESCRIPTION
The Louisville and Jefferson County MSD operates and
maintains a complex wastewater and stormwater
system, with more than 3,200 miles of wastewater
collection sewer lines, 16 small and regional WWTPs,
over 280 pump stations, and 790 miles of stream water
quality monitoring as well as the Ohio River Flood
Protection System.
Louisville MSD is one of the nation’s early adopters of
RTC, applying inline storage since the 1990s and
pioneering the application of global, optimal, and
predictive RTC that has been in operation since 2006.
The RTC system was key to maximizing conveyance,
storage (inline and offline; see Figure 1), and treatment
capacity to reduce CSO, with consistent operational
results of more than 1 billion gallons of CSO captured
annually.
Louisville MSD is in the final years of a 19-year
initiative known as the IOAP. The vision of the IOAP is
Figure 1. Staff inspecting one of MSD’s storage
basins. to provide a long-term plan to eliminate SSO and other
unauthorized discharges and to reduce and mitigate
wet weather CSOs in both the combined and separate sewer systems, in an effort to improve water
quality in both Louisville Metro streams and the Ohio River.
Appendix A: Case Studies A--23
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Louisville, Kentucky
MSD has a progressive vision for total wastewater system optimization, which includes the control of
both inline and offline storage facilities, diversion control within and between the combined and
sanitary sewer systems, and maximizing of wastewater treatment throughout the system. RTC is integral
to the fulfillment of this vision. Smart use of RTC technology has allowed MSD to enhance the
sustainability of its sewer systems while also improving the water quality of receiving waterways—
shown in Figure 2, along with MSD’s combined sewer area.
The global, optimal, and predictive RTC approach
was determined as the most appropriate level of
RTC for the Louisville system based on the control
objectives and the system hydraulic
characteristics. The RTC system includes remote
control facilities and a central station. Each
remote site includes sensors (flow, level) and
control elements (e.g., gates, pumps) connected
to a local PLC. This PLC modulates the control
elements based on the rules programmed into it
and setpoints computed by a global DSS.
Information collected in the field is
communicated from the remote stations to the
central station via the SCADA system. The central
station manages and coordinates the various
Figure 2. Map of Louisville MSD’s combined sewer area.
modules, including data management and
archiving, DSS control algorithms, hydrologic and hydraulic models, and weather forecasting.
As conditions are monitored, acknowledged, and controlled, the DSS accounts for the distribution of
flow in the entire system, both under current conditions and in the future, based on rain forecasts,
measurements, and sewer simulations in real time. The RTC system allows continuous and strategic
adjustment of control devices to optimize flow conveyance, storage, release, and transfer according to
the available capacity in the entire system.
RTC feasibility studies of phase 1 implementation showed that optimizing the existing collection and
treatment system would have a relatively low unit cost, ranging from $0.006 to $0.021 per gallon of CSO
reduction per year. This cost is 4 to 10 times lower than that of the traditional approach (building more
storage). The overall savings was estimated at $117 million from the original CSO LTCP cost of $200
million (a 58 percent reduction in capital investment).
The RTC technology is scalable and flexible. The global, optimal, and predictive RTC system involves all
levels of control—from static to local to global—to provide system-wide optimization. New control sites
were added to the RTC system as the facilities were being built. Moreover, control logics can be
modified based on performance monitoring as part of adaptive management. The use of an online
model reduces the number of sites and extent of the monitoring network required for system-wide
optimization.
The RTC approach did present several challenges:
 It relies on online model and weather forecasting to predict upcoming inflows and their spatial
distribution. This requires the calibration and updating of the hydrologic and hydraulic model to
represent the wastewater system adequately.
 The control strategy and decisions need to account for inaccuracy and unpredictability in
weather forecasting.
Appendix A: Case Studies A--24
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Louisville, Kentucky
Lessons learned from this project include the following:
 The adoption of RTC technology requires organizational commitment and staff buy-in.
 The utility needs to consider O&M issues and constraints when choosing the appropriate level of
RTC implementation.
 It is important to involve system operators early in planning and design, and to identify and
communicate roles and responsibilities at every stage, from design, construction, and
commissioning to post-construction performance monitoring.
 Documentation such as standard operation procedures and post-event analysis is critical in
properly operating, maintaining, and improving an RTC system.
The MSD RTC program’s cost is estimated at $21 million,
including retrofit, construction, monitoring, IT, etc. The current “[RTC] is an important component
RTC system includes 2 stormwater retention basins (over 30 of MSD's long-term plan to
MG) for CSO control, multiple inline storages, flow diversions,
mitigate untreated [CSOs] into
and pump stations, as well as the management of the
Beargrass Creek and the Ohio
southwestern outfall, an egg-shaped tunnel with a diameter
River. It is a cost-effective
ranging from 24 to 27 feet.
management strategy to help
MSD continues to improve and expand its RTC system as new
sustain the resources of our
STFs are constructed under the IOAP.
community.”
MSD has developed web-based training modules on the RTC
system and used them for continuous training and knowledge —Angela Akridge
transfer. Control site commissioning and startup provide onsite Chief Engineer, Louisville MSD
training opportunities for instrumentation and control and
O&M staff.
Appendix A: Case Studies A--25
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
C ity of Newburgh Newburgh, New York October 2016
KEY FEATURES
 Easier, more reliable, more nimble operations.
 Less risk of loss or damage to sensors.
 Lower cost.
PROJECT DESCRIPTION
The City of Newburgh replaced its traditional telemetry system with smart controls, both to give city
staff and the public real-time notification of CSO events (see Figure 1) and to prepare for increased
regulatory requirements for annual reporting and notification. The city spent around $78,000 for 18
units.
The city’s prior telemetry system used pressure sensors that had to be at the bottom of the influent
channel, in direct contact with the flow, and in the combined sewer regulator environment. In these
locations, the sensors were regularly damaged or displaced by debris. Many times, under high flow
conditions, several entire units were swept away down the CSO and lost at the outfall.
The prior sensors also needed expensive calibration equipment and a proprietary consultant to perform
the annual calibration of the telemetry system at each installation location. The old telemetry system
used a dedicated phone line for each telemetry station, with only a single point of access and control (at
the WWTP). These hard lines were expensive, had regular loss of communication, and were very difficult
or impossible for the utility company to find when they needed service.
The new telemetry system resolved all of these problems. The smart control wireless satellite
connectivity proved more reliable than land phone lines and cost less. Any computer, tablet, or
smartphone with internet access can communicate with the telemetry system. Little calibration is
needed; when a sensor does need to be calibrated or moved, in-house staff can easily do so with basic
tools. The sensors are not in contact with the water, so they avoid damage.
Appendix A: Case Studies A--26
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Newburgh, New York
Figure 1. The new system monitors water level above the bottom of the pipe and allows the city to automatically and
accurately monitor and report CSO events. Significant rainfall generated stormwater peaks above the red dotted line,
which indicates CSO events.
The new sensors are generally installed hanging from the manhole cover above. At some installation
locations, some initial erroneous readings resulted in the discovery that, in some locations within the
sewer, plugs of air can cause the sensors to swing. At these locations, a restrained installation of the
sensor is needed. This has been accomplished in-house with stainless steel angle brackets and
associated hardware.
In some sites, initial erroneous readings were caused by low flows with a large distance from the
influent channel to the sensor above. This challenge was overcome with the installation of replacement
long-range sensors.
Appendix A: Case Studies A--27
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
Cit y of Ormond Beach Ormond Beach, Florida February 2017
KEY FEATURES
 RTC used to convert 70 acre-feet of dead storage into flood management capacity for pre-event
drawdown.
 Optimizations to the pump system that mitigated the need for an $8 million upgrade.
 Lakes prevented from reaching flood elevation during 2017’s Hurricane Irma.
 Actionable insights for emergency response personnel, improving community resilience.
PROJECT DESCRIPTION
A 2009 storm caused excessive flooding
and property damage in Ormond Beach.
About 79 structures were affected, and
flooding made roads impassable
throughout the city’s Laurel Creek
drainage basin area. With help from the
Federal Emergency Management Agency
and in coordination with various city
departments, an upgrade project was
undertaken to address not only the
flooding issues but provide the ability to
upgrade utilities within the area, enhance
park elements, and bring existing
roadways up to current city standards.
To further minimize the risk of flooding,
the city implemented the Laurel Creek Figure 1. The Laurel Creek Pump Station is located at an
Pump Station Additions and interconnected lake system that provides flood control for the area.
Improvements project, which was
approved under its Capital Improvements Program. The stormwater pump station is located at an
interconnected lake system (comprised of five lakes) and provides flood control for the area (see Figure
1).
As part of this effort to maximize the flood storage potential of the lakes, the city deployed weather-
forecast-based CMAC technology. Specifically, CMAC controls two VFD pumps to discharge water from
the lakes in advance of a weather event, creating additional storage capacity. A cloud-based software
platform collects data from the local weather forecast, four solar-powered water level monitoring
Appendix A: Case Studies A--28
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Ormond Beach, Florida
stations, and the VFD pumps. Data are processed in real-time, and the cloud platform automatically
sends commands via a cellular network to set VFD discharge rates.
The interconnected lake system receives runoff from a 7,680-acre watershed and has a total storage
capacity of 250 acre-feet. In preparation for Hurricane Irma, the city used CMAC to discharge about 70
acre-feet of storage from the lake system. Even with the tremendous performance of the lakes’ new
pump system, there was a total storage increase of 190 acre-feet after pre-event drawdown (see Figure
2). Given that local flooding occurs at a storage volume of 250 acre-feet, the pre-event drawdown
prevented flooding of nearby roads and property. Without pre-event drawdown, the lake elevation
would have exceeded the flood stage of 5 feet (i.e., a volume of 250 acre-feet). Continuous monitoring
before, during, and after Irma’s eight-inch rainfall on this basin was also an integral part of the city’s
emergency operations and further enhanced infrastructure management.
The city estimated that it would have cost $8 million to eliminate flooding by increasing pump capacity
with additional pump stations. Instead, the city reduced localized flooding within one year for $200,000
by optimizing its existing system.
Figure 2. Laurel Creek Pump Station Additions and Improvements project performance during
Hurricane Irma.
Appendix A: Case Studies A--29
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
Philadelphia Water Department Philadelphia, Pennsylvania 2016
KEY FEATURES
 Retrofit of an existing SMP with active control technology to increase treatment and reduce wet
weather flows.
 Minimization of wet weather discharge for storms up to two inches in rainfall depth.
 Integrated system monitoring and reporting capabilities.
PROJECT DESCRIPTION
An existing SMP collecting runoff from eight acres on private property in the combined sewer area was
not meeting PWD’s stormwater management standards. For all areas served by a combined sewer and
for which infiltration is infeasible, 100 percent of the runoff from 1.5 inches of rainfall must be routed
through an acceptable pollutant-reducing practice and detained in each SMP for no more than 72 hours.
Any runoff detained must also be released from
the site at a maximum rate of 0.05 cfs per
impervious acre. The existing pond was originally
designed as an infiltration basin but does not
achieve sufficient infiltration because of errors in
the construction process.
A PWD Stormwater Management Incentives
Program grant was awarded to fund a facility
retrofit to increase treatment and further reduce
wet weather flows. The SMP enhancement was
achieved through the installation of CMAC on the
existing outlet control structure of the basin (see
Figure 1). The system includes a level sensor,
actuated valve, and integrated software that will
Figure 1. CMAC installation on the existing outlet control
provide dynamic control of stormwater storage and
structure.
discharge above the permanent pool of water in
the existing basin.
The stormwater pond contains a permanent pool of 22,500 cubic feet maintained by an outlet structure
with a 6-inch orifice. A second, eight-inch orifice is positioned about two feet above the invert of the six-
inch orifice and an overflow weir is about two feet above the eight-inch orifice. The retrofit involved
installing a six-inch actuated valve on the six-inch orifice, a water level sensor, and the associated
Appendix A: Case Studies A--30
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Philadelphia, Pennsylvania
communications hardware to connect these to cloud-based control software. The software uses the
water level data along with National Oceanic and Atmospheric Administration storm forecasts to
determine an optimal valve open percentage based on water quality, storm retention, and flood
protection objectives. For this basin, the software was configured to achieve the following logic:
 When a forecasted storm can be fully captured within the basin storage between the permanent
pool and the eight-inch orifice, close the six-inch valve to eliminate wet weather flow.
 After the event, open the valve to release the captured runoff within the 72-hour retention
period without exceeding a discharge rate of 0.26 cfs (0.05 cfs per impervious acre).
 When the forecast indicates that an upcoming storm cannot be fully captured, release water at
the lowest possible rate to avoid overflowing the riser structure. This logic ensures that the 0.26
cfs target is only exceeded during large events to mitigate high water levels and discharge rates.
Post-event, release any captured storm runoff within the 72-hour retention period without
exceeding the 0.26 cfs target.
The storage volume available above the current permanent pool of water and below the invert of the 8-
inch orifice is 38,000 cubic feet. This volume is larger than the runoff generated by the 2-inch storm
event (34,000 cubic feet). Therefore, for all rainfall events up to two inches, the CMAC basin is able to
fully capture the runoff with no discharge to the combined sewer during the wet weather event. After
the event, the valve will slowly but continuously adjust (i.e., open further as the driving head drops) to
match the target 0.26 cfs rate until the basin returns to its permanent pool elevation.
In addition to meeting the requirements for stormwater retention credits, the retrofit facility still
provides safe passage for larger events. The pond depth and outlet structure configuration were not
changed from the existing conditions. When the system is fully functioning, the software logic will open
the valve as far as is needed to avoid overtopping the outlet structure, up to fully open for very large
events. When the valve is fully open, the retrofit and existing conditions peak flow and maximum water
surface elevations are identical. If the CMAC system fails to function properly and the 6-inch valve is
closed during a large event, modeling shows that the 100-year event is still safely contained within the
basin and will not contribute to local flooding. The CMAC system includes failsafe features that protect
the infrastructure in the event of connectivity or physical hardware failures. The retrofit was installed in
November 2016 and has been collecting hydraulic data while adaptively managing the pond discharge.
Figures 2 and 3 illustrate how the pond’s volume and flows after a wet weather event are managed with
passive outlet control compared to CMAC.
Appendix A: Case Studies A--31
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Philadelphia, Pennsylvania
Figure 2. Modeled pond volume and flows with passive outlet control.
Figure 3. Observed pond volume and flows with CMAC.
Appendix A: Case Studies A--32
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
City of Rutland Rutland, Vermont July 2017
KEY FEATURES
 RTC solutions helped the city meet state public notification requirements.
 Easy for non-technical users to visualize the data.
PROJECT DESCRIPTION
Rutland, Vermont, is a small city of about 16,500 residents. It operates a combined sewer system, some
of whose sections are more than 100 years old. In the past, the city relied on measuring techniques that
involved field crews and site visits, such as reading height markers from a wooden stick, to periodically
sample levels in its wastewater system. Although this fulfilled its basic reporting obligations, it clearly
did not provide real-time information. It also necessitated frequent field visits, and—being a non-digital
method—could not connect with interfaces such as the city’s SCADA system. It did not provide the
means to predict the development of a CSO, nor could it alert operators to one that was already in
progress.
Remedial and proactive engineering work could only be planned on the basis of modeling efforts
predicated upon the accuracy of data taken from indirect estimates of water flows. The lack of
information from the furthest portions of the collection system from the treatment plant also greatly
impeded the city’s efforts to address the root problems, inherent in its system design, that were causing
the CSOs to happen.
In 2016, the Vermont state legislature enacted law that requires operators to notify the public of
overflow events within an hour of discovery. The city saw in the legislation an opportunity to proactively
increase the transparency of local government and provide up-to-date information about wastewater
management issues to citizens. To comply with the legislation and deliver its planned citizen information
initiative, the city realized that it needed to develop an affordable system that could provide real-time
level data to its regulators, its customers, and engineers. To this end, the city embarked on a public
information initiative that included setting up social media to inform customers of wastewater events
including overflows. This provided a user-friendly alternative to the municipality’s website.
The city piloted several RTC solutions before choosing a product, in February 2019. Non-technical users
could quickly learn how to visualize field data using the web-based data hub. Engineers could integrate
the real-time data feed directly into the city’s SCADA monitoring and control platform quickly. Members
of the public could subscribe to receive live updates about overflows from familiar social platforms.
Appendix A: Case Studies A--33
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Rutland, Vermont
An additional benefit of the city’s RTC solution has been the ability to help draft a hydrologic and
hydraulic study, which the city is undertaking to improve the performance of its wastewater network
over the long term. Consultants are working with the city to draft a plan that will use the RTC devices to
capture extensive data from the field. When complete, the plan will give network operators the ability
to accurately predict the development of CSO events. In addition, it will enable the city to undertake a
cost-benefit analysis to determine what mix of green infrastructure (aboveground water interception
devices), gray infrastructure (underground retention measures), and data infrastructure (flexible state
underground devices, such as inflatable weirs, operated based on cues from smart sensors) will yield the
best long-term results for minimizing CSO events. As Figure 1 shows, the city is already gathering data
on how much Otter Creek backflows into the combined sewer system.
Figure 1. The city uses multiple level sensors to monitor how much Otter Creek backflows into the combined sewer
system.
The strategies that the city will put into action, based upon the hydrologic and hydraulic study and the
data derived from the RTC installation project, will greatly help it remain compliant with the terms of the
Chapter 10 Vermont Statutes Annotated Section 1272 Order (“Regulation of activities causing discharge
or affecting significant wetlands”). The order sets out guidance plans for operators who do not currently
comply with best practice management guidelines to reduce their overflow rates.
In 2019, total CSO volume for 29 storms was 26.8 MG, with an average duration per event of 3 hours
and 21 minutes. The data from the field assets showed that more than 70 percent of the overflows
occurred between April and November 2019. The highest recorded discharge was 2.5 cfs, which was
reached 10 times during 2019. The city is using the data collected from the monitoring equipment to
identify cost-effective collection system modifications it can implement as part of its LTCP. The RTC
system has given the city an alternative, convenient way to affordably revolutionize the operation of its
network without needing to physically change it.
Appendix A: Case Studies A--34
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
San Antonio Water System San Antonio Water System Fall 2017
KEY FEATURES
 1,246 anticipated cleanings reduced to 65 actual cleanings.
 95 percent reduction in cleaning frequency at 200 sites.
 No spills.
 Certification of 216 SSO “saves.”
 Annual average return on investment of 115 percent.
PROJECT DESCRIPTION
From 2013 to 2015, SAWS tackled an EPA consent decree with an estimated cost of $1 billion. SAWS
adopted EPA’s CMOM guidelines and instituted high-frequency cleaning for its 110,000 manholes and
pipeline segments. Effectively, this meant SAWS established a program of cleaning “high-risk” pipes with
potential for overflows and instituted routine cleanings at monthly, bi-monthly, quarterly, semi-annual,
and annual frequencies.
To help reduce overflows and mitigate the disadvantages of high-frequency cleaning, SAWS
implemented a smart sewer pilot project at 10 monthly cleaning locations from summer 2015 to
summer 2016. The pilot used remote sensors that automatically scan water level patterns and issue
notification when high levels are detected upstream or downstream from the monitored location. The
technology system provides real-time continuous monitoring and trend analysis, allowing SAWS to use
data to determine where and when to clean a sewer pipe segment rather than using a predetermined
cleaning schedule. The pilot resulted in a 94 percent reduction in cleaning (see Figure 1) and an
estimated $4,000 in savings per monitored location.
Appendix A: Case Studies A--35
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile San Antonio, Texas
Figure 1. Cleanings avoided with smart data.
In fall 2017, after the success of the pilot program, SAWS deployed another 200 remote monitoring
sensors at high-risk sites for regular monthly cleanings. As a conscientious sewer operator, it planned to
clean whether the pipes needed cleaning or not. SAWS anticipated nearly 1,300 cleanings at these
locations—but with the analysis and the notification system, it ended up needing to clean only 65 sites.
SAWS has experienced a 95 percent reduction in cleaning, no SSOs, and a certified 216 SSO “saves,” as
shown in Figure 2.
Over time, there has been a distinctive paradigm shift from “We always clean this spot just in case” to
relying on smart data for more efficient “as-needed” cleaning.
For SAWS, the use of smart data
continues to lower cleaning
costs while preventing SSOs.
And, with its smart sewer
solution, SAWS has witnessed
fast payoff and excellent return
on investment, solved old
problems with new technology,
extended underground asset
lifetime, eased stress on staff,
protected lives in the field with
no confined space entry,
created staff availability for
other tasks, lowered pressure
on user rates, and significantly Figure 2. Spills saved using smart data between 2009 and 2019.
decreased operational liabilities.
Appendix A: Case Studies A--36
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
City of San Diego, Stormwater Division City of San Diego 2016
KEY FEATURES
 Optimized sto rmwater/wastewater m anagement using R TC a nd adaptive l ogic.
 Cost savings from program coordination.
 Magnitude of water supply augmentation.
 Water quality benefits.
PROJECT DESCRIPTION
Starting in 2011, California experienced a historic drought, with much of the state reaching D4
“exceptional” conditions on the U.S. Drought Monitor. In response, Governor Jerry Brown declared a
state of emergency in January 2014 and established the first statewide mandatory water restrictions in
March 2015. More recently, significant investments in green infrastructure are needed to address water
quality impairments throughout southern California. Despite the apparent synergy, urban stormwater is
still underutilized as a water resource in coastal areas and is often conveyed directly to the ocean
without beneficial uses. Synergy between drought resiliency planning and water quality protection could
be realized if green infrastructure could be optimized to collect, treat, and distribute urban runoff as a
supplemental, local water source.
This work explored and quantified the potential nexus between an emerging stormwater capture
program and ongoing efforts to reclaim wastewater as a drinking water resource in San Diego (see
Figure 1), which currently imports over 80 percent of its water supply. The project considered both (1)
the need to pursue water independence in response to prolonged droughts, rising imported water costs,
and the city’s growing population and (2) the need to plan, construct, and maintain extensive green
infrastructure to comply with water quality regulations and flooding issues. As such, it provided valuable
data on technological approaches to bolster San Diego’s water resiliency while reducing pollution,
flooding, spending, and redundancy.
The analysis first defined treatment plant boundary conditions to determine what additional hydraulic
and mass loading (from stormwater) the expanding water reclamation program could accommodate.
The team used a calibrated watershed model to predict the loading to the plant from raw stormwater
and from effluent from the green infrastructure that would be built to address water quality regulations.
The team then assessed the cost-effectiveness of methods to convey stormwater to the plant, including
using the existing sanitary collection infrastructure and implementing a separate storm drain
conveyance. Finally, they assessed upstream stormwater control measures—equipped with RTCs—to
optimize the management of stormwater storage and release to the reclaimed water system. The model
included various scales of green infrastructure within the two major sewershed areas served by two
Appendix A: Case Studies A--37
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile San Diego, California
existing pump plants. The resulting integrated water management analysis synthesized the benefits,
costs, and energy demands of various alternatives to inform data-driven decision-making for
municipalities with simultaneous water, wastewater, and stormwater stressors.
Analysis of the coordinated approach to water management hinged on simulating the capabilities of
RTCs operated by cloud-based adaptive logic for intelligently managing storage and conveyance of water
throughout the collection network (i.e., to reduce stormwater overflow to receiving waters while
regulating diverted flow not to exceed the capacity of the treatment plant). This was accomplished using
a software package to simulate optimization of control setpoints throughout the sewer network. The
software identifies when valves, gates, and pumps should be operated to manage overall system
performance in response to forecasted runoff and treatment plant capacity. It is well suited to an
application where flows and storage must be actively controlled to enforce certain constraints and
multiple objectives must be optimized over a long-term simulation. The analysis demonstrated potential
cost savings and co-funding opportunities, as well as solutions to create resilient, low-impact
communities. The simulations suggested that stormwater harvesting (enabled by RTCs) could
substantially augment local water supplies while complying with stormwater quality regulations.
Figure 1. Graphic showing the potential nexus between an emerging stormwater capture program and ongoing efforts to
reclaim wastewater as a drinking water resource in San Diego.
Appendix A: Case Studies A--38
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
San Francisco Public Utilities Commission San Francisco, California 2017
KEY FEATURES
 Two-dimensional module that helps characterize the sewer system performance.
 Easy-to-program, easy-to-understand RTC system.
 Less time required for data management and conflict resolution and higher productivity.
PROJECT DESCRIPTION
San Francisco is home to about 880,000 residents and uses a combined sewer system to collect and
treat sanitary and stormwater flows. SFPUC owns and operates close to 1,000 miles of sewer mains, 3
treatment facilities, 200 MG of storage, 26 pump stations, and 36 CSO outfalls.
Developing a numerical model for San Francisco’s combined sewer system came with several
overarching challenges:
 Detailed representation of sanitary and stormwater flows through a large and complex
collection network.
 Characterization of overland flow transport through the city’s challenging topography.
 Accurate depiction of passive and active control structures’ operation.
 Multiple engineers working concurrently to solve the same problem.
To help address these challenges, SFPUC chose a numerical model that has shown remarkable
performance in three key areas:
 A two-dimensional module.
 RTC logic.
 Multi-processing capabilities.
The city’s combined sewer system is designed to collect and convey flows for a design storm. In extreme
storm events, excess stormwater flows may not enter the sewer system and combined sewer flows may
exit the sewer system at some locations. In flat topographies, these overland flows might pond in the
area until the system regains capacity. However, with San Francisco’s famous topography—steep hills,
low valleys, and low-lying flat areas—the overland flows often pass over the street surface and either
enter back into the sewer system or pond at other low-lying locations. The location where the overland
flows originate and the eventual location of re-entry into the system or ponding can be very different.
The two-dimensional module in the city’s integrated catchment modeling makes it possible to generate
a surface mesh using ground surface elevation data. In extreme storms, when there are overland flows
Appendix A: Case Studies A--39
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile San Francisco, California
on the ground, the city’s integrated catchment modeling enables the two-dimensional module and
routes the overland flows by solving the surface flow transport equations for each mesh element.
Allowing the model to mimic the transport of
overland flows is extremely helpful to characterize
the performance of the sewer system (see Figure
1). The ability to visualize the fate and transport of
overland flows with increasing accuracy has given
the planners and engineers higher confidence in
the model and its use in sewer infrastructure
projects.
Many of the treatment facilities, pump stations,
and CSO outfalls convey and treat the flows
differently during dry and wet weather.
Additionally, during wet weather the operation of
some facilities varies depending on the amount of
rainfall and the combined sewer flows in the
system.
The RTC module allows programming different
types of pump stations, gate structures, and valve
structures. It also allows programming the set-
points for the operation of these facilities. The RTC
logic is easy to program and understand and Figure 1. Overland flows transported on the ground
allows a much better representation for simulating surface, as shown in the two-dimensional module.
the different treatment pathways (i.e., secondary
versus primary treatment facility versus CSO outfall) for any storm event.
Several engineers from different locations work on the model, often working to solve the same problem
concurrently. The workgroup-based databases and configuration management system have enabled
them to work together seamlessly to update the model, develop scenarios for analysis, and generate
results using the same network. This has decreased the time needed for database management and
conflict resolution and raised team productivity.
Appendix A: Case Studies A--40
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
South Bend Department of Public Works South Bend, Indiana 2008
KEY FEATURES
 Illicit dry weather overflows eliminated; total CSO volume reduced by about 70 percent (about 1
billion gallons per year).
 Potential cost of the city’s LTCP reduced by an estimated $500 million.
 O&M costs reduced by $1.5 million.
 More than 50 percent decrease in E. coli concentration (from the sewer system) in the Saint
Joseph River.
PROJECT DESCRIPTION
Before 2008, South Bend had one of the largest CSO discharge volumes per capita in the Great Lakes
watershed. With a population of a little over 100,000, South Bend generated annual CSO discharge
volumes of 1–2 billion gallons and 25–30 dry weather overflows per year. Had the city implemented the
prescribed projects in its LTCP, the cost of mitigating its CSO problem would have totaled roughly $800
million.
In 2008, the city commissioned a real-time monitoring system of more than 120 sensor locations
throughout the city. In 2012, after reviewing data from the system and choosing sites accordingly, the
city launched a distributed, global, optimal RTC system. The RTC system consists of nine auxiliary
throttle lines with valves governed by an agent-based optimization strategy. Distributed computing
agents trade available conveyance capacity in real time, similar to a commodities market.
The system provides information to staff throughout the organization through SCADA screens for the
operators, smartphones and tablets for field staff, and customized websites jointly developed with the
city’s engineering staff. Operations staff can override automated controls and take over valve and gate
operation at any time.
Since 2012, the city has added additional sensor locations and rain gauges, bringing the total number of
sites to 152. It also added automated gates at several stormwater retention basins to better control the
timing and rate of stormwater releases into the combined system.
Appendix A: Case Studies A--41
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile South Bend, Indiana
Maximizing conveyance capacity utilization throughout the Saint Joseph interceptor line was the original
objective of the RTDSS. From 2008 through 2014, South Bend eliminated illicit dry weather overflows in
the first 12 months and subsequently reduced its total CSO volume by about 1 billion gallons per year,
about 70 percent (see Figure 1). The city estimates the program will reduce the cost of the LTCP by $500
million, 63 percent less than the original $800 million estimate; it has already surpassed its original
target of a 25 percent reduction in CSOs. E. coli concentrations in the Saint Joseph River have dropped
by more than 50 percent on average. Overall, this intelligent program allowed South Bend to reduce
costly traditional gray infrastructure, while improving system performance and capacity utilization,
delivering environmental gains 10 to 15 years ahead of schedule.
Figure 1. From 2008 through 2014, South Bend eliminated illicit dry weather overflows in the first 12 months and
subsequently reduced its total CSO volume by about 1 billion gallons per year, about 70 percent.
Appendix A: Case Studies A--42
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
U.S. Environmental Protection Agency Washington, D.C. 2014
KEY FEATURES
 RTCs that retain water for onsite irrigation and reduce wet weather discharge to the combined
sewer.
 100 percent of all 1-inch (and smaller) rain events captured, preventing about 100,000 gallons of
wet weather flow from entering the combined sewer each year.
PROJECT DESCRIPTION
EPA and the General Services Administration sought to upgrade an existing 6,000-gallon rainwater
harvesting system at EPA headquarters in Washington, D.C. Two competing priorities needed to be
addressed: minimizing wet weather discharge and maintaining water availability for irrigation on site.
Uncaptured wet weather flows contributed to the local combined sewer system, increasing the
potential for CSOs and poor water quality in the Chesapeake Bay.
To monitor storage volumes and expected
storage needs based on weather, the
rainwater harvesting system was retrofitted
with a CMAC technology. The cloud-based
platform automatically monitors the weather
forecast and calculates expected runoff
volume from future storms. The system then
automatically opens the discharge valve in
advance of the storm and releases a predicted
volume equal to the potential runoff. As the
forecast changes, the system adjusts
intelligently. Before the storm begins the
Figure 1. The rainwater harvesting system at EPA Headquarters
prevents about 100,000 gallons of wet weather flow from
system closes the valve, capturing rain to refill
entering the combined sewer each year.
the cistern. The valve stays closed until
another rain event is in the forecast, ensuring
that water is available for reuse.
A one-inch solenoid valve was installed to allow the CMAC technology to control water draining to the
combined sewer system. The CMAC technology also monitors discharge flow, irrigation flow, and air
temperature and activates a freeze protection system during cold weather. The addition of CMAC
technology to the existing rainwater harvesting system eliminated the need to install additional storage
volume to meet otherwise competing objectives.
Appendix A: Case Studies A--43
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Washington, D.C.
Since deployment in 2014, the advanced rainwater harvesting system at EPA headquarters has proven
to be a low-cost, high-performance solution for meeting stormwater management goals (see Figure 1).
The increased data transparency and opportunities for adaptive management can achieve a range of
stormwater management objectives. Figure 2 shows how cistern levels are clearly presented to the user
for easy storage volume management.
Figure 2. Cistern levels shown in the user interface.
Appendix A: Case Studies A--44
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

OWNER LOCATION INCEPTION
City of Wilmington Wilmington, Delaware 2011
KEY FEATURES
 Anticipated increase of Wilmington’s average annual wet weather capture from 50 percent to more
than 85 percent.
 Overall cost savings estimated at $87 million from the original CSO-LTCP.
 Fully automated operation, with remote supervision and manual override capacity at all times by
treatment plant operators.
PROJECT DESCRIPTION
Since the early 1990s, the city of
Wilmington has initiated a series of
improvement projects to reduce CSO
events and increase the annual average
flow intercepted at the WWTP. These
projects included the upgrade of
treatment plant capacity, the
construction of the 2.7 MG Canby Park
CSO Storage Basin (see Figure 1), the
elimination of certain CSOs, other
specific collection system
improvements, and public outreach.
As part of its ELTCP, Wilmington
implemented a coordinated system-
wide RTC solution. The RTC system
provides efficient flow management to
Figure 1. The 2.7 MG Canby Park CSO Storage Basin under construction.
reduce CSOs along the Brandywine
Creek and the Christina River and
optimizes the capacity available in the interceptor and pump stations. Overall, the ELTCP will increase the
average annual percent capture from 50 percent to more than 85 percent, meeting the CSO control
objective via the presumption approach. Wilmington’s green infrastructure program is expected to meet
the total maximum daily load objectives by increasing the wet weather capture rate to over 90 percent.
The city adopted an adaptive management approach whereby site-specific system improvement, such as
localized separation and additional green infrastructure, will be determined based on post-construction
performance of implemented projects.
Appendix A: Case Studies A--45
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Wilmington, Delaware
The RTC project encompasses the design, retrofitting, and implementation of four flow control stations,
the control of Canby Park CSO Storage Basin, the control of the three existing siphons, and the design
and implementation of a network of data collection and measuring sites for monitoring purposes. All of
the local stations are linked to the central station via a telemetry system and automatically managed
under a global, optimal, and predictive RTC approach from the central station (see Figure 2), under the
supervision of operators. Smart use of RTC technology has allowed the City of Wilmington to significantly
reduce overall costs of the LTCP.
Figure 2. Process flow diagram for the Canby Park CSO Storage Basin.
The RTC system is fully automated, giving treatment plant operators with remote supervision and
manual override capacity at all times.
The system has four major components:
 A monitoring system including level, flow, and rainfall.
 Local control facilities equipped with control elements (gate and pumps), PLCs, and remote
telemetry units with backup power.
 A SCADA system for data acquisition of sensor information and control facility status, as well as
for communication of control set points.
 A central station that manages and coordinates the various components, including data
management and archiving, RTC control algorithms and optimization, hydrologic and hydraulic
models, and weather forecasting.
As conditions are monitored, acknowledged, and controlled, Wilmington’s RTC system accounts for
current and future flow distribution throughout the system based on rain forecasts, measurements, and
sewer simulations in real time. It provides continuous and strategic adjustment of control devices to
optimize flow conveyance, storage, release, and transfer according to the available capacity in the entire
system.
RTC feasibility studies showed that optimizing the existing collection and treatment system would have a
relatively low unit cost, $0.07 per gallon of CSO reduction per year. This cost is four times lower than that
Appendix A: Case Studies A--46
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Wilmington, Delaware
of the traditional approach (building more storage). The overall savings is estimated at $87 million from
the original CSO LTCP cost of $114 million, for a final LTCP cost of $27 million.
The RTC technology is scalable and flexible and involves all levels of control—from static to local to
global—to provide system-wide optimization. New control sites can be added and control logics modified
based on performance monitoring as part of adaptive management.
The RTC system design and operation accounts for equipment and sensor failures and provides failsafe
control for a robust performance system in real time.
The RTC approach enables the system to meet multiple objectives in a predefined priority order: (1) flood
protection, (2) CSO minimization with local priorities, (3) minimal retention time with local priority order,
and (4) minimal gate movements.
The use of an online model reduces the number of sites and the extent of the monitoring network
required for system-wide optimization. The RTC system gives the city a greatly enhanced capability to
monitor, analyze, assess, and report on CSO discharges and collection system performance (capture rate)
on an annual basis. This has been useful for reporting to the regulating agencies and for integrating
adaptive management into LTCP planning.
The RTC approach did present several challenges:
 It relies on an online model and real-time rain gauges to predict upcoming inflows and their
spatial distribution. This requires the calibration and updating of the hydrologic and hydraulic
model to represent the wastewater system adequately.
 The control strategy and decisions need to account for inaccuracy in rainfall distributions and
real-time monitoring data.
The lessons learned from this project include the following:
 The adoption of RTC technology requires organizational commitment and staff buy-in.
 The utility needs to consider O&M issues and
constraints when choosing the appropriate level “We’d have to tear up several parks in the
of RTC implementation. city to build more tanks, I’m not a
 It is important to involve system operators early scientist, but we knew there had to be
in planning and design and to identify and ways to divert the way water flows in
communicate roles and responsibilities at every pipes. We are among the selected
stage, from design, construction, and
communities that have utilized [RTC] that
commissioning to post-construction performance
makes optimum use of our sewer capacity
monitoring.
to manage and minimize overflows. This
 Documentation such as standard operation
plan is cheaper, quicker and actually
procedures and post-event analysis is critical in
properly operating, maintaining, and improving
increases the amount of overflow we are
an RTC system. trying to catch. The Enhanced LTCP would
 Achievement of the anticipated performance was increase the CSO capture and treatment
delayed until initially unidentified system rate to 87% or higher, reduce CSO control
collection anomalies were resolved. These costs by more than $87 million and
included pipes obstructed with up to 50 percent accelerate implementation by ten years.”
sedimentation or root blockages, as well as pump
station control logic that deviated from the —Mayor James M. Baker,
reported operational condition. City of Wilmington, Delaware
Appendix A: Case Studies A--47
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.

Project Profile Wilmington, Delaware
 Key to the project has been the City of Wilmington and its designated operator taking ownership
of the instrumentation and control and SCADA system to maintain equipment and
instrumentation in a proactive manner.
The project cost $12 million, including retrofit, construction, monitoring, IT, etc. The current RTC system
includes the use of 1 retention basin (2.7 MG) for CSO control, an additional 2 MG of inline storage, the
management of 3 siphons, and the operation of a 135 MGD pumping station.
Appendix A: Case Studies A--48
Any mention of trade names or commercial products does not constitute an endorsement or
recommendation for use. EPA and its employees do not endorse any products, services or enterprises.