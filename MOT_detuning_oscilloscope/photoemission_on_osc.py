from p4p.client.thread import Context
import sys
import numpy as np
import pandas as pd

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QTime
import pyqtgraph as pg
from plot_ui import Ui_MainWindow  # Ensure this is the correct import for your UI file
from interface_app import Interface_app as iapp
import time

'''
This program is meant to interface the oscilloscope and the cooler lock, in order to:
- start and stop acqusitions on the oscilloscope
- change detuning of cooler
- acquire photoemission at resonace on the 
'''
COOLER_MOT_FREQ = 1042# MHz
COOLER_RES_FREQ = 1027# MHz
GAMMA = 5.88 # MHz

DEFAULT_VOLTAGE_RANGE = 0.5 # V
DEFAULT_TIME_RANGE = 10 # s

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, ctx, osc: iapp.Osc_RS):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ctx = ctx
        self.osc = osc
        
        self.x_osc = np.array([])
        self.y_osc = np.array([])
        
        self.x_auto = np.array([])
        self.y_auto = np.array([])
        
        '''PLOTS'''
        # Set up two separate plot widgets
        self.plot_widget_osc = pg.PlotWidget()
        self.plot_widget_auto = pg.PlotWidget()
        
        # Add the plot widgets to the layout in the UI
        self.ui.plot_osc.addWidget(self.plot_widget_osc)
        self.ui.plot_auto.addWidget(self.plot_widget_auto)
        
        self.plot_widget_osc.setLabel('left', 'Voltage', units='V')  # y-axis
        self.plot_widget_osc.setLabel('bottom', 'Time', units='s')  # x-axis

        self.plot_widget_auto.setLabel('left', 'Voltage', units='V')  # y-axis
        self.plot_widget_auto.setLabel('bottom', 'Time', units='s')  # x-axis

        # Set fixed range for both plots
        self.plot_widget_osc.setRange(xRange=(0, DEFAULT_TIME_RANGE), yRange=(0, DEFAULT_VOLTAGE_RANGE))  # x -> time, y -> photovoltage
        self.plot_widget_auto.setRange(xRange=(0, DEFAULT_TIME_RANGE), yRange=(0, DEFAULT_VOLTAGE_RANGE))  # x -> detuning, y -> photovoltage
        
        # Initialize empty curves for real-time and acquisition
        self.curve_osc = self.plot_widget_osc.plot([], [], pen='r')  # Red line for real-time data
        self.curve_auto = self.plot_widget_auto.plot([], [], pen='b')  # Blue line for acquisition data

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

        # # Connect buttons
        self.ui.set_freq_button.clicked.connect(self.set_beat_note_freq)
        self.ui.set_freq_res_button.clicked.connect(self.go_to_resonance)
        self.ui.set_freq_opt_button.clicked.connect(self.go_to_optimal)
        
        self.ui.set_time_button.clicked.connect(self.set_time_range)
        self.ui.set_voltage_button.clicked.connect(self.set_voltage_range)
        
        self.ui.start_button.clicked.connect(self.start_osc_acquisition)
        self.ui.stop_button.clicked.connect(self.stop_osc_acquisition)
        
        self.ui.plot_osc_button.clicked.connect(self.update_plot_osc) # plot data from oscilloscope
        self.ui.save_osc_button.clicked.connect(self.save_osc)
        
        self.ui.auto_acquire_button.clicked.connect(self.auto_acquisition_osc) # plot data from auto-acquisition on oscilloscope
        self.ui.save_acquisition_button.clicked.connect(self.save_auto)
        
    def set_beat_note_freq(self):
        '''Set Cooler frequency with value from UI'''
        freq_value = self.ui.freq_box.value() * 1e3 # kHz
        self.ctx.put('CoolLas:RFLock:FR', freq_value)
    
    def set_time_range(self):
        time_range = self.ui.time_box.value()
        print(f'time = {time_range} s')
        self.osc.Set_horizontal_range(time_range)
        self.plot_widget_osc.setRange(xRange=(0, time_range))
        self.plot_widget_auto.setRange(xRange=(0, time_range))
    
    def set_voltage_range(self):
        voltage_range = self.ui.voltage_box.value()
        print(f'voltage = {voltage_range} V')
        self.osc.Set_vertical_range(voltage_range)
        self.plot_widget_osc.setRange(yRange=(0, voltage_range))
        self.plot_widget_auto.setRange(yRange=(0, voltage_range))
        
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
        return self.osc.Get_Data()
        
    def go_to_resonance(self):
        self.ctx.put('CoolLas:RFLock:FR', COOLER_RES_FREQ * 1e3) # in kHz
    
    def go_to_optimal(self):
        self.ctx.put('CoolLas:RFLock:FR', COOLER_MOT_FREQ * 1e3) # in kHz
            
    def update_plot_osc(self):
        """Update the osc plot with new data."""
        # Update the osc curve with new data
        time.sleep(0.5)
        self.x_osc, self.y_osc = self.get_data_osc()
        self.curve_osc.setData(self.x_osc, self.y_osc) # time in s, voltage in V
    
    def fit_data(self):
        """Fit the data from the oscilloscope with an exponential"""

    def plot_fit(self):
        """Plot fit over data"""
    
    def compute_num_atoms(self):
        """Compute num of atoms from photo-voltage"""
        
    def auto_acquisition_osc(self):
        time_to_resonance = 10 # s
        acquisition_time = 14 # s
        acquisition_range = 1 # V
                
        self.osc.Set_vertical_range(acquisition_range)
        self.plot_widget_osc.setRange(yRange=(0, acquisition_range))
        self.plot_widget_auto.setRange(yRange=(0, acquisition_range))
        
        self.osc.Set_horizontal_range(acquisition_time)
        self.plot_widget_osc.setRange(xRange=(0, acquisition_time))  # x -> time, y -> photovoltage
        self.plot_widget_auto.setRange(xRange=(0, acquisition_time))
        
        self.osc.Stop_acquisition()
        self.osc.Start_acquisition()
        
        time.sleep(time_to_resonance)
        self.go_to_resonance()
        
        time.sleep(acquisition_time - time_to_resonance + 1)
        self.x_auto, self.y_auto = self.get_data_osc()
        self.update_auto_plot()
        self.go_to_optimal()
        
    def update_auto_plot(self):
        self.curve_auto.setData(self.x_auto, self.y_auto) # time in s, voltage in V
    
    def save_osc(self):
        '''save data from oscilloscope'''
        file_name = self.ui.save_osc_button.text()
        data = np.array([self.x_osc, self.y_osc]).T
        df = pd.DataFrame(data, columns=['Time [s]', 'Sig [V]'])
        df.to_csv(file_name, index=False)
        
    def save_auto(self):
        '''save acquisition'''
        file_name = self.ui.save_acquisition_button.text()
        data = np.array([self.x_auto, self.y_auto]).T
        df = pd.DataFrame(data, columns=['Time [s]', 'Sig [V]'])
        df.to_csv(file_name, index=False)
        
if __name__ == "__main__":
    ctx = Context('pva')
    osc = iapp.Osc_RS()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(ctx=ctx, osc=osc)
    window.show()
    sys.exit(app.exec_())

