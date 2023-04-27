# WSU ECE Benchtop Equipment Toolset

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0) ![PyVISA](https://pyvisa.readthedocs.io/en/latest/?badge=latest)

A toolset for controlling and automating benchtop equipment for electronics testing. Built for ECE 5900 Digital Signal Processing Capstone Project. 


## Description 

Gathering data from benchtop equipment can be a very tedious task, especially with any real precision or resolution. For example, gathering frequency response data is painful when gathering more than a few data points over a few frequency steps. This toolset aims to make all these tasks easier by automating the process using standard benchtop equipment commands and PyVISA.

## Dependencies
 - pyVISA
 - Numpy
 - Time
 - MatPlotLib
 - PySimpleGUI

## How To Use

 - [Keysight Interface API](#keysight-interface-api) 
   - [Connecting to Devices](#how-to-connect-to-devices)
   - [Frequnecy Response Test](#running-frequency-response-tests)
   - [Controlling Waveform Generator](#controlling-the-wavegenerator)
     - [on/off](#turning-onoff-wavegen)
     - [Set Frequency](#setting-frequency)
     - [Set Voltage](#setting-vpp)
     - [Set Waveform](#setting-waveform)
    - [Reading Files](#reading-files)
 - [Toolset GUI](#toolset-gui)

### **Keysight Interface API**

The API is used for implementing commands in your own Python code. After the object has been instantiated you can call simple functions that will automate tasks typically done by hand or on the oscilloscope.

#### -- **How to connect to devices:** --

```
\\ Instantidate object 
labObject = labequipment.labequipment()

\\ Autoconnect to available devices
labObject._autoconnect()
```

#### -- **Running Frequency Response Tests** --

Running frequency tests using the  `frequency_response` method:

`frequency_response(START_FREQ, STOP_FREQ, STEPS, VPP)`

This method will control the oscilloscope and waveform generator to step through the frequency range at the given voltage. It will get the phase and magnitude. 

Requires:
 - Input 1 on oscilloscope to be reference
 - Input 2 on oscilloscope to be device under test 

```
start_freq = 100
stop_freq = 1000
steps = 100
vpp = 2

labObject.frequency_response(start_freq, stop_freq, steps, vpp)
```
Returns nothing. Plots and writes results to `bode_plot.txt`

#### -- **Controlling the Wavegenerator** --
All of the standard functions on the wave generator are available to control.

##### *Turning on/off wavegen*

```
labObject.wavegen.on()
labObject.wavegen.off()
```

##### *Setting frequency*

Accepted ranges are the same of the connected waveform generator
```
FREQ = 1000
labObject.wavegen.set_freq(FREQ)
```

##### *Setting Vpp*

Accepted ranges are the same of the connected waveform generator
```
VPP = 2
labObject.wavegen.set_vpp(VPP)
```

##### *Setting waveform*

Currently accepts:
 - sine
 - sqaure
```
labObject.wavegen.set_waveform('sine')
```

### **Reading Files**

This `labequipment` object can also read files created by itself.

Returns:
 - Frequecy array in numpy array
 - Magnitude array in numpy array
 - Phase array in numpy array
 
The "bode_plot.txt" is hard coded. 

```
freq, mag, phase = labequipment.readExisting("bode_plot.txt")
```


### **Toolset GUI**

The GUI is a visual wrapper for the API and let's you control the arbitrary waveform generator and oscilloscope.

Currently in the GUI you can:
 - Connect to the equipment
 - Set specific frequencies on the wavefrom generator
 - Run a frequnecy reponse test

To start the GUI, run the `gui.py` script


## Acknowledgements

 - [PyVISA](https://github.com/pyvisa/pyvisa)
 - [keyoscacquire](https://github.com/asvela/keyoscacquire)
 - [Keysight Infiniium Oscilloscopes Programming Guide](https://keysight-docs.s3-us-west-2.amazonaws.com/keysight-pdfs/DSOV084A/Programmer_s+Guide+for+Infiniium+Oscilloscop.pdf)
 - [IEEE 448.2 Common Commands](https://rfmw.em.keysight.com/spdhelpfiles/truevolt/webhelp/US/Content/__I_SCPI/IEEE-488_Common_Commands.htm)

## Authors

- [@jackj770](https://github.com/jackj770)
