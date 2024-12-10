from p4p.client.thread import Context
import sys
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QTime
import pyqtgraph as pg
from plot_ui import Ui_MainWindow# Ensure this is the correct import for your UI file
from interface_app import Interface_app as iapp
import time

pm = "\u00B1"

'''
This program is meant to interface the oscilloscope and the cooler lock, in order to:
- start and stop acqusitions on the oscilloscope
- change detuning of cooler
- acquire photoemission at resonace on the 
'''
COOLER_MOT_FREQ = 1010 # MHz (for master on 2'-4')
COOLER_RES_FREQ = 995 # MHz (for master on 2'-4')
GAMMA = 5.88 # MHz

DEFAULT_VOLTAGE_RANGE = 0.25 # V
DEFAULT_TIME_RANGE = 8 # s

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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx: Context, osc: iapp.Osc_RS, func_gen: iapp.Func_Gen):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ctx = ctx
        self.osc = osc
        self.func_gen = func_gen
        
        self.x_osc = np.array([])
        self.y_osc = np.array([])
        
        self.x_auto = np.array([])
        self.y_auto = np.array([])
        
        self.time_range = DEFAULT_TIME_RANGE
        self.voltage_range = DEFAULT_VOLTAGE_RANGE
        
        self.start_time_fit = 5.0 #s
        self.end_time_fit = 10.0 # s
        self.mot_offset = 0.0
        self.fit_params = None
        self.fit_errors = None
        
        '''PLOTS'''
        # Set up two separate plot widgets
        self.plot_widget_osc = pg.PlotWidget()
        self.plot_widget_auto = pg.PlotWidget()
        self.plot_widget_fit = pg.PlotWidget()
        
        # Add the plot widgets to the layout in the UI
        self.ui.plot_osc.addWidget(self.plot_widget_osc)
        self.ui.plot_auto.addWidget(self.plot_widget_auto)
        self.ui.plot_fit.addWidget(self.plot_widget_fit)
        
        self.plot_widget_osc.setLabel('left', 'Voltage', units='V')  # y-axis
        self.plot_widget_osc.setLabel('bottom', 'Time', units='s')  # x-axis

        self.plot_widget_auto.setLabel('left', 'Voltage', units='V')  # y-axis
        self.plot_widget_auto.setLabel('bottom', 'Time', units='s')  # x-axis
        
        self.plot_widget_fit.setLabel('left', 'Voltage', units='V')  # y-axis
        self.plot_widget_fit.setLabel('bottom', 'Time', units='s')  # x-axis

        # Set fixed range for plots
        self.plot_widget_osc.setRange(xRange=(0, DEFAULT_TIME_RANGE), yRange=(0, DEFAULT_VOLTAGE_RANGE))  # x -> time, y -> photovoltage
        self.plot_widget_auto.setRange(xRange=(0, DEFAULT_TIME_RANGE), yRange=(0, DEFAULT_VOLTAGE_RANGE))  # x -> detuning, y -> photovoltage
        self.plot_widget_fit.setRange(xRange=(0, DEFAULT_TIME_RANGE), yRange=(0, DEFAULT_VOLTAGE_RANGE))
        
        # Initialize empty curves
        self.curve_osc = self.plot_widget_osc.plot([], [], pen='r')  # Red line for real-time data
        self.curve_auto = self.plot_widget_auto.plot([], [], pen='b')  # Blue line for acquisition data
        self.curve_fit = self.plot_widget_fit.plot([], [], pen='b')  # Blue line for acquisition data

        '''BUTTONS'''
        # Set up the spin box for frequency input
        self.ui.freq_box.setRange(0.01, 9999)  # Minimum 0.01, Maximum 9999
        self.ui.freq_box.setDecimals(2)  # Allow 2 decimal places (0.01 precision)
        self.ui.freq_box.setSingleStep(0.01)  # Set step size to 0.01
        self.ui.freq_box.setValue(COOLER_MOT_FREQ)
        
        # Set up the spin box for vertical range input
        self.ui.voltage_box.setRange(0.01, 10)  # Minimum 0.01, Maximum 10 V
        self.ui.voltage_box.setDecimals(2)  # Allow 2 decimal places (0.01 precision)
        self.ui.voltage_box.setSingleStep(0.01)  # Set step size to 0.01 V
        self.ui.voltage_box.setValue(DEFAULT_VOLTAGE_RANGE)
        
        # Set up the spin box for horizontal range input
        self.ui.time_box.setRange(0.01, 20)  # Minimum 0.01, Maximum 10 s
        self.ui.time_box.setDecimals(2)  # Allow 2 decimal places (0.01 precision)
        self.ui.time_box.setSingleStep(0.01)  # Set step size to 0.01 s
        self.ui.time_box.setValue(DEFAULT_TIME_RANGE)
        
        # Set up the spin box for frequency photo input
        self.ui.freq_photo_box.setRange(900, 1200)  # Minimum 0.01, Maximum 9999
        self.ui.freq_photo_box.setDecimals(2)  # Allow 2 decimal places (0.01 precision)
        self.ui.freq_photo_box.setSingleStep(0.01)  # Set step size to 0.01
        self.ui.freq_photo_box.setValue(COOLER_MOT_FREQ)
        
        # Set up the spin box for frequency mot charge input
        self.ui.freq_optimal_box.setRange(900, 1200)  # Minimum 0.01, Maximum 9999
        self.ui.freq_optimal_box.setDecimals(2)  # Allow 2 decimal places (0.01 precision)
        self.ui.freq_optimal_box.setSingleStep(0.01)  # Set step size to 0.01
        self.ui.freq_optimal_box.setValue(COOLER_MOT_FREQ)

        # # Connect buttons
        self.ui.set_freq_button.clicked.connect(self.set_beat_note_freq)
        self.ui.set_freq_res_button.clicked.connect(self.go_to_resonance)
        self.ui.set_freq_opt_button.clicked.connect(self.go_to_optimal)
        
        self.ui.set_time_button.clicked.connect(self.set_time_range)
        self.ui.set_voltage_button.clicked.connect(self.set_voltage_range)
        
        self.ui.start_button.clicked.connect(self.start_osc_acquisition)
        # self.ui.stop_button.clicked.connect(self.stop_osc_acquisition)
        
        self.ui.plot_osc_button.clicked.connect(self.update_plot_osc) # plot data from oscilloscope
        self.ui.save_osc_button.clicked.connect(self.save_osc)
        
        # Tab Meas. Lorentzian
        self.ui.auto_acquire_button.clicked.connect(self.auto_acquisition_osc) # plot data from auto-acquisition on oscilloscope
        self.ui.save_acquisition_button.clicked.connect(self.save_auto)
        
        # Tab Fit
        self.ui.set_range_time_fit_button.clicked.connect(self.set_range_time_for_fit)
        self.ui.fit_button.clicked.connect(self.fit_data)
        self.ui.save_data_fit_button.clicked.connect(self.save_data_fit)
        
        # Tam Num. Atoms
        self.ui.num_atoms_button.clicked.connect(self.compute_num_atoms)
        
    def set_beat_note_freq(self):
        '''Set Cooler frequency with value from UI'''
        freq_value = self.ui.freq_box.value() * 1e3 # kHz
        self.ctx.put('CoolLas:RFLock:FR', freq_value)
    
    def set_time_range(self):
        self.time_range = self.ui.time_box.value()
        print(f'time = {self.time_range} s')
        
        try:
            self.osc.Set_horizontal_range(self.time_range)
        except Exception as e:
            print(e)
            
        self.plot_widget_osc.setRange(xRange=(0, self.time_range))
        self.plot_widget_auto.setRange(xRange=(0, self.time_range))
        self.plot_widget_fit.setRange(xRange=(0, self.time_range))
    
    def set_voltage_range(self):
        self.voltage_range = self.ui.voltage_box.value()
        print(f'voltage = {self.voltage_range} V')
        try:
            self.osc.Set_vertical_range(self.voltage_range)
        except Exception as e:
            print(e)
        self.plot_widget_osc.setRange(yRange=(0, self.voltage_range))
        self.plot_widget_auto.setRange(yRange=(0, self.voltage_range))
        self.plot_widget_fit.setRange(yRange=(0, self.voltage_range))
        
    def start_osc_acquisition(self):
        """Start the data acquisition on scilloscope"""
        self.osc.Start_acquisition()
        print("Real-time data acquisition started.")

    def stop_osc_acquisition(self):
        """Stop the data acquisition and plotting."""
        self.osc.Stop_acquisition()
        print("Real time data acquisition stopped.")
    
    def get_data_osc(self):
        """get data from oscilloscope"""
        try:
            data = self.osc.Get_Data()
        except Exception as e:
            print('Using test data')
            x_data = np.linspace(0, self.time_range, 200)
            y_data = charge_MOT(x_data, self.voltage_range * 3/4, self.time_range / 15, self.time_range/3) + 0.01 * np.random.randn(200)
            data = (x_data, y_data)
            
        return data
                    
    def go_to_resonance(self):
        self.ctx.put('CoolLas:RFLock:FR', COOLER_RES_FREQ * 1e3) # in kHz
    
    def go_to_optimal(self):
        self.ctx.put('CoolLas:RFLock:FR', COOLER_MOT_FREQ * 1e3) # in kHz
    
    def go_to_freq(self, freq):
        '''Set a value for cooler beat-note in MHz'''
        if freq > 900 and freq < 1200:
            self.ctx.put('CoolLas:RFLock:FR', freq * 1e3) # in kHz
        else:
            print('Frequency is out of range [900, 1200] MHz')
            
    def update_plot_osc(self):
        """Update the osc plot with new data."""
        # Update the osc curve with new data
        time.sleep(0.5)
        self.x_osc, self.y_osc = self.get_data_osc()
        self.curve_osc.setData(self.x_osc, self.y_osc) # time in s, voltage in V
    
    
    def set_range_time_for_fit(self):
        '''Set time from which starting the fitting'''
        self.start_time_fit = self.ui.start_time_fit_box.value()
        self.end_time_fit = self.ui.end_time_fit_box.value()
        print(f'Set fit time range: \n - Start Time = {self.start_time_fit} \n - End Time = {self.end_time_fit}')
        
    def fit_data(self):
        """Fit the data from the oscilloscope with an exponential and plot the result."""
        # Select data for fitting based on start time
        index_fit = (self.x_auto > self.start_time_fit) * (self.x_auto < self.end_time_fit)
        x_data = self.x_auto[index_fit]
        index_offset = self.x_auto < self.start_time_fit/2
        self.mot_offset = np.mean(self.y_auto[index_offset])
        y_data = self.y_auto[index_fit] - self.mot_offset
        
        # Define initial parameter guesses
        sat_guess = np.mean(y_data)
        tau_guess = 1  # s
        
        # Perform curve fitting with initial guesses
        p0 = [sat_guess, tau_guess, self.start_time_fit]
        popt, pcov = curve_fit(charge_MOT, x_data, y_data, p0=p0)
        V0, tau, t0 = popt
        dV0, dtau, dt0 = np.sqrt(np.diag(pcov))  # Uncertainties in fit parameters
        
        self.fit_params = popt
        self.fit_errors = np.sqrt(np.diag(pcov))
        
        print(f'\n V0 = ({V0:.4f} {pm} {dV0:.4f}) V \n tau = ({tau:.4f} {pm} {dtau:.4f}) s \n t0 = ({t0:.4f} {pm} {dt0:.4f}) s')
        
        # Generate fitted curve data
        self.x_fit = x_data
        self.y_fit = charge_MOT(x_data, *popt)
        
        # Plot the fit on the dedicated fit plot widget
        self.plot_fit()

    def plot_fit(self):
        """Plot the fitted curve over the acquired data in the fit plot widget."""
        # Plot the acquired data (x_auto, y_auto) in the fit plot widget
        self.plot_widget_fit.clear()  # Clear any previous data or fits
         # Create or update the TextItem with fit results
        V0, tau, t0 = self.fit_params
        dV0, dtau, dt0 = self.fit_errors 

        fit_results_text = (
            f"V0 = ({V0:.4f} {pm} {dV0:.4f}) V\n"
            f"tau = ({tau:.4f} {pm} {dtau:.4f}) s\n"
            f"t0 = ({t0:.4f} {pm} {dt0:.4f}) s\n\n"
            #f"N = ({Num/1e8:.2f} {pm} {dNum}) " + r"$\cdot 10^8"
        )
        
        self.fit_text_item = pg.TextItem(fit_results_text, anchor=(0, 1), color='w', border='w', fill='k')
        self.plot_widget_fit.addItem(self.fit_text_item)

        # Adjust the position of the TextItem on the plot to ensure visibility
        self.fit_text_item.setPos(0, 0.75 * self.voltage_range)

        self.plot_widget_fit.plot(self.x_auto, self.y_auto - self.mot_offset, pen='b', name="Data")  # Original data in blue
        
        # Plot the fitted curve over the data
        self.plot_widget_fit.plot(self.x_fit, self.y_fit, pen='r', name="Fit")  # Fit in red
    
    def plot_fit_over_data(self):
        """Plot the fitted curve over the acquired data in the fit plot widget."""
        # Plot the acquired data (x_auto, y_auto) in the fit plot widget
        self.plot_widget_auto.clear()  # Clear any previous data or fits
        self.plot_widget_auto.plot(self.x_auto, self.y_auto, pen='b', name="Data")  # Original data in blue
        
        # Plot the fitted curve over the data
        self.plot_widget_auto.plot(self.x_fit, self.y_fit, pen='r', name="Fit")  # Fit in red

    def save_data_fit(self):
        '''save data from oscilloscope'''
        file_name = self.ui.file_name_fit_input.text()
        data = np.array([self.fit_params, self.fit_errors])
        df = pd.DataFrame(data, columns=['V0 [V]', 'tau [s]', 'off [V]'])
        df.to_csv(file_name, index=False)
        time.sleep(0.5)
        self.ui.file_name_fit_input.clear()
    
    def compute_num_atoms(self):
        """Compute num of atoms from photo-voltage at resonance"""
        #V0 = np.max(self.y_auto) - np.mean
        
    def auto_acquisition_osc(self):
        try:
            acquisition_time = self.time_range # s
            offset_time = 1 # s
            mot_time = acquisition_time - 2 * offset_time # s
            acquisition_range = self.voltage_range # V
                    
            self.osc.Set_vertical_range(acquisition_range)
            self.plot_widget_osc.setRange(yRange=(0, acquisition_range))
            self.plot_widget_auto.setRange(yRange=(0, acquisition_range))
            
            self.osc.Set_horizontal_range(acquisition_time)
            self.plot_widget_osc.setRange(xRange=(0, acquisition_time))  # x -> time, y -> photovoltage
            self.plot_widget_auto.setRange(xRange=(0, acquisition_time))
            
            self.osc.Stop_acquisition()
            self.osc.Start_acquisition()
            
            if FUNC_GEN_ON:
                time.sleep(offset_time)
                # Swicth ON Magnetic field
                self.func_gen.Set_Amp(5) # V
                self.func_gen.Set_Freq(0.1) # Hz
                self.func_gen.Set_Offset(2.5) # V
                self.func_gen.Set_Output('ON')
            
            time.sleep(mot_time)
            
            if self.ui.swipe_to_res_checkBox.isChecked():
                # Change beat note cooler to the set value (photo)
                Freq = self.ui.freq_photo_box.value()
                self.go_to_freq(Freq)
                print(f'Photo at {Freq:.2f} MHz')
            
            time.sleep(offset_time)
            
            self.x_auto, self.y_auto = self.get_data_osc()
            self.update_auto_plot()
            if FUNC_GEN_ON: 
                # Swicth OFF Magnetic field
                self.func_gen.Set_Output('OFF')
                
            self.go_to_freq(self.ui.freq_optimal_box.value())
            
        except Exception as e:
            
            if self.ui.swipe_to_res_checkBox.isChecked():
                print('Freq set to resonance')
                
            print('Using test data')
            N_data = 500
            x_data = np.linspace(0, self.time_range, N_data)
            t0 = 0.01 * np.random.randn() + self.time_range / 3
            index_larger_t0 = x_data > t0
            y_data = np.ones(N_data) * self.voltage_range/7
            y_data = y_data + charge_MOT(x_data, self.voltage_range * 3/4, tau=self.time_range/15, t0=t0) * index_larger_t0 + 0.01 * np.random.randn(N_data)
            self.x_auto = x_data
            self.y_auto = y_data
            self.update_auto_plot()
            
    def update_auto_plot(self):
        self.curve_auto.setData(self.x_auto, self.y_auto) # time in s, voltage in V
    
    def save_osc(self):
        '''save data from oscilloscope'''
        file_name = self.ui.file_name_osc_input.text()
        data = np.array([self.x_osc, self.y_osc]).T
        df = pd.DataFrame(data, columns=['Time [s]', 'Sig [V]'])
        df.to_csv(file_name, index=False)
        time.sleep(0.5)
        self.ui.file_name_osc_input.clear()
        
    def save_auto(self):
        '''save acquisition'''
        file_name = self.ui.file_name_auto_input.text()
        data = np.array([self.x_auto, self.y_auto]).T
        df = pd.DataFrame(data, columns=['Time [s]', 'Sig [V]'])
        df.to_csv(file_name, index=False)
        time.sleep(0.5)
        self.ui.file_name_auto_input.clear()
        
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
        

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(ctx=ctx, osc=osc, func_gen=func_gen)
    window.show()
    sys.exit(app.exec_())

