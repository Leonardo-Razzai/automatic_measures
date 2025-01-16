from p4p.client.thread import Context
import sys
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from interface_app import Interface_app as iapp
import time
from git import Repo

pm = "\u00B1"

'''
This program is meant to interface the oscilloscope and the cooler lock, in order to:
- start and stop acqusitions on the oscilloscope
- change detuning of cooler
- acquire photoemission at resonace on the 
'''
COOLER_MOT_FREQ = 1036 # MHz (for master on 3'-4') ; 1010 MHz (for master on 2'-4') 
COOLER_RES_FREQ = 1027 # MHz (for master on 3'-4') ; 995 MHz (for master on 3'-4')
GAMMA = 5.88 # MHz

DEFAULT_VOLTAGE_RANGE = 0.15 # V
DEFAULT_TIME_RANGE = 6 # s
TIME_MOT = 4
OFF_TIME = (DEFAULT_TIME_RANGE-TIME_MOT) / 2

# True if Func gen is connected via ethernet
FUNC_GEN_ON = True

def charge_MOT(t, V0, tau, t0):
    return V0 * (1 - np.exp(-(t-t0)/tau))

def Prob_photoemission(Delta, s0, Gamma):
  return s0/2 / (1 + s0 + 4 * Delta**2 / Gamma**2)

def NumOfAtoms(V0, dV0, Delta, s0, Gamma):
  tau = 2.38 *1e6 # V/A 5% error
  eta = 0.5 # A/W 10 % error
  R_lens = 2 # cm
  dist_mot = 40 # cm
  sigma = np.pi * (R_lens/dist_mot)**2
  Gamma_fund = 5.88 * 1e6 # Hz
  Ep = 1.589 * 1.602 * 1e-19 # J
  
  I = V0 / tau # A
  P = I / eta # W
  
  # relative errors
  dV0_rel = dV0/V0
  dtau_rel = 0.05
  deta_rel = 0.1
  ddist_mot_rel = 2 / 40
  dsigma_rel = 2 * ddist_mot_rel
  
  Na = P / (sigma * Prob_photoemission(Delta, s0, Gamma) * Gamma_fund * Ep)
  dNa = (dV0_rel + dtau_rel + deta_rel + dsigma_rel) * Na
  
  return (Na, dNa)

class MeasureWindow():
    def __init__(self, ctx: Context, osc: iapp.Osc_RS, func_gen: iapp.Func_Gen, Current: float):

        self.ctx = ctx
        self.osc = osc
        self.func_gen = func_gen
        self.Current = Current
        
        self.x_osc = np.array([])
        self.y_osc = np.array([])
        
        self.time_range = DEFAULT_TIME_RANGE
        self.voltage_range = DEFAULT_VOLTAGE_RANGE
        
        self.setup_oscilloscope()
        self.setup_func_gen()
    
    def setup_func_gen(self):
        try:
            self.func_gen.Set_Amp(5) # V
            self.func_gen.Set_Freq(0.05) # Hz
            self.func_gen.Set_Offset(2.5) # V
        except Exception as e:
            print(f'Error: {e}')
    
    def setup_oscilloscope(self):
        try:
            self.osc.Clear_Buffer()
            self.osc.Set_vertical_range(DEFAULT_VOLTAGE_RANGE)         
            self.osc.Set_horizontal_range(DEFAULT_TIME_RANGE)
            self.osc.Set_coupling('DC')
        except Exception as e:
            print(f'Error: {e}')            
    
    def get_data_osc(self):
        """get data from oscilloscope"""
        try:
            data = self.osc.Get_Data()
        except Exception as e:
            print(f'Error: {e}')
            
        return data
    
    def go_to_freq(self, freq):
        '''Set a value for cooler beat-note in MHz'''
        try:
            if freq > 900 and freq < 1200:
                self.ctx.put('CoolLas:RFLock:FR', freq * 1e3) # in kHz
            else:
                print('Frequency is out of range [900, 1200] MHz')
        except Exception as e:
              print(f'Error: {e}')

    def turn_on_BField(self):
        self.func_gen.Set_Output('ON')
    
    def turn_off_BField(self):
        self.func_gen.Set_Output('OFF')

    def FluoCurve_auto_meas(self, BN_Cooler: float):
        try:
            
            if FUNC_GEN_ON:
                self.func_gen.Set_Output('OFF')                
            
            self.osc.Clear_Buffer()
            self.osc.Start_single()
            
            if FUNC_GEN_ON:
                time.sleep(OFF_TIME)
                # Swicth ON Magnetic field
                time.sleep(0.1)
                self.turn_on_BField()
            
            time.sleep(TIME_MOT)
            
            # Change beat note cooler to the set value (photo)
            self.go_to_freq(BN_Cooler)
            print(f'Photo at {BN_Cooler:.2f} MHz')
            
            time.sleep(0.1)
            if FUNC_GEN_ON: 
                # Swicth OFF Magnetic field
                self.turn_off_BField()
                
            time.sleep(OFF_TIME)
            
            self.osc.Wait_acquisition_end()
            
            self.x_osc, self.y_osc = self.get_data_osc()
            
        except Exception as e:
            print(f'Error: {e}')
    
    def save_data_osc(self, Det: float):
        '''save data from oscilloscope'''
        file_name = f'B={self.Current}_D={Det}.csv'
        data = np.array([self.x_osc, self.y_osc]).T
        df = pd.DataFrame(data, columns=['Time [s]', 'Sig [V]'])
        df.to_csv(file_name, index=False)
        time.sleep(1)
        
    def save_data_to_github(self, file_name: str):
        # Authentication using a personal access token
        repo_path = "C:/Users/User/Desktop/Files_desktop/Bologna/PhD/auto_measures"
        file_to_add = file_name
        commit_message = f"Add {file_name} file"

        # Initialize Repo object
        repo = Repo(repo_path)
        repo.index.add([file_to_add])  # Add file
        repo.index.commit(commit_message)  # Commit
        origin = repo.remote(name="origin")
        origin.push()  # Push to GitHub
        
if __name__ == "__main__":
    
    try:
        ctx = Context('pva')
        osc = iapp.Osc_RS()
        func_gen = iapp.Func_Gen()
    except Exception as e:
        # Handle any exception here
        print(f"An error occurred:\n {e}")
        ctx = None
        osc = None
        func_gen = None
        

    window = MeasureWindow(ctx=ctx, osc=osc, func_gen=func_gen)
