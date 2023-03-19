import PySimpleGUI as sg
import time 

def dummy_con():
    print("Connecting to deviecs")
    text = ("OSCOPE", "FUNC")
    return text

test_list = ["FREQRESP", "FREQAT"]

master_size = (400, 150)

layout_button = [
                    [sg.Button('Connect'), sg.Button('Disconnect')],
                    [sg.Text(key='-OSCOPE-')], [sg.Text(key='-FUNC-')]
                ]
                        
layout_test_selection = [
                            [sg.Combo( test_list, default_value=test_list[0], enable_events=True, readonly=True, size=(50, 10), pad=(10,10), key='-TEST_SELECT-')]
                            # [sg.Button("Select Test", key='-TEST-', pad=(10,2))]
                        ]

layoutfreq = [[sg.Text("Frequency Response Test - Performs a frequency sweep from a \nto b and records data from oscilloscope.")],
              [sg.Text("Start Frequency (Hz):"), sg.Input(key='-START_FREQ-', size=(15))],
              [sg.Text("Stop Frequency (Hz):"), sg.Input(key='-STOP_FREQ-', size=(15))],
              [sg.Text("Steps (Int):"), sg.Input(key='-FREQRESP_STEPS-', size=(15))],]
layoutatfreq = [[sg.Text("Specific Freq Input")]]

# All the stuff inside your window.
layout = [  [sg.Text('Benchtop Equipment Toolset', font="_14")],
            [sg.Text('Version 0.2')],
            [sg.Frame('Connection Status', layout_button , size=master_size)],
            [sg.Frame('Available Tests', layout_test_selection , size=(400, 70))],
            [sg.Frame('Frequency Response', layoutfreq, size=(400, 300) , key='-FREQRESP-'), sg.Frame('At Response', layoutatfreq, size=master_size ,key='-FREQAT-', visible=False)]
            ]

# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs"
current_test = "FREQRESP"
layout_current = 1
while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    if event == 'Connect':
        status = dummy_con()
        for x in status:
            if x == "OSCOPE":
                window['-OSCOPE-'].update("Oscope Connected")
            if x == "FUNC":
                window['-FUNC-'].update("Function Generator Connected")
    if values['-TEST_SELECT-'] != current_test:
        current_test = values['-TEST_SELECT-']
        for x in test_list:
            if x == values['-TEST_SELECT-']:
                window[f'-{x}-'].update(visible=True)
            else:
                window[f'-{x}-'].update(visible=False)
            


window.close()