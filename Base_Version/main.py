from MOEMS import ModelParameters 
import numpy as np

import os
ipopt_path=os.getcwd() #change it to the path of the ipopt solver depending on your system
os.environ['PATH'] = ipopt_path + os.pathsep + os.environ['PATH']
###example for a grid optimizing to 10 time intervals with 15 minutes resolution

#time parameters
Time_Resolution=15   #minutes
n_Time_intervals=10

#static load predection in W >> it does not matter for shape of the list/array but it should be a list/array of lists/arrays with shape of (n_Time_intervals, n_loads) or (n_loads, n_Time_intervals)
Load_P=[[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1],[1,1]]
Load_P=np.transpose(Load_P)

#PV predections in W>> it does not matter for shape of the list/array but it should be a list/array of lists/arrays with shape of (n_Time_intervals, n_PV) or (n_PV, n_Time_intervals)
PV_P=[[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4]]
#or 
PV_P=np.transpose(PV_P)

#Electricity cost predections in $/Wh >> shape is (n_Time_intervals, ) 
electricity_cost=[0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2]

#CO2 predections in gco2/Wh>> shape is (n_Time_intervals, )
CO2=[5,5,5,5,5,5,5,5,5,5]


#ESS Parameters
ESS_capacity=[10,25]   #in Wh and it should be a list with shape of (n_ESS, )
ESS_SOC_init=[85,35]     #in % and it should be a list with shape of (n_ESS, )
ESS_max_charge=[1,1.4]   #in W and it should be a list with shape of (n_ESS, )
ESS_max_discharge=[1,1.4] #in W and it should be a list with shape of (n_ESS, )
ESS_charge_efficiency=[100,100]  #in % and it should be a list with shape of (n_ESS, )
ESS_discharge_efficiency=[100,100] #in % and it should be a list with shape of (n_ESS, )

#ebus parameters
eBUS_capacity=[5]  #in Wh and it should be a list with shape of (n_eBUS, )
eBUS_SOC_init=[10]  #in % and it should be a list with shape of (n_eBUS, )
eBUS_max_charge=[1]  #in W and it should be a list with shape of (n_eBUS, )
eBUS_max_discharge=[0] #in W and it should be a list with shape of (n_eBUS, )
eBUS_charge_efficiency=[100] #in % and it should be a list with shape of (n_eBUS, )
eBUS_discharge_efficiency=[100] #in % and it should be a list with shape of (n_eBUS, )
eBUS_round_trip_energy=[2] # the energy consumed by ebus for a round trip, in Wh and it should be a list with shape of (n_eBUS, )
eBus_scedule=[[0],[0],[1],[1],[1],[0],[0],[0],[0],[0]]          # shape is (n_Time_intervals, n_eBUS) or (n_eBUS, n_Time_intervals) and if connected to charger 1 and if not 0

#EV Parameters
EV_er=[3,4]  #in Wh and it should be a list with shape of (n_EV, )
EV_scedule=[[0,0],[0,1],[0,1],[1,1],[1,1],[1,0],[1,0],[1,0],[0,0],[0,0]] # shape is (n_Time_intervals, n_EV) or (n_EV, n_Time_intervals) and if connected to charger 1 and if not 0. create it based on connection time and departure time
EV_max_charge=[1,1.4]  #in W and it should be a list with shape of (n_EV, ), note that it is the maximum charge rate of the EV or max charge rate of charger for unknown EVs
EV_max_discharge=[0,0] #in W and it should be a list with shape of (n_EV, ), note that it is the maximum charge rate of the EV or max charge rate of charger for unknown EVs
EV_charge_efficiency=[100,100] #in % and it should be a list with shape of (n_EV, )
EV_discharge_efficiency=[100,100] #in % and it should be a list with shape of (n_EV, )
EV_n_charger=3 #number of chargers in your grid and it should be an integer
EV_charger_phase=[3,1,3] #the phase of chargers and it should be a list with shape of (EV_n_charger, )
EV_charger_ID=[1,2] #the ID of chargers and it should be a list with shape of (n_EV, )

EV_OFs=[{'EC':50,'SC':10,'CO2':40},{'EC':60,'CO2':20}] #the objective functions and their weights, the sum of weights should be 100% and it should be a list with shape of (n_EV, )
EV_smartcharge=['yes','no'] #if the EV user asks for smart charging or not and it should be a list with shape of (n_EV, )


##Grid Parameters
Grid_max_in=10  #in W
Grid_max_out=10  #in W
Grid_OFs={'EC':50,'SC':10,'CO2':40}  #the objective functions and their weights, the sum of weights should be 100%


#solver parameters
Solver='ipopt'  #solver name 


#Model Parameters
MOEMS=ModelParameters(Time_Resolution=Time_Resolution,n_Time_intervals=n_Time_intervals,
                    Grid_max_in=Grid_max_in,Grid_max_out=Grid_max_out,Grid_OFs=Grid_OFs,Load_P=Load_P,
                    PV_P=PV_P,electricity_cost=electricity_cost,CO2=CO2,ESS_capacity=ESS_capacity,
                    ESS_SOC_init=ESS_SOC_init,ESS_max_charge=ESS_max_charge,ESS_max_discharge=ESS_max_discharge,
                    ESS_charge_efficiency=ESS_charge_efficiency,ESS_discharge_efficiency=ESS_discharge_efficiency,
                    eBUS_capacity=eBUS_capacity,eBUS_SOC_init=eBUS_SOC_init,eBUS_max_charge=eBUS_max_charge,
                    eBUS_max_discharge=eBUS_max_discharge,eBUS_charge_efficiency=eBUS_charge_efficiency,
                    eBUS_discharge_efficiency=eBUS_discharge_efficiency,eBUS_round_trip_energy=eBUS_round_trip_energy,
                    eBus_scedule=eBus_scedule,EV_er=EV_er,EV_scedule=EV_scedule,EV_max_charge=EV_max_charge,EV_max_discharge=EV_max_discharge,
                    EV_charge_efficiency=EV_charge_efficiency,EV_discharge_efficiency=EV_discharge_efficiency,EV_n_charger=EV_n_charger,EV_charger_phase=EV_charger_phase,
                    EV_charger_ID=EV_charger_ID,EV_OFs=EV_OFs,EV_smartcharge=EV_smartcharge,Solver=Solver)

##expected output
#for ESS
print(MOEMS.ESS_SOC)
print(MOEMS.ESS_P)

#for eBUS
print(MOEMS.eBUS_SOC)
print(MOEMS.eBUS_P)

#for Grid
print(MOEMS.allPowers)

#for EV
print(MOEMS.EV_SOC)
print(MOEMS.EV_SOC_discrete)
print(MOEMS.EV_P)
print(MOEMS.EV_P_discrete)
print(MOEMS.EV_plan)
c=1