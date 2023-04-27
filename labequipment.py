import pyvisa
import config
import numpy as np
import time
import matplotlib.pyplot as plt


def readExisting(filename):
   #open the file
    freq_array = []
    amp_array = []
    in_v_array = []
    phase_array = []
    count = 0
    with open(filename, 'r') as infile:
    #read each line
        for line in infile:
            columns = line.strip().split('\t')
            # print(columns[0])

            if len(columns) == 1 and count == 0:
                start_freq = float(columns[0])
                count = count + 1
            elif len(columns) == 1 and count == 1:
                stop_freq = float(columns[0])
                count = count + 1
            elif columns[0] != "" and count == 2:
                step_freq = float(columns[0])
                count = count + 1
            elif len(columns) > 1:
                freq_array.append(float(columns[0]))
                amp_array.append(float(columns[1]))
                in_v_array.append(float(columns[2]))
                phase_array.append(float(columns[3]))

    db = np.ones(len(np.array(freq_array) ))
    db = np.array(amp_array)/np.array(in_v_array)
    db = 20 * np.log(db)

    fig, axs = plt.subplots(2, sharex=True)
    axs[0].plot(freq_array, db)
    axs[0].set_title("Magnitude Response")
    axs[0].set(ylabel = "Magnitude (dB)")
    axs[0].grid()
    axs[1].plot(freq_array, phase_array)
    axs[1].set(ylabel = "Phase (Radians)")
    axs[1].grid()
    plt.show()

    return np.array(freq_array) , np.array(db), np.array(phase_array)


class labequipment:

    def __init__(self, verbose):
        self.verbose = verbose
        self._availableDevices = {}
        self.oscope = 0 
        self.wavegen = 0 
        self.dmm = 0 
        self.powersupply = 0 
        # self._autoconnect()
        # self._userCommand()
        

    def _autoconnect(self):
        """Auto connect functionality for connect VISA devices. It can find devices that are not lab equipment but will ignore those. 
        """
        print("Attempting autodetect...")
        rm = pyvisa.ResourceManager()
        avail_dev = rm.list_resources()

        device_list = ["Not Connected - Please Connect Oscilloscope", "Not Connected - Please Connect Waveform Generator", "temp", "temp"]

        if len(avail_dev) != 0:
            print("Found %i devices. Some of these devices may not be test equipment." % len(avail_dev))
        
            for i, n in enumerate(avail_dev):
                try:
                    dev = rm.open_resource(n)
                    self._availableDevices[i] = n 
                    dev_name = dev.query("*IDN?")
                    if dev_name.split(",")[1] == "DSOX1204G":
                        self.oscope = self.oscilioscope(rm, n)
                        device_list[0] = ("DSOX1204G (Digital Oscilloscope)")
                    if dev_name.split(",")[1] == "EDU33212A":
                        self.wavegen = self.waveGenerator(rm, n)
                        device_list[1] = ("EDU33212A (Waveform Generator)")    
                    if self.verbose:
                        print("Device: %i" % i)
                        print("Device Information: %s" % dev_name.split(",")[1])
                        
                except:
                    continue
        return device_list

    def _device_info_lookup(device_string):
        """Checks to see if the devices are support and returns the command set. This may be deprecated soon. It was just an idea.
        Parameters
        ----------
        idn : str
            Device Mode String
        Returns
        -------
        dev_type : str
            Full name of device as seen on front of device
        avail_commands : int
            An integer for later use
        """
        if device_string == "DSOX1204G":
            dev_type = "Keysight InfiniiVision Digital Oscilloscope 70 MHz - 2 GSa/s"
            avail_commands = 1
            return dev_type, avail_commands 
        if device_string == "EDU33212A":
            dev_type = "Keysight Waveform Generator 20 MHz"
            avail_commands = 2
            return dev_type, avail_commands 

    def frequency_response(self, start_freq, stop_freq, steps, Vpp):
        print(start_freq)
        print(stop_freq)
        print(steps)
        print(Vpp)
        step_freq = (int(stop_freq) - int(start_freq)) / int(steps)
        float(step_freq)
        start_freq = float(start_freq)
        stop_freq = float(stop_freq)
        step_freq = int(step_freq)

        freq_array = np.arange(start_freq, stop_freq + step_freq, step_freq)

        amp_array = np.zeros(len(freq_array))
        in_v_array = np.zeros(len(freq_array))
        phase_array = np.zeros(len(freq_array))

        file = open("bode_plot.txt", "w")

        file.write(str(start_freq)+"\n")
        file.write(str(stop_freq)+"\n")
        file.write(str(step_freq)+"\n\n")

        self.wavegen.set_waveform('sine')
        self.wavegen.set_freq(start_freq)
        self.wavegen.set_vpp(float(Vpp))
        self.wavegen.on()

        self.oscope.autoscale()
        time.sleep(2)

        for n, val in enumerate(freq_array):
            self.wavegen.set_freq(val)
            self.oscope.set_timebase(val)
            print("Aquiring Data....")
            amp_array[n] = self.oscope.aquire_data("vpp", 1)
            in_v_array[n] = self.oscope.aquire_data("vpp", 2)
            phase_array[n] = self.oscope.aquire_data("phase", 1, 2) 
            if phase_array[n] > 180 or phase_array[n] < -180:
                phase_array[n] = 0
            file.write(str(val)+"\t"+str(amp_array[n])+"\t"+str(in_v_array[n])+"\t"+str(phase_array[n])+"\n")
            time.sleep(0.4)
        
        return 1
    
    class oscilioscope:
        def __init__(self, visaObj, visaAddr):
            self._inst = visaObj.open_resource(visaAddr)

        def dev_info(self):
            dev_name = self._inst.query("*IDN?")
            print(dev_name)

        def set_timebase(self, freq):
            """Sets the timebase of the oscilloscope baesd on the given frequency
            Parameters
            ----------
            freq : 
                frequency for timebase to based on.
            Returns
            -------
            None
            """
            period = 1/freq
            scale = period / 2
            self._inst.write(":TIMebase:SCALe " + str(scale))
        
        def set_scale(self, vpp, channel):
            """Sets the channel scale of the oscilloscope baesd on the given VPP
            Parameters
            ----------
            vpp : 
                Voltage of signal from wavegenerator
            channel:
                Channel of oscilloscope to be scaled based on vpp
            Returns
            -------
            None
            """
            self._inst.write(":CHANnel"+str(channel)+":SCALe " + str(vpp/2))
            for i in range(1,4):
                self._inst.write(":CHANnel"+str(i)+":OFFSet " + str(-vpp/2))
        
        def autoscale(self):
            self._inst.write(":AUToscale")
            
        
        def aquire_data(self, type, channel1, channel2 = None):
            if type == "phase":
                return self._inst.query(":MEASure:PHASe? CHANnel"+str(channel1)+",CHANnel"+str(channel2))
            if type == "vpp":
                return self._inst.query(":MEASure:VPP? CHANnel"+str(channel1))
                
        
    class waveGenerator:
        def __init__(self, visaObj, visaAddr):
            self._inst = visaObj.open_resource(visaAddr)
        
        def dev_info(self):
            dev_name = self._inst.query("*IDN?")
            print(dev_name)

        def on(self):
            self._inst.write("OUTPut ON")
        def off(self):
            self._inst.write("OUTPut OFF")

        def set_mode(self, mode):
            self._inst.write("FUNCtion " +str(mode))

        def set_freq(self, freq):
            self._inst.write("FREQuency " + str(freq))

        def set_vpp(self, vpp):
            vpp = float(vpp)
            self._inst.write("VOLTage:HIGH +" + str(vpp))
            self._inst.write("VOLTage:LOW +0.0")
            self._inst.write("VOLTage:OFFSet -" + str(vpp/2))

        def set_waveform(self, waveform):
            if(waveform == "sine" or waveform == "SINE"):
                self._inst.write("FUNCtion SIN")
            if(waveform == "square" or waveform == "SQUARE"):
                self._inst.write("FUNCtion SQU")
    
    class digitMultiMeter:
        def __init__(self, visaObj, visaAddr):
            self._inst = visaObj.open_resource(visaAddr)
    
    class progPowerSupply:
        def __init__(self, visaObj, visaAddr):
            self._inst = visaObj.open_resource(visaAddr)