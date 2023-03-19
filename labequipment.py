import pyvisa
import config

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
        if len(avail_dev) != 0:
            print("Found %i devices. Some of these devices may not be test equipment." % len(avail_dev))
        
            for i, n in enumerate(avail_dev):
                try:
                    dev = rm.open_resource(n)
                    self._availableDevices[i] = n 
                    dev_name = dev.query("*IDN?")
                    if dev_name.split(",")[1] == "DSOX1204G":
                        self.oscope = self.oscilioscope(rm, n)
                    if dev_name.split(",")[1] == "EDU33212A":
                        self.wavegen = self.waveGenerator(rm, n)
                    if self.verbose:
                        print("Device: %i" % i)
                        print("Device Information: %s" % dev_name.split(",")[1])
                        
                except:
                    continue

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

    def frequency_reponse(start_freq, stop_freq, steps, Vpp):
        return 0
    
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
            self._inst.write("VOLTage:HIGH +" + str(vpp))
            self._inst.write("VOLTage:LOW +0.0")
            self._inst.write("VOLTage:OFFSet -" + str(vpp/2))
    
    class digitMultiMeter:
        def __init__(self, visaObj, visaAddr):
            self._inst = visaObj.open_resource(visaAddr)
    
    class progPowerSupply:
        def __init__(self, visaObj, visaAddr):
            self._inst = visaObj.open_resource(visaAddr)