from MOEMS import ModelParameters 
import numpy as np


import os
ipopt_path=os.getcwd() #change it to the path of the ipopt solver depending on your system
os.environ['PATH'] = ipopt_path + os.pathsep + os.environ['PATH']
###example for a grid optimizing to 96 time intervals with 15 minutes resolution

#time parameters
Time_Resolution=15   #minutes
n_Time_intervals=96
 
#static load predection in W >> it does not matter for shape of the list/array but it should be a list/array of lists/arrays with shape of (n_Time_intervals, n_loads) or (n_loads, n_Time_intervals)
Load_P=[[0]*40+[1500]*20+[0]*36,[0]*50+[2000]*(25)+[0]*21]
Load_P=[[0]*n_Time_intervals]
##NOET: if you dont want to have static load, just give Load_P=[[0]*n_Time_intervals]
 
 
#PV predections in W>> it does not matter for shape of the list/array but it should be a list/array of lists/arrays with shape of (n_Time_intervals, n_PV) or (n_PV, n_Time_intervals)
PV_P=[[0]*24 + (np.sin(np.linspace(-np.pi, 0, 48)) ** 2 * 17000).tolist() + [0]*24,[0]*24 + (np.sin(np.linspace(-np.pi, 0, 48)) ** 2 * 26000).tolist() + [0]*24]
PV_P=[[0]*n_Time_intervals]
##NOET: if you dont want to have PV, just give PV_P=[0]*n_Time_intervals
 
#Electricity cost predections in $/Wh >> shape is (n_Time_intervals, ) 
electricity_cost_buy=[0.2]*40+[0.3]*20+[0.2]*36
electricity_cost_sell=[0.1]*40+[0.15]*20+[0.1]*36
##NOET: if you dont want to have electricity cost, just give electricity_cost=[0]*n_Time_intervals
 
#CO2 predections in gco2/Wh>> shape is (n_Time_intervals, )
CO2=[8]*40+[5]*20+[12]*28+ [8]*8
CO2=[1]*n_Time_intervals
##NOET: if you dont want to have CO2, just give CO2=[0]*n_Time_intervals
 
#ESS Parameters
ESS_capacity=[13000,13000]   #in Wh and it should be a list with shape of (n_ESS, )
ESS_SOC_init=[26,30]     #in % and it should be a list with shape of (n_ESS, )
ESS_max_charge=[12000,12000]   #in W and it should be a list with shape of (n_ESS, )
ESS_max_discharge=[12000,12000] #in W and it should be a list with shape of (n_ESS, )
ESS_charge_efficiency=[100,100]  #in % and it should be a list with shape of (n_ESS, )
ESS_discharge_efficiency=[100,100] #in % and it should be a list with shape of (n_ESS, )
 
 
##Grid Parameters
Grid_max_in=30000  #in W
Grid_max_out=30000  #in W
Grid_OFs={'EC':20,'SC':80,'CO2':0}  #the objective functions and their weights, the sum of weights should be 100%

#solver parameters
Solver='ipopt'  #solver name 


#Model Parameters
MOEMS=ModelParameters(Time_Resolution=Time_Resolution,n_Time_intervals=n_Time_intervals,
                    Grid_max_in=Grid_max_in,Grid_max_out=Grid_max_out,Grid_OFs=Grid_OFs,Load_P=Load_P,
                    PV_P=PV_P,electricity_cost_buy=electricity_cost_buy,electricity_cost_sell=electricity_cost_sell,CO2=CO2,ESS_capacity=ESS_capacity,
                    ESS_SOC_init=ESS_SOC_init,ESS_max_charge=ESS_max_charge,ESS_max_discharge=ESS_max_discharge,
                    ESS_charge_efficiency=ESS_charge_efficiency,ESS_discharge_efficiency=ESS_discharge_efficiency,
                    Solver=Solver)



##expected output
#for ESS
print("results for ESS")
print(MOEMS.ESS_SOC)
print(MOEMS.ESS_P)
print("")

#write it in a file (CSV)
np.savetxt('ESS_SOC.csv', MOEMS.ESS_SOC, delimiter=',')
np.savetxt('ESS_P.csv', MOEMS.ESS_P, delimiter=',')

#for eBUS
print("results for eBUS")
print(MOEMS.eBUS_SOC)
print(MOEMS.eBUS_P)
print("")

#write it in a file (CSV)
np.savetxt('eBUS_SOC.csv', MOEMS.eBUS_SOC, delimiter=',')
np.savetxt('eBUS_P.csv', MOEMS.eBUS_P, delimiter=',')

#for Grid
print("results for Grid")
print(MOEMS.allPowers)
print("")

#write it in a file (CSV)
np.savetxt('allPowers.csv', MOEMS.allPowers, delimiter=',')

#for EV
print("results for EV")
print(MOEMS.EV_SOC)
print(MOEMS.EV_SOC_discrete)
print(MOEMS.EV_P)
print(MOEMS.EV_P_discrete)
print(MOEMS.EV_plan)

#write it in a file (CSV)
np.savetxt('EV_SOC.csv', MOEMS.EV_SOC, delimiter=',')
np.savetxt('EV_SOC_discrete.csv', MOEMS.EV_SOC_discrete, delimiter=',')
np.savetxt('EV_P.csv', MOEMS.EV_P, delimiter=',')
np.savetxt('EV_P_discrete.csv', MOEMS.EV_P_discrete, delimiter=',')
np.savetxt('EV_plan.csv', MOEMS.EV_plan, delimiter=',')


c=1