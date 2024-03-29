"""
@author: Bahman AHmadi <<->> b.ahmadi@utwente.nl
"""
import sys,numpy as np
from pyomo.environ import *
import logging
logging.getLogger('pyomo.core').setLevel(logging.ERROR)
############################################################
class ModelParameters:
    def __init__(self,Time_Resolution:int=15,n_Time_intervals:int=96,Grid_max_in:int=None,Grid_max_out:int=None,Grid_OFs=None,
                Load_P=None,PV_P=None,electricity_cost=None,CO2=None,
                ESS_capacity:int=None,ESS_SOC_init:int=None,ESS_max_charge:int=None,
                ESS_max_discharge:int=None,ESS_charge_efficiency:int=None,ESS_discharge_efficiency:int=None,
                eBUS_capacity:int=None,eBUS_SOC_init:int=None,eBUS_max_charge:int=None,
                eBUS_max_discharge:int=None,eBUS_charge_efficiency=None,eBUS_discharge_efficiency=None,eBUS_round_trip_energy=None,
                eBus_scedule=None,EV_er:int=None,EV_scedule=None,EV_max_charge:int=None,
                EV_max_discharge:int=None,EV_charge_efficiency:int=None,EV_discharge_efficiency:int=None,EV_n_charger:int=None,
                EV_charger_phase=None,EV_charger_ID:int=None,EV_OFs=None,EV_smartcharge=None,Solver='ipopt'):
        """
        parameters:
        Time_Resolution (int): the time resolution of the model in minutes
        n_Time_intervals (int): the number of time intervals in one day
        Grid_max_in (int): the maximum power that can be injected to the grid in W
        Grid_max_out (int): the maximum power that can be taken from the grid in W
        Grid_OFs (dict): the objective functions and their weights, the sum of weights should be 100%
        Load_P (array): the load profile in W with shape of (n_Time_intervals, n_loads) or (n_loads, n_Time_intervals) 
        PV_P (array): the PV predections in W with shape of (n_Time_intervals, n_PV) or (n_PV, n_Time_intervals)
        electricity_cost (array): the electricity cost predections in cost/Wh
        CO2 (array): the CO2 predections in gCO2/Wh
        ESS_capacity (array): the capacity of ESSs in Wh with shape of (n_ESS, )
        ESS_SOC_init (array): the initial SOC of ESSs in % with shape of (n_ESS, )
        ESS_max_charge (array): the maximum charge power of ESSs in W with shape of (n_ESS, )
        ESS_max_discharge (array): the maximum discharge power of ESSs in W with shape of (n_ESS, )
        ESS_charge_efficiency (array): the charge efficiency of ESSs in % with shape of (n_ESS, )
        ESS_discharge_efficiency (array): the discharge efficiency of ESSs in % with shape of (n_ESS, )
        eBUS_capacity (array): the capacity of eBUSs in Wh
        eBUS_SOC_init (array): the initial SOC of eBUSs in % with shape of (n_eBUS, )
        eBUS_max_charge (array): the maximum charge power of eBUSs in W with shape of (n_eBUS, )
        eBUS_max_discharge (array): the maximum discharge power of eBUSs in W
        eBUS_charge_efficiency (array): the charge efficiency of eBUSs in % with shape of (n_eBUS, )
        eBUS_discharge_efficiency (array): the discharge efficiency of eBUSs in % with shape of (n_eBUS, )
        eBUS_round_trip_energy (array): the energy consumed by ebus for a round trip, in Wh with shape of (n_eBUS, )
        eBus_scedule (array): the eBus_scedule in % with shape of (n_Time_intervals, n_eBUS) or (n_eBUS, n_Time_intervals)
        EV_er (array): the energy required by EVs in Wh with shape of (n_EV, )
        EV_scedule (array): the EV_scedule in 0 and 1 with shape of (n_Time_intervals, n_EV) or (n_EV, n_Time_intervals), 1 for connected to charger and 0 for not connected
        EV_max_charge (array): the maximum charge power of EVs in W with shape of (n_EV, )
        EV_max_discharge (array): the maximum discharge power of EVs in W with shape of (n_EV, )
        EV_charge_efficiency (array): the charge efficiency of EVs in % with shape of (n_EV, )
        EV_discharge_efficiency (array): the discharge efficiency of EVs in % with shape of (n_EV, )
        EV_n_charger (int): the number of chargers in your grid
        EV_charger_phase (array): the phase of chargers with shape of (EV_n_charger, )
        EV_charger_ID (array): the ID of chargers with shape of (n_EV, )
        EV_OFs (array): the objective functions and their weights, the sum of weights should be 100% with shape of (n_EV, )
        EV_smartcharge (array): if the EV user asks for smart charging or not with shape of (n_EV, )
        Solver (str): the solver that you want to use, default is 'ipopt'
        
        outputs/varibales:
        instance: the instance of the model
        solver: the solver that you want to use
        model: the model that you have created
        ESS_SOC: the SOC of ESSs
        ESS_P: the power of ESSs
        eBUS_SOC: the SOC of eBUSs
        eBUS_P: the power of eBUSs
        allPowers: the sum of all powers
        EV_SOC: the SOC of EVs
        EV_P: the power of EVs
        EV_plan: the plan of EVs
        EV_SOC_discrete: the discrete SOC of EVs
        EV_P_discrete: the discrete power of EVs
        """



        ##Time steps resolution
        self.Time_Resolution=Time_Resolution # minutes
        self.n_Time_intervals=n_Time_intervals # number of time intervals in one day

        ##Loads
        if Load_P is None:
            print('Load_P is not defined')
            print("please provide the load profile in W with shape of (n_Time_intervals, n_loads) or (n_loads, n_Time_intervals)")
            print("or provide empty list or array")
            sys.exit()
        
        loadshape=np.shape(Load_P)
        for i in range(len(loadshape)):
            if loadshape[i] is not n_Time_intervals:
                self.Load_N=loadshape[i]
                index=i
        
        if self.Load_N==0:
            self.Load_P=np.zeros((self.n_Time_intervals, 1))  #in W
        else:
            self.Load_P=np.sum(Load_P,axis=index)  #in W
        self.Load_n=1  #number of loads
        


        ##PVs
        if PV_P is None:
            print('PV_P is not defined')
            print("please provide the PV predections in W with shape of (n_Time_intervals, n_PV) or (n_PV, n_Time_intervals)")
            print("or provide empty list or array")
            sys.exit()
        
        pvshape=np.shape(PV_P)
        for i in range(len(pvshape)):
            if pvshape[i] is not n_Time_intervals:
                self.PV_n=pvshape[i] # number of PVs
                index=i
        if self.PV_n==0:
            self.PV_P=np.zeros((self.n_Time_intervals, 1))
        else:
            if index==1:
                self.PV_P=PV_P   #in W 
            else:
                self.PV_P=np.transpose(PV_P) 
        


        ##electricity cost information
        if electricity_cost is None:
            print('electricity_cost is not defined')
            print("please provide the electricity cost predections in cost/Wh with shape of (n_Time_intervals, )")
            sys.exit()
        self.E_cost=electricity_cost #in cost_unit/Wh


        ##CO2
        if CO2 is None:
            print('CO2 is not defined')
            print("please provide the CO2 predections in gCO2/Wh with shape of (n_Time_intervals, )")
            sys.exit()
        self.CO2=CO2 #in gCO2/Wh


        ##ESS >>parameters
        if ESS_capacity is None:
            print('ESS_capacity is not defined!')
            ESS_capacity=[]
        else:
            if len(ESS_capacity)==0:
                print('No ESS in your grid')
        self.ESS_capacity=ESS_capacity    #in Wh and it should be a list with shape of (n_ESS, )
        self.ESS_n=len(self.ESS_capacity) #number of ESSs
        

        if self.ESS_n==0:
            self.ESS_SOC_init=[]   #in % and it should be a list with shape of (n_ESS, )
            self.ESS_max_charge=[] #in W and it should be a list with shape of (n_ESS, )
            self.ESS_max_discharge= [] #in W and it should be a list with shape of (n_ESS, )
            self.ESS_charge_efficiency=[] #in % and it should be a list with shape of (n_ESS, )
            self.ESS_discharge_efficiency=[] #in % and it should be a list with shape of (n_ESS, )
            
        else:
            if ESS_SOC_init is None:
                print('ESS_SOC_init is not defined')
                print("please provide the initial SOC of ESSs in % with shape of (n_ESS, )")
                sys.exit()
            self.ESS_SOC_init=ESS_SOC_init   #in % and it should be a list with shape of (n_ESS, )
            if ESS_max_charge is None:
                print('ESS_max_charge is not defined')
                print("please provide the maximum charge power of ESSs in W with shape of (n_ESS, )")
                sys.exit()
            self.ESS_max_charge=ESS_max_charge #in W and it should be a list with shape of (n_ESS, )
            if ESS_max_discharge is None:
                print('ESS_max_discharge is not defined')
                print("please provide the maximum discharge power of ESSs in W with shape of (n_ESS, )")
                sys.exit()
            self.ESS_max_discharge= ESS_max_discharge #in W and it should be a list with shape of (n_ESS, )
            if ESS_charge_efficiency is None:
                print('ESS_charge_efficiency is not defined')
                print("please provide the charge efficiency of ESSs in % with shape of (n_ESS, )")
                sys.exit()
            self.ESS_charge_efficiency=ESS_charge_efficiency #in % and it should be a list with shape of (n_ESS, )
            if ESS_discharge_efficiency is None:
                print('ESS_discharge_efficiency is not defined')
                print("please provide the discharge efficiency of ESSs in % with shape of (n_ESS, )")
                sys.exit()
            self.ESS_discharge_efficiency=ESS_discharge_efficiency #in % and it should be a list with shape of (n_ESS, )
            
        ##ESS >> Variables
        self.ESS_SOC=[]
        self.ESS_P=[]

        
        
        ##eBUS >> parameters
        if eBUS_capacity is None:
            print('eBUS_capacity is not defined!')
            eBUS_capacity=[]
        else:
            if len(eBUS_capacity)==0:
                print('No eBUS in your grid')

        self.eBUS_capacity=eBUS_capacity  #in Wh and it should be a list with shape of (n_eBUS, )
        self.eBUS_n=len(self.eBUS_capacity) #number of eBUSs
        if self.eBUS_n==0:
            self.eBUS_SOC_init=[]
            self.eBUS_max_charge=[]
            self.eBUS_max_discharge=[]
            self.eBUS_charge_efficiency=[]
            self.eBUS_discharge_efficiency=[]
            self.eBUS_round_trip_energy=[]
            self.eBus_scedule=[]
        else:
            if eBUS_SOC_init is None:
                print('eBUS_SOC_init is not defined')
                print("please provide the initial SOC of eBUSs in % with shape of (n_eBUS, )")
                sys.exit()
            self.eBUS_SOC_init= eBUS_SOC_init #in % and it should be a list with shape of (n_eBUS, )
            if eBUS_max_charge is None:
                print('eBUS_max_charge is not defined')
                print("please provide the maximum charge power of eBUSs in W with shape of (n_eBUS, )")
                sys.exit()
            self.eBUS_max_charge=eBUS_max_charge  #in W and it should be a list with shape of (n_eBUS, )
            if eBUS_max_discharge is None:
                print('eBUS_max_discharge is not defined')
                print("please provide the maximum discharge power of eBUSs in W with shape of (n_eBUS, )")
                sys.exit()
            self.eBUS_max_discharge=eBUS_max_discharge  #in W and it should be a list with shape of (n_eBUS, )
            if eBUS_charge_efficiency is None:
                print('eBUS_charge_efficiency is not defined')
                print("please provide the charge efficiency of eBUSs in % with shape of (n_eBUS, )")
                sys.exit()
            self.eBUS_charge_efficiency=eBUS_charge_efficiency  #in % and it should be a list with shape of (n_eBUS, )
            if eBUS_discharge_efficiency is None:
                print('eBUS_discharge_efficiency is not defined')
                print("please provide the discharge efficiency of eBUSs in % with shape of (n_eBUS, )")
                sys.exit()
            self.eBUS_discharge_efficiency=eBUS_discharge_efficiency #in % and it should be a list with shape of (n_eBUS, )
            if eBUS_round_trip_energy is None:
                print('eBUS_round_trip_energy is not defined')
                print("please provide the energy consumed by ebus for a round trip, in Wh with shape of (n_eBUS, )")
                sys.exit()
            self.eBUS_round_trip_energy=eBUS_round_trip_energy  # the energy consumed by ebus for a round trip, in Wh and it should be a list with shape of (n_eBUS, )
            if eBus_scedule is None:
                print('eBus_scedule is not defined')
                print("please provide the eBus_scedule in % with shape of (n_Time_intervals, n_eBUS) or (n_eBUS, n_Time_intervals)")
                sys.exit()
            eBus_shape=np.shape(eBus_scedule)
            if eBus_shape[0] is not n_Time_intervals:
                self.eBus_scedule=np.transpose(eBus_scedule)
            self.eBus_scedule=eBus_scedule
        
        ##eBUS Variables
        self.eBUS_SOC=[]
        self.eBUS_P=[]



        ##Grid parameters
        if Grid_max_in is None:
            print('Grid_max_in is not defined')
            print("please provide the maximum power of the grid in W")
            sys.exit()
        self.Grid_max_in=Grid_max_in #in W

        if Grid_max_out is None:
            print('Grid_max_out is not defined')
            print("please provide the maximum power of the grid in W")
            sys.exit()
        self.Grid_max_out=Grid_max_out #in W
        ##Grid Variables
        self.allPowers=[]

        ##OFs
        if Grid_OFs is None:
            print('OFs is not defined')
            print("please provide the OFs")
            print("example: {'SC':43,'EC':33,'CO2':24}")
            sys.exit()
        if len(Grid_OFs)<3:
            sc=Grid_OFs.get('SC')
            if sc is None:
                sc=0
            ec=Grid_OFs.get('EC')
            if ec is None:
                ec=0
            co2=Grid_OFs.get('CO2')
            if co2 is None:
                co2=0
            self.Grid_OFs={'SC':sc,'EC':ec,'CO2':co2}
        else:
            self.Grid_OFs=Grid_OFs #the objective functions and their weights, the sum of weights should be 100%
        

        ##EVs >> parameters
        if EV_er is None:
            print('No EV is charging!')
            EV_er=[]
        self.EV_er=EV_er  #in Wh and it should be a list with shape of (n_EV, )
        self.EV_n=len(self.EV_er) #number of EVs
        if self.EV_n==0:
            self.EV_scedule=[]
            self.EV_max_charge=[]
            self.EV_max_discharge=[]
            self.EV_charge_efficiency=[]
            self.EV_discharge_efficiency=[]
            self.EV_n_charger=0
            self.EV_charger_ID=[]
            self.EV_OFs=[]
            self.EV_smartcharge=[]
        else:
            shapeschedule=np.shape(EV_scedule)
            for i in range(len(shapeschedule)):
                if shapeschedule[i] is not n_Time_intervals:
                    index=i
            if index==0:
                self.EV_scedule=np.transpose(EV_scedule)
            else:
                self.EV_scedule=EV_scedule # shape is (n_Time_intervals, n_EV) or (n_EV, n_Time_intervals) and if connected to charger 1 and if not 0
            
            self.EV_max_charge=EV_max_charge  #in W and it should be a list with shape of (n_EV, )
            self.EV_max_discharge=EV_max_discharge #in W and it should be a list with shape of (n_EV, )
            self.EV_charge_efficiency=EV_charge_efficiency #in % and it should be a list with shape of (n_EV, )
            self.EV_discharge_efficiency=EV_discharge_efficiency #in % and it should be a list with shape of (n_EV, )
            self.EV_n_charger=EV_n_charger #number of chargers in your grid and it should be an integer
            self.EV_charger_phase=EV_charger_phase #the phase of chargers and it should be a list with shape of (EV_n_charger, )
            self.EV_charger_ID=EV_charger_ID #the ID of chargers and it should be a list with shape of (n_EV, )

            for i in range(self.EV_n):
                sc=EV_OFs[i].get('SC')
                if sc is None:
                    sc=0
                ec=EV_OFs[i].get('EC')
                if ec is None:
                    ec=0
                co2=EV_OFs[i].get('CO2')
                if co2 is None:
                    co2=0
                EV_OFs[i]={'SC':sc,'EC':ec,'CO2':co2}
            self.EV_OFs=EV_OFs #the objective functions and their weights, the sum of weights should be 100% and it should be a list with shape of (n_EV, )
            self.EV_smartcharge=EV_smartcharge #if the EV user asks for smart charging or not and it should be a list with shape of (n_EV, )
        self.chargingPowers=np.multiply([6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32],230)
        
        
        ##EV >> Variables
        self.EV_SOC=[]
        self.EV_SOC_discrete=[]
        self.EV_P=[]
        self.EV_P_discrete=[]
        self.EV_plan=[]
        
        
        ## Model parameters
        self.instance=[]
        self.solver=Solver

        ## Model
        self.model=self.create_model()

        ## Results
        #create instance of the model
        self.instance = self.model.create_instance()
        self.Find_Base_OFs()
        self.Find_results()

        

    def create_model(self):
        # Create model
        model = AbstractModel()
        ############################################################
        # Define sets
        model.t = RangeSet(self.n_Time_intervals) #range for time intervals
        model.n_OF=RangeSet(len(self.Grid_OFs)) #range for objective functions
        model.n_l = RangeSet(self.Load_n) #range for loads
        model.n_pv = RangeSet(self.PV_n) #range for PVs
        model.n_ess = RangeSet(self.ESS_n) #range for ESSs
        model.n_eBus = RangeSet(self.eBUS_n) #range for eBUSs
        model.n_EV = RangeSet(self.EV_n) #range for EVs
        model.n_EV_charger = RangeSet(self.EV_n_charger) #range for EV chargers
        ############################################################
        # Define parameters
        #OFs
        OF_name=[]
        for i in range(len(self.Grid_OFs)):
            OF_name.append(list(self.Grid_OFs.keys())[i])
        model.OF_name = Param(model.n_OF, within=Any,initialize=lambda model, n_OF: OF_name[n_OF-1])
        #grid params
        model.grid_max_in = Param(initialize=self.Grid_max_in)
        model.grid_max_out = Param(initialize=self.Grid_max_out)
        #electricity price
        model.E_cost = Param(model.t, initialize=lambda model, t: self.E_cost[t-1])
        #co2
        model.CO2 = Param(model.t, initialize=lambda model, t: self.CO2[t-1])
        #load
        model.P_load = Param(model.t, initialize=lambda model, t: self.Load_P[t-1])
        #pv
        model.PV = Param(model.t,model.n_pv, initialize=lambda model, t,n_pv: self.PV_P[t-1][n_pv-1])
        #ess
        model.ESS_capacity = Param(model.n_ess,initialize=lambda model,n_ess: self.ESS_capacity[n_ess-1])
        model.ESS_SOC_init = Param(model.n_ess,initialize=lambda model,n_ess: self.ESS_SOC_init[n_ess-1])
        model.ESS_max_charge = Param(model.n_ess,initialize=lambda model,n_ess: self.ESS_max_charge[n_ess-1])
        model.ESS_max_discharge = Param(model.n_ess,initialize=lambda model,n_ess: self.ESS_max_discharge[n_ess-1])
        model.ESS_charge_efficiency = Param(model.n_ess,initialize=lambda model,n_ess: self.ESS_charge_efficiency[n_ess-1])
        model.ESS_discharge_efficiency = Param(model.n_ess,initialize=lambda model,n_ess: self.ESS_discharge_efficiency[n_ess-1])
        #eBUS
        model.eBus_scedule = Param(model.t,model.n_eBus, initialize=lambda model, t,n_eBus: self.eBus_scedule[t-1][n_eBus-1])
        model.eBUS_capacity = Param(model.n_eBus ,initialize=lambda model,n_eBus: self.eBUS_capacity[n_eBus-1])
        model.eBUS_max_charge = Param(model.n_eBus ,initialize=lambda model,n_eBus: self.eBUS_max_charge[n_eBus-1])
        model.eBUS_max_discharge = Param(model.n_eBus ,initialize=lambda model,n_eBus: self.eBUS_max_discharge[n_eBus-1])
        model.eBUS_charge_efficiency = Param(model.n_eBus ,initialize=lambda model,n_eBus: self.eBUS_charge_efficiency[n_eBus-1])
        model.eBUS_discharge_efficiency = Param(model.n_eBus ,initialize=lambda model,n_eBus: self.eBUS_discharge_efficiency[n_eBus-1])
        model.eBUS_round_trip_energy = Param(model.n_eBus ,initialize=lambda model,n_eBus: self.eBUS_round_trip_energy[n_eBus-1])
        model.eBUS_SOC_init = Param(model.n_eBus, initialize=lambda model,n_eBus: self.eBUS_SOC_init[n_eBus-1])
        #EV
        model.EV_scedule = Param(model.t,model.n_EV, initialize=lambda model, t,n_EV: self.EV_scedule[t-1][n_EV-1])
        model.EV_er=Param(model.n_EV, initialize=lambda model,n_EV: self.EV_er[n_EV-1])
        model.EV_charger_ID=Param(model.n_EV, initialize=lambda model,n_EV: self.EV_charger_ID[n_EV-1])

        
        model.EV_max_charge = Param(model.n_EV, initialize=lambda model,n_EV_charger: self.EV_max_charge[n_EV_charger-1])
        model.EV_max_discharge = Param(model.n_EV, initialize=lambda model,n_EV_charger: self.EV_max_discharge[n_EV_charger-1])
        model.EV_charge_efficiency = Param(model.n_EV, initialize=lambda model,n_EV_charger: self.EV_charge_efficiency[n_EV_charger-1])
        model.EV_discharge_efficiency = Param(model.n_EV, initialize=lambda model,n_EV_charger: self.EV_discharge_efficiency[n_EV_charger-1])
        model.Charger_n_phase = Param(model.n_EV_charger, initialize=lambda model,n_EV_charger: self.EV_charger_phase[n_EV_charger-1])
        #time
        model.deltaT=Param(initialize=self.Time_Resolution/60)
        model.n_Time_intervals=Param(initialize=self.n_Time_intervals)
        ############################################################
        # Define variables
        #ESS
        model.P_ESS = Var(model.t,model.n_ess)# bounds=(-model.ESS_max_power, model.ESS_max_power))
        model.ESS_SOC = Var(model.t,model.n_ess)# within=NonNegativeReals, bounds=(0.1*model.ESS_capacity, 0.9*model.ESS_capacity))
        #eBUS
        model.P_eBUS = Var(model.t,model.n_eBus)#,within=NonNegativeReals, bounds=(0*model.eBUS_max_charge, model.eBUS_max_charge))
        model.SOC_eBUS = Var(model.t,model.n_eBus, within=NonNegativeReals)#, bounds=(model.eBUS_round_trip_energy, model.eBUS_capacity))
        #EV
        model.P_EV = Var(model.t,model.n_EV)#,
        model.EV_SOC = Var(model.t,model.n_EV, within=NonNegativeReals)
        

        ############################################################
        # define the wights of the objective function
        #for grid
        list_n_Grid_OFs=[i for i in range(1,len(self.Grid_OFs)+1)]
        model.w_OF_Grid=Param(list_n_Grid_OFs,mutable=True)
        model.OF_Base=Param(list_n_Grid_OFs,mutable=True)
        #for EV
        list_EV_wOFs=[]
        for i in range(self.EV_n):
            list_EV_wOFs.append([self.EV_OFs[i].get('SC'),self.EV_OFs[i].get('EC'),self.EV_OFs[i].get('CO2')])
        model.w_OF_EV=Param(model.n_EV,model.n_OF, initialize=lambda model, n_EV,n_OF: list_EV_wOFs[n_EV-1][n_OF-1],mutable=True)
        model.EV_smartchargeing=Param(model.n_EV,initialize=lambda model, n_EV: self.EV_smartcharge[n_EV-1],mutable=True)
        
        ############################################################
        ## Define objective function
        def OF_cost_rule(model):
            if len(model.n_l.data())<1:
                p_loads = [[0 for t in model.t] for n in range(1)]
            else:
                p_loads = [[model.P_load[t] for t in model.t] for n in model.n_l]
            if len(model.n_pv.data())<1:
                p_PV= [[0 for t in model.t] for n in range(1)]
            else:
                p_PV = [[model.PV[t,n] for t in model.t] for n in model.n_pv]
            if len(model.n_ess.data())<1:
                p_ESS= [[0 for t in model.t] for n in range(1)]
            else:
                p_ESS = [[model.P_ESS[t,n] for t in model.t] for n in model.n_ess]
            if len(model.n_eBus.data())<1:
                p_eBUS= [[0 for t in model.t] for n in range(1)]
            else:
                p_eBUS = [[model.P_eBUS[t,n] for t in model.t] for n in model.n_eBus]
            if len(model.n_EV.data())<1:
                p_EV= [[0 for t in model.t] for n in range(1)]
            else:
                p_EV = [[model.P_EV[t,n] for t in model.t] for n in model.n_EV]
            # allPowers=np.sum([np.sum(p_loads,axis=0),np.sum(p_EV,axis=0),np.sum(p_eBUS,axis=0),np.sum(p_ESS,axis=0),np.multiply(np.sum(p_PV,axis=0),-1)],axis=0)
            allPowers=np.sum([np.sum(p_loads,axis=0),np.sum(p_eBUS,axis=0),np.sum(p_ESS,axis=0),np.multiply(np.sum(p_PV,axis=0),-1)],axis=0)
            
            OF=0
            for i in range(1,len(model.OF_name)+1):
                if model.OF_name[i]=='CO2':
                    OFv=sum((allPowers[t-1]) * model.CO2[t] for t in model.t) #CO2 minimization
                    OFv_EV=[]
                    if len(model.n_EV.data())>1:
                        for EVn in range(len(model.n_EV.data())):
                            OFv_EV.append(sum((p_EV[EVn][t-1]) * model.CO2[t] for t in model.t))
                    else:
                        OFv_EV=[0]
                elif model.OF_name[i]=='SC':
                    OFv=sum((allPowers[t-1])**2 for t in model.t) #self consumption maximization
                    OFv_EV=[]
                    if len(model.n_EV.data())>1:
                        for EVn in range(len(model.n_EV.data())):
                            OFv_EV.append(sum((p_EV[EVn][t-1])**2 for t in model.t))
                    else:
                        OFv_EV=[0]
                elif model.OF_name[i]=='EC':
                    OFv=sum((allPowers[t-1]) * model.E_cost[t] for t in model.t) #electricity cost minimization
                    OFv_EV=[]
                    if len(model.n_EV.data())>1:
                        for EVn in range(len(model.n_EV.data())):
                            OFv_EV.append(sum((p_EV[EVn][t-1]) * model.E_cost[t] for t in model.t))
                    else:
                        OFv_EV=[0]
                
                if len(model.n_EV.data())>1:
                    OF=OF+model.w_OF_Grid[i]*OFv/model.OF_Base[i]
                    for EVn in range(1,len(model.n_EV.data())+1):
                        if model.EV_smartchargeing[EVn]()=='yes':
                            OF=OF+model.w_OF_EV[EVn,i]*OFv_EV[EVn-1]/model.OF_Base[i]
                        else:
                            OF=OF+model.w_OF_Grid[i]*OFv_EV[EVn-1]/model.OF_Base[i]
                else:
                    OF=OF+model.w_OF_Grid[i]*OFv/model.OF_Base[i]
            return OF
        model.OF = Objective(rule=OF_cost_rule,sense = minimize)
        ############################################################
        ### Define constraints

        ## Grid constraints
        if True:
            #power balance between load, PV, eBus, EV, ESS and the power of the grid
            def Power_Balance_Constraint_rule(model, t,n_pv,n_ess,n_eBus,n_EV):
                return (-model.grid_max_out,model.P_load[t]-model.PV[t,n_pv] + model.P_ESS[t,n_ess]+ model.P_eBUS[t,n_eBus]+ model.P_EV[t,n_EV], model.grid_max_in)
            model.Power_Balance_Constraint = Constraint(model.t,model.n_pv,model.n_ess,model.n_eBus,model.n_EV, rule=Power_Balance_Constraint_rule)

        
        if True:
            #power balance between load, eBus, EV, ESS and the power of the grid
            def Power_Balance_Constraint_rule1(model, t,n_ess,n_eBus,n_EV):
                return (-model.grid_max_out,model.P_load[t] + model.P_ESS[t,n_ess]+ model.P_eBUS[t,n_eBus]+ model.P_EV[t,n_EV], model.grid_max_in)
            model.Power_Balance_Constraint1 = Constraint(model.t,model.n_ess,model.n_eBus,model.n_EV, rule=Power_Balance_Constraint_rule1)

        ## ESS constraints
        if True:
            #power limit of the ESS  >>    model.P_ESS[t,n_ess] > 0 means charge 
            def ESS_power_Constraint_rule(model, t,n_ess):
                return (-model.ESS_max_discharge[n_ess], model.P_ESS[t,n_ess], model.ESS_max_charge[n_ess])
            model.ESS_power_Constraint = Constraint(model.t,model.n_ess, rule=ESS_power_Constraint_rule)
        
        if False:
            #power change limit of the ESS  >>    model.P_ESS[t,n_ess] can not change when EV charging 
            def ESS_power_Constraint_rule1(model, t,n_ess, n_EV):
                if t==model.t.first():
                    return Constraint.Skip
                if model.EV_scedule[t,n_EV]==1:
                    return (-model.ESS_max_discharge[n_ess], model.P_ESS[t,n_ess], 0.1)
                else:
                    return Constraint.Skip
            model.ESS_power_Constraint1 = Constraint(model.t,model.n_ess,model.n_EV, rule=ESS_power_Constraint_rule1)
    
        if True:
            #SOC limit of the ESS
            def ESS_SOC_Constraint_rule(model, t,n_ess):
                return (0.2*model.ESS_capacity[n_ess], model.ESS_SOC[t,n_ess], 0.9*model.ESS_capacity[n_ess])
            model.ESS_SOC_Constraint = Constraint(model.t,model.n_ess, rule=ESS_SOC_Constraint_rule)
        
        if True:
            # State of charge of the ESS # positive P_ESS means charging (load) #negative P_ESS means discharging (generation)
            def ESS_State_of_Charge_Constraint_rule(model, t,n_ess):
                Model_for_SOC='Kezo'
                if Model_for_SOC=="Kezo":   #the model for for online optimization in Kezo with regresion model for SOC of ESS
                    if t==model.t.first():
                        return model.ESS_SOC[t,n_ess] == model.ESS_SOC_init[n_ess]/100*model.ESS_capacity[n_ess]+ (model.P_ESS[t,n_ess]*model.ESS_charge_efficiency[n_ess]/100*model.deltaT)
                    a=0.99707
                    b=0.185707/model.deltaT  # considering deltaT=15min, 
                    c=0.004025
                    return model.ESS_SOC[t,n_ess] == a*model.ESS_SOC[t-1,n_ess] + (b*model.P_ESS[t,n_ess]*model.ESS_charge_efficiency[n_ess]/100*model.deltaT)+c
                else:
                    if t == model.t.first():
                        return model.ESS_SOC[t,n_ess] == model.ESS_SOC_init[n_ess]/100*model.ESS_capacity[n_ess]+ (model.P_ESS[t,n_ess]*model.ESS_charge_efficiency[n_ess]/100*model.deltaT)
                    return model.ESS_SOC[t,n_ess] == model.ESS_SOC[t-1,n_ess] + (model.P_ESS[t,n_ess]*model.ESS_charge_efficiency[n_ess]/100*model.deltaT)
            model.ESS_State_of_Charge_Constraint = Constraint(model.t,model.n_ess, rule=ESS_State_of_Charge_Constraint_rule)


        ## eBUS constraints
            
        #note that P_eBUS is zero while eBUS is not in station # positive P_eBUS means charging (load)
        if True:
            #power limit of the eBUS
            def eBUS_power_Constraint_rule1(model, t,n_eBus):
                if model.eBus_scedule[t,n_eBus] == 1:
                    return model.P_eBUS[t,n_eBus] == model.P_eBUS[t,n_eBus]*0
                else:
                    return model.P_eBUS[t,n_eBus] == model.P_eBUS[t,n_eBus]
            model.eBUS_power_Constraint = Constraint(model.t,model.n_eBus, rule=eBUS_power_Constraint_rule1)
        if True:
            #max min power fro eBUS
            def e_BUS_power_Constraint_rule(model, t,n_eBus):
                #return (-model.eBUS_max_discharge[n_eBus], model.P_eBUS[t,n_eBus], model.eBUS_max_charge[n_eBus])
                return (0, model.P_eBUS[t,n_eBus], model.eBUS_max_charge[n_eBus])
            model.e_BUS_power_Constraint1 = Constraint(model.t,model.n_eBus, rule=e_BUS_power_Constraint_rule)
        if True:
            #SOC limit of the eBUS
            def e_BUS_SOC_Constraint_rule(model, t,n_eBus):
                return (model.eBUS_round_trip_energy[n_eBus], model.SOC_eBUS[t,n_eBus], model.eBUS_capacity[n_eBus])
            model.e_BUS_SOC_Constraint = Constraint(model.t,model.n_eBus, rule=e_BUS_SOC_Constraint_rule)
        if True:
            #SOC rule of the eBUS
            def eBUS_State_of_Charge_Constraint_rule(model, t,n_eBus):
                if t == model.t.first():
                    #if value(model.P_eBUS[t,n_eBus])>0:
                    #    return model.SOC_eBUS[t,n_eBus] == model.eBUS_init[n_eBus]*model.eBUS_capacity[n_eBus]+ (model.P_eBUS[t,n_eBus]*model.eBUS_charge_efficiency*model.deltaT)-(model.eBus_scedule[t,n_eBus]*model.eBUS_round_trip_energy[n_eBus]*model.deltaT)
                    #else:
                    #    return model.SOC_eBUS[t,n_eBus] == model.eBUS_init[n_eBus]*model.eBUS_capacity[n_eBus]+ (model.P_eBUS[t,n_eBus]*model.eBUS_discharge_efficiency*model.deltaT)-(model.eBus_scedule[t,n_eBus]*model.eBUS_round_trip_energy[n_eBus]*model.deltaT)  
                    return model.SOC_eBUS[t,n_eBus] == model.eBUS_SOC_init[n_eBus]/100*model.eBUS_capacity[n_eBus]+ (model.P_eBUS[t,n_eBus]*model.eBUS_charge_efficiency[n_eBus]/100*model.deltaT)-(model.eBus_scedule[t,n_eBus]*model.eBUS_round_trip_energy[n_eBus]*model.deltaT)
                #if value(model.P_eBUS[t,n_eBus])>0:
                #    return model.SOC_eBUS[t,n_eBus] == model.SOC_eBUS[t-1,n_eBus] + (model.P_eBUS[t,n_eBus]*model.eBUS_charge_efficiency*model.deltaT)-(model.eBus_scedule[t,n_eBus]*model.eBUS_round_trip_energy[n_eBus]*model.deltaT)
                #else:
                #    return model.SOC_eBUS[t,n_eBus] == model.SOC_eBUS[t-1,n_eBus] + (model.P_eBUS[t,n_eBus]*model.eBUS_discharge_efficiency*model.deltaT)-(model.eBus_scedule[t,n_eBus]*model.eBUS_round_trip_energy[n_eBus]*model.deltaT)
                return model.SOC_eBUS[t,n_eBus] == model.SOC_eBUS[t-1,n_eBus] + (model.P_eBUS[t,n_eBus]*model.eBUS_charge_efficiency[n_eBus]/100*model.deltaT)-(model.eBus_scedule[t,n_eBus]*model.eBUS_round_trip_energy[n_eBus]*model.deltaT)

            model.eBUS_State_of_Charge_Constraint = Constraint(model.t,model.n_eBus, rule=eBUS_State_of_Charge_Constraint_rule)

        if True:
            def eBUS_State_of_Charge_last_Constraint_rule(model, t,n_eBus):
                #if t == model.t.last():
                #    return model.SOC_eBUS[t,n_eBus] >= 0.6*model.eBUS_capacity[n_eBus]
                if t == int(6*60/model.deltaT):
                    return model.SOC_eBUS[t,n_eBus] >= 0.95*model.eBUS_capacity[n_eBus]
                else:
                    return Constraint.Skip
                
            model.eBUS_State_of_Charge_Constraint1 = Constraint(model.t,model.n_eBus, rule=eBUS_State_of_Charge_last_Constraint_rule)


        ## EV constraints
            
        #Note that P_EV is zero while EV is not in station # positive P_eBUS means charging (load)
        if True:
            #power limit of the EV
            def EV_power_Constraint_rule(model, t,n_EV):
                if model.EV_scedule[t,n_EV] == 0:
                    return model.P_EV[t,n_EV] == model.P_EV[t,n_EV]*0
                else:
                    return model.P_EV[t,n_EV] == model.P_EV[t,n_EV]
            model.EV_power_Constraint = Constraint(model.t,model.n_EV, rule=EV_power_Constraint_rule)
        
        if True:
            #max min power for EV and give max power when smart charging is off
            def EV_power_Constraint1_rule(model, t,n_EV):
                if model.EV_scedule[t,n_EV] == 0:
                    return Constraint.Skip
                else:
                    if model.EV_smartchargeing[n_EV]()=='no':
                        return (model.EV_max_charge[model.EV_charger_ID[n_EV]]*0.95, model.P_EV[t,n_EV], model.EV_max_charge[model.EV_charger_ID[n_EV]])
                    else:
                        return (0, model.P_EV[t,n_EV], model.EV_max_charge[model.EV_charger_ID[n_EV]])
                    #return (1380, model.P_EV[t,n_EV], model.EV_max_charge[model.EV_charger_ID[n_EV]])
            model.EV_power_Constraint1 = Constraint(model.t,model.n_EV, rule=EV_power_Constraint1_rule)
        
        if True:
            #power can not be less than 6A
            def EV_power_can_not_be_less_than_6A_rule(model, t,n_EV):
                if model.EV_scedule[t,n_EV] == 0:
                    return Constraint.Skip
                else:
                    return model.P_EV[t,n_EV] >= 1440*model.Charger_n_phase[model.EV_charger_ID[n_EV]] #1440 w #6A for single phase charger
            model.EV_power_can_not_be_less_than_6A = Constraint(model.t,model.n_EV, rule=EV_power_can_not_be_less_than_6A_rule)

        if True:
            #SOC limit of the EV  between soc_now and full charge==energy required for full charge
            def EV_SOC_Constraint_rule1(model, t,n_EV):
                return (0, model.EV_SOC[t,n_EV], model.EV_er[n_EV])
            model.EV_SOC_Constraint = Constraint(model.t,model.n_EV, rule=EV_SOC_Constraint_rule1)
        
        if True:
            #SOC rule of the EV
            def EV_State_of_Charge_Constraint_rule(model, t,n_EV):
                if t == model.t.first():
                    return model.EV_SOC[t,n_EV] == (model.P_EV[t,n_EV]*model.EV_charge_efficiency[model.EV_charger_ID[n_EV]]/100*model.deltaT)
                if t>3:
                    if model.EV_scedule[t,n_EV]-model.EV_scedule[t-1,n_EV]==-1:
                        return model.EV_SOC[t,n_EV] == (model.P_EV[t,n_EV]*model.EV_charge_efficiency[model.EV_charger_ID[n_EV]]/100*model.deltaT)
                return model.EV_SOC[t,n_EV] == model.EV_SOC[t-1,n_EV] + (model.P_EV[t,n_EV]*model.EV_charge_efficiency[model.EV_charger_ID[n_EV]]/100*model.deltaT)
            model.EV_State_of_Charge_Constraint = Constraint(model.t,model.n_EV, rule=EV_State_of_Charge_Constraint_rule)


        if True:
            #insure 98% of the energy is charged before departure
            def EV_State_of_Charge_last_Constraint_rule(model, t,n_EV):
                
                if t==model.t.first():
                    return Constraint.Skip
                if t==model.t.last():
                    return Constraint.Skip
                if model.EV_scedule[t+1,n_EV]-model.EV_scedule[t,n_EV]==-1:
                    return model.EV_SOC[t,n_EV] >= 0.98*model.EV_er[n_EV]
                else:
                    return Constraint.Skip
                
            model.EV_State_of_Charge_Constraint1 = Constraint(model.t,model.n_EV, rule=EV_State_of_Charge_last_Constraint_rule)

        return model

    
    
    
    
    
    def Find_Base_OFs(self):
        """
        @author: Bahman AHmadi <<->> b.ahmadi@utwente.nl
        """
        #find the base OFs

        #define the solver
        solver = SolverFactory(self.solver)
        #assign the weights of the OFs as zero and base OFs as 1 for all OFs
        for i in range(1,len(self.Grid_OFs)+1):
            self.instance.OF_Base[i]=1
            self.instance.w_OF_Grid[i]=0

        #solve the model and find based OF value while wOF for an objective function is 1 and the rest are 0
        for i in range(1,len(self.Grid_OFs)+1):
            self.instance.w_OF_Grid[i]=1
            results = solver.solve(self.instance)
            self.instance.OF_Base[i]=value(self.instance.OF)
            self.instance.w_OF_Grid[i]=0
        return True

    
        
    def Find_results(self):
        """
        @author: Bahman AHmadi <<->> b.ahmadi@utwente.nl
        """
        #define the solver
        solver = SolverFactory(self.solver)
        #assign the weights of the OFs into the model
        wofs=[self.Grid_OFs.get('SC'),self.Grid_OFs.get('EC'),self.Grid_OFs.get('CO2')]
        for i in range(len(self.Grid_OFs)):
            self.instance.w_OF_Grid[i+1]=wofs[i]
        #solve the model
        Res=solver.solve(self.instance)

        ##find the results and fill  the variable with results
        #ESS
        if self.ESS_n>0:
            self.ESS_P = [[value(self.instance.P_ESS[t,n]) for t in self.instance.t] for n in self.instance.n_ess]
            self.ESS_SOC = [[value(self.instance.ESS_SOC[t,n]) for t in self.instance.t] for n in self.instance.n_ess]
        else:
            self.ESS_P =[np.zeros((self.n_Time_intervals))]
            self.ESS_SOC =[np.zeros((self.n_Time_intervals))]
        
        
        #eBUS
        if self.eBUS_n>0:
            self.eBUS_P = [[value(self.instance.P_eBUS[t,n]) for t in self.instance.t] for n in self.instance.n_eBus]
            self.eBUS_SOC = [[value(self.instance.SOC_eBUS[t,n]) for t in self.instance.t] for n in self.instance.n_eBus]
        else:
            self.eBUS_P =[np.zeros((self.n_Time_intervals))]
            self.eBUS_SOC =[np.zeros((self.n_Time_intervals))]
        
        
        #EV
        if self.EV_n>0:
            self.EV_P = [[value(self.instance.P_EV[t,n]) for t in self.instance.t] for n in self.instance.n_EV]
            self.EV_SOC = [[value(self.instance.EV_SOC[t,n]) for t in self.instance.t] for n in self.instance.n_EV]
            self.EV_plan = [[value(self.instance.EV_scedule[t,n]) for t in self.instance.t] for n in self.instance.n_EV]
        
            #find the dicrete schedule for EV charging if the chargers are current controllable
            self.EV_P_discrete=[]
            self.EV_SOC_discrete=[]
            for i in range(self.EV_n):
                a=[]
                b=[]
                if self.EV_max_charge[self.EV_charger_ID[i]-1]==7000:
                    chargingPowers=self.chargingPowers
                elif self.EV_max_charge[self.EV_charger_ID[i]-1]==22000:
                    chargingPowers=np.multiply(self.chargingPowers,3)
                else:
                    chargingPowers=np.multiply(self.chargingPowers,1)

                a,b=self.DiscretizationPlanning(self.EV_P[i], np.sum(self.EV_P[i]),self.EV_plan[i], chargingPowers, powerLimitsUpper = [], prices = None, beta = 1, efficiency = None, intervalMerge=None)
                self.EV_P_discrete.append(a)
                self.EV_SOC_discrete.append(b)
        else:
            self.EV_P =[np.zeros((self.n_Time_intervals))]
            self.EV_SOC =[np.zeros((self.n_Time_intervals))]
            self.EV_plan =[np.zeros((self.n_Time_intervals))]
            self.EV_P_discrete=[np.zeros((self.n_Time_intervals))]
            self.EV_SOC_discrete=[np.zeros((self.n_Time_intervals))]
        
        self.Load_P = [[self.instance.P_load[t] for t in self.instance.t] for n in self.instance.n_l]
        self.PV_P = [[self.instance.PV[t,n] for t in self.instance.t] for n in self.instance.n_pv]
        
        #agregared power
        #FIXME add the new EV schedule to all power list it is based on not discrete schedule
        self.allPowers=np.sum([np.sum(self.Load_P,axis=0),np.sum(self.EV_P,axis=0),np.sum(self.eBUS_P,axis=0),np.sum(self.ESS_P,axis=0),np.multiply(np.sum(self.PV_P,axis=0),-1)],axis=0)
        #OFs values
        OF_val=[]
        OF_par=[]
        OF_val_aPareto=[]
        Of_par_aPareto=[]
        for i in range(1,len(self.instance.OF_name)+1):
            if self.instance.OF_name[i]=='CO2':
                OFv=sum((self.allPowers[t-1]) * self.instance.CO2[t] for t in self.instance.t) #CO2 minimization
            elif self.instance.OF_name[i]=='SC':
                OFv=sum((self.allPowers[t-1])**2 for t in self.instance.t) #self consumption maximization
            elif self.instance.OF_name[i]=='EC':
                OFv=sum((self.allPowers[t-1]) * self.instance.E_cost[t] for t in self.instance.t) #electricity cost minimization
            OF_val_aPareto.append(value(OFv))
            Of_par_aPareto.append(value(OFv)/value(self.instance.OF_Base[i]))
        OF_val.append(OF_val_aPareto)
        OF_par.append(Of_par_aPareto)
        return True




    def DiscretizationPlanning(self, desired, chargeRequired,EV_plan, chargingPowers, powerLimitsUpper = [], prices = None, beta = 1, efficiency = None, intervalMerge=None):
        """
        @author: Bahman AHmadi <<->> b.ahmadi@utwente.nl
        """
        result = [0] * len(desired)
        remainingCharge = chargeRequired

        if efficiency is None:
            #assert(False)
            efficiency = [1] * len(chargingPowers)
        else:
            assert(len(efficiency) == len(chargingPowers))

        if prices is None:
            prices = [0] * len(desired)

        if intervalMerge is None:
            intervalMerge = [1] * len(desired)
        else:
            assert(len(intervalMerge) == len(desired))

        chargingPowers.sort()
        assert(len(chargingPowers) >= 1)

        slopes = []

        # FIXME: ADD SOME PENALTY TO SLOPES WITH HIGH INEFFECIENCY??

        for i in range(0, len(desired)):
            #calculate the first slopes
            # Check if the next slope fits in the powerlimits:
            if len(powerLimitsUpper) == 0 or chargingPowers[1] <= powerLimitsUpper[i]:
                slope = ((prices[i] * chargingPowers[1] * efficiency[1] + beta * intervalMerge[i] * pow((chargingPowers[1] * efficiency[1]) - desired[i], 2) \
                        - (prices[i] * chargingPowers[0]  * efficiency[0] + beta * intervalMerge[i] * pow((chargingPowers[0] * efficiency[0]) - desired[i], 2) )) \
                        / (intervalMerge[i]*((chargingPowers[1] * efficiency[1]) - (chargingPowers[0] * efficiency[0])))).real

                #add the association
                pair = (i, 1)
                association = (slope, pair)
                slopes.append(association)

        #now append the other options:
        while(remainingCharge > 0.001 and len(slopes)>0):
            #sort the slopes
            slopes.sort()

            i = slopes[0][1][0]
            j = slopes[0][1][1]

            assert(j>0)

            sigma = min(remainingCharge, intervalMerge[i]*(chargingPowers[j] - chargingPowers[j-1]))

            result[i] += sigma / intervalMerge[i]
            remainingCharge -= sigma

            slopes.pop(0)

            if(j < len(chargingPowers)-1):
                if len(powerLimitsUpper) == 0 or chargingPowers[j+1] <= powerLimitsUpper[i]:
                    #add new entry to replace
                    slope = ((prices[i]*chargingPowers[j+1]*efficiency[j+1] + beta * intervalMerge[i] * pow((chargingPowers[j+1] * efficiency[j+1])- desired[i], 2) \
                        - (prices[i] * chargingPowers[j] * efficiency[j] + beta * intervalMerge[i] * pow((chargingPowers[j] * efficiency[j]) - desired[i], 2) )) \
                        / (intervalMerge[i]*((chargingPowers[j+1] * efficiency[j+1]) - (chargingPowers[j] * efficiency[j])))).real

                    #add the association
                    pair = (i, j+1)
                    association = (slope, pair)
                    slopes.append(association)
        
        SOC=[np.sum(result[0])]
        k=0
        for it in range(1,len(result)):
            if EV_plan[it]-EV_plan[it-1]==-1:
                k=1
            if k==0:
                SOC.append(np.multiply(np.sum(result[0:it]),self.Time_Resolution/60))
            else:
                SOC.append(0)
        
        return result,SOC