import multiprocessing
import time
from csv import writer
import os
import csv
import numpy as np
import sys

print('Monitoring starting below...')
print('Battery capacity set to',sys.argv[2])

if len(sys.argv[1])>2:
    print('Writing data into file',sys.argv[1])
#from codecarbon import EmissionsTracker

import psutil
#cpu_control = psutil.cpu_percent()

def get_battery_charge():
    battery = psutil.sensors_battery()
    charge = battery.percent
    #print('Battery percent',charge,'%')
    return(charge)
'''
def get_cpu_temp():
    temp = psutil.sensors_temperatures()
    res = []
    for k in range(4):
        res.append(temp['coretemp'][k+1][1])
    #print('Temperature of CPU',res)
    return(res)

def get_cpu_percent():
    #print('Percentage of CPU used',psutil.cpu_percent(percpu=True))
    return(res)
'''
def monitore():
    #res = {'temp':[],'percent':[]}
    k = 0
    previouscharge = 100
    periode = 10#in seconds
    result = []
    study_time = 3#en heure
    stop_crit = (60/periode)*60*study_time
    while True and k<stop_crit:
        #96000 = 12000*8heures = (60/periode)parminute*60min*8h
        #res['percent'].append(get_percent())
        #res['temp'].append(get_temp())
        currentcharge = get_battery_charge()
        #cpu_temp = get_cpu_temp()
        #cpu_percent = get_cpu_percent()
        BT_Wh = float(sys.argv[2])#condition of battery in Wh, given by command inxi -B (ubuntu or mac os)
        power_est = 36*(previouscharge - currentcharge)*BT_Wh/periode
        #energy_consumption = 52*(difference/100) (en Wh)
        #power_est = 3600*energy_consumption/periode (en Watt car periode est le temps entre deux mesures en seconde)
        if k>0:
            result.append(power_est)
            print('Current charge',currentcharge,'%')
        #exp_percentage = 100*k/stop_crit
        if k>0:
            print(k,'| Power estimation =',round(power_est,1),'W')
        previouscharge = currentcharge
        k += 1
        time.sleep(periode)
    if len(sys.argv[1])>2:
        np.savetxt(sys.argv[1], result)


if __name__ == '__main__':
    p1 = multiprocessing.Process(name='p1', target=monitore)
    p1.start()