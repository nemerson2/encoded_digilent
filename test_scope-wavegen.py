from WF_SDK import device, scope, wavegen, tools, error   # import instruments
import matplotlib.patches
import numpy as np
import serial
import pandas as pd
import matplotlib.pyplot as plt   # needed for plotting
import matplotlib
from time import sleep            # needed for delays

"""-----------------------------------------------------------------------"""
    # connect to the device
device_data = device.open()
"""-----------------------------------"""

# handle devices without analog I/O channels
if device_data.name != "Digital Discovery":

    # initialize the scope with default settings
    scope.open(device_data, sampling_frequency=1000000, buffer_size=10000)

    # set up triggering on scope channel 1
    scope.trigger(device_data, enable=True, source=scope.trigger_source.analog, channel=1, level=0) #Note the trigger level is 0 so all recorded waveforms start at y=0

    # generate a 10KHz sine signal with 2V amplitude on channel 1
    wavegen.generate(device_data, channel=1, function=wavegen.function.sine, offset=0, frequency=2000, amplitude=2)

    # sleep(1)    # wait 1 second


def write_scope(comport, baudrate, scan_res, enc1_res, scan_length, idx_res, enc2_res, idx_length):
    # record data from Digilent with the scopeon channel 1
    enc1=0 #reset encoder1
    enc2=0 #reset encoder2
    ser = serial.Serial(comport, baudrate, timeout=0.05) #initialize serial port   
    
    #Initialize dictionary for storing data
    column_names = []
    for i in range(0,scan_length+1):
        for j in range(0,idx_length+1):
            column_names.append(str(i)+','+str(j))
    print(len(column_names))
    values = [0]*len(column_names)
    pairs = zip(column_names, values)
    my_dict = dict(pairs)

    # #initialize surface plot for c-scan info
    plt.ion()
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, scan_length)
    ax.set_ylim(0, idx_length)
    ax.set_xlabel('Scan (mm)')
    ax.set_ylabel('IDX (mm)')
    mgr1 = plt.get_current_fig_manager()
    mgr1.window.geometry("+1000+300")
    

    # initialize plot of scope
    x = range(0,10000)
    y = [0]*10000
    plt.ion()
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    ax2.set_xlim(0, 1000)
    ax2.set_ylim(-5,5)
    ax2.set_xlabel('samples')
    ax2.set_ylabel('signal')
    mgr2 = plt.get_current_fig_manager()
    mgr2.window.geometry("+10+10")
    line2, = ax2.plot(x , y)

    try:
        while True:
            buffer = scope.record(device_data, channel=1) #read Digilent buffer

            # get encoder data from Arduino Serial
            enc_data = ser.readline().decode().strip()
            
            #store the data to the proper location in the dictionary
            if enc_data:
                if enc_data[7]=='1': #if first encoder is moving
                    enc1= float(enc_data[9:])
                    if enc1 % enc1_res ==0:   
                        my_dict[str(int(enc1/enc1_res))+','+str(round(enc2/enc2_res))]=buffer #store digilent buffer at current positional location
                        rect = matplotlib.patches.Rectangle([enc1/enc1_res,round(enc2/enc2_res)],scan_res,idx_res) #update 'c-scan' plot
                        fig.gca().add_patch(rect)
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        print('Scan Value: ')
                        print(enc1/enc1_res)


                        line2.set_ydata(buffer)
                        fig2.canvas.draw()
                        fig2.canvas.flush_events()

                        
                if enc_data[7]=='2': #if second encoder is moving
                    enc2=float(enc_data[9:])
                    if enc2 % enc2_res == 0:
                        my_dict[str(round(enc1/enc1_res))+','+str(int(enc2/enc2_res))]=buffer
                        rect = matplotlib.patches.Rectangle([round(enc1/enc1_res),enc2/enc2_res],scan_res,idx_res)
                        fig.gca().add_patch(rect)
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                        print('Index Value: ')
                        print(enc2/enc2_res)

                        line2.set_ydata(buffer)
                        fig2.canvas.draw()
                        fig2.canvas.flush_events()  

    except KeyboardInterrupt:
        df = pd.DataFrame(my_dict)
        df.to_excel('C:/Users/nathan_emerson/Desktop/Resonance_Probe/test.xlsx')
        # print(df)
        # plt.plot(my_dict['1,1'])  
        # plt.show()
    #  # Write data to external file
    #     dat = np.array(buffer)
    #     df = pd.DataFrame(dat, dtype=np.float16)
    #     df.columns=['values']
    #     df.to_csv('C:/Users/nathan_emerson/Desktop/Resonance_Probe/test.csv',mode='a')
    #     # reset the scope

if __name__=="__main__":
    write_scope('COM3',9600, 1, 100,10, 1, 50, 7)


scope.close(device_data)

# reset the wavegen
wavegen.close(device_data)


# close the connection
device.close(device_data)

# except error as e:
#     print(e)
#     # close the connection
#     device.close(device.data)
