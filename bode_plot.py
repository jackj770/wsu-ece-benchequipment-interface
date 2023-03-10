import matplotlib.pyplot as plt
import numpy as np
import time 

import keyoscacquire as koa
import wavegen



start_freq = 0
stop_freq = 0
step_freq = 0
freq_array = []
amp_array = []
in_v_array = []
phase_array = []







def getNewData():    
    Hunt = False
    auto_proceed = False
    try:
        print("Connecting to Scope...")
        scope = koa.Oscilloscope(address='')
        scope.acq_type = 'AVER8'
    except:
        print("Failed to connect. Check connections and try again")
        exit()
    # try:
    print("Connecting to Function Generator...")
    gen = wavegen.Wavegen(address='') 
    # except:
    #     print("Failed to connect. Check connections and try again")
    #     exit() 

    # prompt user for freq range
    start_freq =  float(input("Start Frequecny: "))
    stop_freq = float(input("Stop Frequecny: "))
    step_freq = float(input("Frequency Increment: "))

    if input("Enable intelli-auto scaling? y or n:  ") == "y":
        Hunt = True
    if input("Enable auto-proceed? y or n:  ") == "y":
        auto_proceed = True


    num_of_int = (stop_freq - start_freq) / step_freq

    freq_array = np.arange(start_freq, stop_freq + step_freq, step_freq)
    # print(freq_array)

    amp_array = np.zeros(len(freq_array))
    in_v_array = np.zeros(len(freq_array))
    phase_array = np.zeros(len(freq_array))


    file = open("bode_plot.txt", "w")

    file.write(str(start_freq)+"\n")
    file.write(str(stop_freq)+"\n")
    file.write(str(step_freq)+"\n\n")

    print("Setting up equipment according to parameters...")
    gen.write("FUNCtion SIN")
    gen.write("FREQuency +" + str(start_freq))
    gen.write("VOLTage:HIGH +0.6")
    gen.write("VOLTage:LOW +0.0")
    gen.write("VOLTage:OFFSet -0.3")
    gen.write("PHASe +0.0")
    gen.write("SYSTem:BEEPer[:IMMediate]")
    time.sleep(0.25)
    gen.write("SYSTem:BEEPer[:IMMediate]")
    gen.write("OUTPut ON")
    
    
    timebase = 0.001

    for n, val in enumerate(freq_array):
        gen.write("FREQuency +" + str(val))
        if not auto_proceed:
            input("Press enter to capture data at freq: " + str(val))
        else:
            gen.write("SYSTem:BEEPer[:IMMediate]")
            print("Next data capture at freq: " + str(val))
        if Hunt:
            scope.write(":TIMebase:SCALe " + str(timebase))
            phase = abs(float(scope.query(":MEASure:PHASe? CHANnel1,CHANnel2")))
            checks = 10
            avg = np.zeros(checks)
            for ii in range(checks):
                phase = abs(float(scope.query(":MEASure:PHASe? CHANnel1,CHANnel2")))
                avg[ii] = phase
            std = np.std(avg)
            print("std:", std)
            while std > 10:
                print("Adjusting timebase...")
                timebase = timebase * 0.5
                scope.write(":TIMebase:SCALe " + str(timebase))
                avg = 0.001
                
                avg = np.zeros(checks)
                for jj in range(checks):
                    phase = abs(float(scope.query(":MEASure:PHASe? CHANnel1,CHANnel2")))
                    avg[jj] = phase
                    print(phase)
                    # time.sleep(0.2)
                std = np.std(avg)
                print("std: "+ str(std))


        
        # temp = input("input voltage:")
        # if temp == '':
        #     in_v_array[n] = in_v_array[n-1]
        # else:
        #     in_v_array[n] = temp
        print("Aquiring Data....")

        in_v_array[n] = float(scope.query(":MEASure:VPP? CHANnel1"))
        time.sleep(0.25)
        amp_array[n] = float(scope.query(":MEASure:VPP? CHANnel2"))
        time.sleep(0.25)
        phase_array[n] = float(scope.query(":MEASure:PHASe? CHANnel1,CHANnel2"))
        time.sleep(0.25)
        if phase_array[n] > 180 or phase_array[n] < -180:
            phase_array[n] = 0
        

        

        # amp_array[n] = input("output voltage:")
        # phase_array[n] = input("phase:")
        file.write(str(val)+"\t"+str(amp_array[n])+"\t"+str(in_v_array[n])+"\t"+str(phase_array[n])+"\n")
    
    print("Done. Writing to " + "bode_plot.txt")
    file.close()
    gen.write("OUTPut OFF")
    gen.write("SYSTem:BEEPer[:IMMediate]")
    time.sleep(0.25)
    gen.write("SYSTem:BEEPer[:IMMediate]")
    time.sleep(0.25)
    gen.write("SYSTem:BEEPer[:IMMediate]")

def readExisting(filename):
   #open the file
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

    return np.array(freq_array) , np.array(db), np.array(phase_array)
                
            


        




# curve = np.polyfit(freq_array, db, 15)

# plt.semilogx(freq_array, curve)


if __name__ == "__main__":
    print("\nBode Plot AutoPlotter v0.4")
    print("Written by Jack Fernald")
    print("Feb. 2023\n")
    freq_meas = 0
    mag_meas = 0
    phase_meas = 0
    prompt = input("\nEnter new data(yes) or plot from existing(no)? (yes or no)")
    if prompt == "yes":
        getNewData()
        freq_meas, mag_meas, phase_meas = readExisting("bode_plot.txt")
    elif prompt == "no":
        freq_meas, mag_meas, phase_meas = readExisting("bode_plot.txt")

    print(freq_meas)
    print(mag_meas)
    print(phase_meas)
    for i in freq_meas:
        print("%f, " % i, end='')
    for i in mag_meas:
        print("%f, " % i, end='')
    for i in phase_meas:
        print("%f, " % i, end='')   

    fig, axs = plt.subplots(2, sharex=True)
    axs[0].semilogx(freq_array, mag_meas)
    axs[0].set_title("Magnitude Response")
    axs[0].set(ylabel = "Magnitude (dB)")
    axs[0].grid()
    axs[1].plot(freq_meas, phase_meas)
    axs[1].set(ylabel = "Phase (Radians)")
    axs[1].grid()
    plt.show()