from MOEMS import ModelParameters 
import numpy as np

###example for a grid optimizing to 10 time intervals with 15 minutes resolution

#time parameters
Time_Resolution=15   #minutes
n_Time_intervals=96

#static load predection in W >> it does not matter for shape of the list/array but it should be a list/array of lists/arrays with shape of (n_Time_intervals, n_loads) or (n_loads, n_Time_intervals)
Load_P=[[0]*40+[1500]*20+[0]*36,[0]*50+[2000]*(25)+[0]*21]


#PV predections in W>> it does not matter for shape of the list/array but it should be a list/array of lists/arrays with shape of (n_Time_intervals, n_PV) or (n_PV, n_Time_intervals)
PV_P=[[0]*24 + (np.sin(np.linspace(-np.pi, 0, 48)) ** 2 * 17000).tolist() + [0]*24,[0]*24 + (np.sin(np.linspace(-np.pi, 0, 48)) ** 2 * 26000).tolist() + [0]*24]


#Electricity cost predections in $/Wh >> shape is (n_Time_intervals, ) 
electricity_cost=[0.2]*40+[0.3]*20+[0.2]*36

#CO2 predections in gco2/Wh>> shape is (n_Time_intervals, )
CO2=[8]*40+[5]*20+[12]*28+ [8]*8


#ESS Parameters
ESS_capacity=[13000,13000]   #in Wh and it should be a list with shape of (n_ESS, )
ESS_SOC_init=[26,30]     #in % and it should be a list with shape of (n_ESS, )
ESS_max_charge=[12000,12000]   #in W and it should be a list with shape of (n_ESS, )
ESS_max_discharge=[12000,12000] #in W and it should be a list with shape of (n_ESS, )
ESS_charge_efficiency=[100,100]  #in % and it should be a list with shape of (n_ESS, )
ESS_discharge_efficiency=[100,100] #in % and it should be a list with shape of (n_ESS, )

#ebus parameters
eBUS_capacity=[]  #in Wh and it should be a list with shape of (n_eBUS, )
eBUS_SOC_init=[]  #in % and it should be a list with shape of (n_eBUS, )
eBUS_max_charge=[]  #in W and it should be a list with shape of (n_eBUS, )
eBUS_max_discharge=[] #in W and it should be a list with shape of (n_eBUS, )
eBUS_charge_efficiency=[] #in % and it should be a list with shape of (n_eBUS, )
eBUS_discharge_efficiency=[] #in % and it should be a list with shape of (n_eBUS, )
eBUS_round_trip_energy=[] # the energy consumed by ebus for a round trip, in Wh and it should be a list with shape of (n_eBUS, )
eBus_scedule=[]          # shape is (n_Time_intervals, n_eBUS) or (n_eBUS, n_Time_intervals) and if connected to charger 1 and if not 0

#EV Parameters
EV_er=[15000,21000]  #in Wh and it should be a list with shape of (n_EV, )
EV_scedule=[[0]*40+[1]*28+[0]*28,[0]*72+[1]*24] # shape is (n_Time_intervals, n_EV) or (n_EV, n_Time_intervals) and if connected to charger 1 and if not 0. create it based on connection time and departure time
EV_max_charge=[11000,7000]  #in W and it should be a list with shape of (n_EV, ), note that it is the maximum charge rate of the EV or max charge rate of charger for unknown EVs
EV_max_discharge=[0,0] #in W and it should be a list with shape of (n_EV, ), note that it is the maximum charge rate of the EV or max charge rate of charger for unknown EVs
EV_charge_efficiency=[100,100] #in % and it should be a list with shape of (n_EV, )
EV_discharge_efficiency=[100,100] #in % and it should be a list with shape of (n_EV, )
EV_n_charger=3 #number of chargers in your grid and it should be an integer
EV_charger_phase=[3,1,3] #the phase of chargers and it should be a list with shape of (EV_n_charger, )
EV_charger_ID=[1,2] #the ID of chargers and it should be a list with shape of (n_EV, )

EV_OFs=[{'EC':50,'SC':10,'CO2':40},{'EC':60,'CO2':20}] #the objective functions and their weights, the sum of weights should be 100% and it should be a list with shape of (n_EV, )
EV_smartcharge=['yes','no'] #if the EV user asks for smart charging or not and it should be a list with shape of (n_EV, )


##Grid Parameters
Grid_max_in=30000  #in W
Grid_max_out=30000  #in W
Grid_OFs={'EC':10,'SC':80,'CO2':10}  #the objective functions and their weights, the sum of weights should be 100%


#solver parameters
Solver='ipopt'  #solver name 


#Model Parameters
MOEMS=ModelParameters(Time_Resolution,n_Time_intervals,
                    Grid_max_in,Grid_max_out,Grid_OFs,Load_P,
                    PV_P,electricity_cost,CO2,ESS_capacity,
                    ESS_SOC_init,ESS_max_charge,ESS_max_discharge,
                    ESS_charge_efficiency,ESS_discharge_efficiency,
                    eBUS_capacity,eBUS_SOC_init,eBUS_max_charge,
                    eBUS_max_discharge,eBUS_charge_efficiency,
                    eBUS_discharge_efficiency,eBUS_round_trip_energy,
                    eBus_scedule,EV_er,EV_scedule,EV_max_charge,EV_max_discharge,
                    EV_charge_efficiency,EV_discharge_efficiency,EV_n_charger,EV_charger_phase,
                    EV_charger_ID,EV_OFs,EV_smartcharge,Solver)


c=1