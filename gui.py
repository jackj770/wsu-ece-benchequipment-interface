import PySimpleGUI as sg
import time 
import labequipment
import numpy as np

labObject = labequipment.labequipment(True)

def dummy_con():
    print("Connecting to deviecs")
    text = ("OSCOPE", "FUNC")
    devices = labObject._autoconnect()
    return devices

test_list = ["FREQRESP", "FREQAT"]

master_size = (400, 150)

layout_button = [
                    [sg.Button('Connect'), sg.Button('Disconnect')],
                    [sg.Text('Not Connected',key='-OSCOPE-')], [sg.Text('Not Connected',key='-FUNC-')]
                ]
                        
layout_test_selection = [
                            [sg.Combo( test_list, default_value=test_list[0], enable_events=True, readonly=True, size=(50, 10), pad=(10,10), key='-TEST_SELECT-')]
                            # [sg.Button("Select Test", key='-TEST-', pad=(10,2))]
                        ]

layoutfreq = [[sg.Text("Frequency Response Test - Performs a frequency sweep from a \nto b and records data from oscilloscope.")],
              [sg.Text("Start Frequency (Hz):"), sg.Input(key='-START_FREQ-', size=(15))],
              [sg.Text("Stop Frequency (Hz):"), sg.Input(key='-STOP_FREQ-', size=(15))],
              [sg.Text("Steps (Int):"), sg.Input(key='-FREQRESP_STEPS-', size=(15))],
            [sg.Text("Vpp (V):"), sg.Input(key='-FREQRESP_VPP-', size=(15))],
              [sg.Button('Run Test'), sg.Button('Stop Test')]]
layoutatfreq = [[sg.Text("Specific Freq Input")],
                [sg.Text("Frequency (Hz):"), sg.Input(key='-SET_FREQ-', size=(15))],
                [sg.Text("Vpp (V):"), sg.Input(key='-SET_VPP-', size=(15))],
                [sg.Button('Set Freqency'), sg.Button('Turn On'), sg.Button('Turn Off')],
                # [sg.Button('All Channel Off')]
                ]

# All the stuff inside your window.
layout = [  [sg.Text('Benchtop Equipment Toolset', font="_14")],
            [sg.Text('Version 0.2')],
            [sg.Frame('Connection Status', layout_button , size=master_size)],
            [sg.Frame('Available Tests', layout_test_selection , size=(400, 70))],
            [sg.Frame('Frequency Response', layoutfreq, size=(400, 300) , key='-FREQRESP-'), sg.Frame('At Response', layoutatfreq, size=master_size ,key='-FREQAT-', visible=False)]
            
            ]

# Create the Window
window = sg.Window('Benchtop Equipment Toolset', layout)
# Event Loop to process "events" and get the "values" of the inputs"
current_test = "FREQRESP"
layout_current = 1
while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Connect':
        status = dummy_con()
        print(status)
        window['-OSCOPE-'].update(status[0])
        window['-FUNC-'].update(status[1])
    if values['-TEST_SELECT-'] != current_test:
        current_test = values['-TEST_SELECT-']
        for x in test_list:
            if x == values['-TEST_SELECT-']:
                window[f'-{x}-'].update(visible=True)
            else:
                window[f'-{x}-'].update(visible=False)
    if event == 'Set Freqency':
        labObject.wavegen.set_freq(values['-SET_FREQ-'])
        labObject.wavegen.set_vpp(values['-SET_VPP-'])
    
    if event == 'Turn On':
        labObject.wavegen.on()
    if event == 'Turn Off':
        labObject.wavegen.off()

    if event == 'Run Test':
        # labObject.frequency_response(100, 2000, 100, 2)
        resp = labObject.frequency_response(values['-START_FREQ-'], values['-STOP_FREQ-'], values['-FREQRESP_STEPS-'], values['-FREQRESP_VPP-'])
        if(resp == 1):
            labequipment.readExisting("bode_plot.txt")
    if event == 'Stop Test':
        labObject.wavegen.off()


window.close()