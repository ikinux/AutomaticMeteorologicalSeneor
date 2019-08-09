# -*-coding:utf-8-*-

import serial
import time


ser = serial.Serial("com3", 9600, timeout=16)

try:
    ser.open()
except:
    pass

def display_data():
    ser.flushInput()
    data_bytes = ser.read(21)

    # process 4th byte
    byte4 = data_bytes[3]
    byte4_list = bin(byte4)
    bit7 = data_bytes[3] % 2
    bit4 = int(byte4_list[-5])
    bit3 = int(byte4_list[-4])
    bit2 = int(byte4_list[-3])
    bit1 = int(byte4_list[-2])
    bit0 = int(byte4_list[-1])

    wind_dir = data_bytes[2] + 2**8*bit7  # wind direction
    wind_spd = '%.1f' % ((data_bytes[6] + 2**8*bit4)/8 * 1.12)  # wind speed
    temp = '%.1f' % ((data_bytes[4] + 2**8*bit0 + 2**9*bit1 + 2**10*bit2)/10 - 40)  # temperature
    humi = data_bytes[5]  # humidity(%)
    gust = '%.1f' % (data_bytes[7] * 1.12)  # gust speed
    rain = '%.1f' % (((data_bytes[8] * 2**8 + data_bytes[9])) * 0.3)  # rain(mm)
    uv = data_bytes[10] * 2**8 + data_bytes[11]  # ultraviolet(uW/cm²)
    light = (data_bytes[12] * 2**16 + data_bytes[13] * 2**8 + data_bytes[14])/10  # light(lux)
    pressure = (data_bytes[17] * 2**16 + data_bytes[18] * 2**8 + data_bytes[19])/100  # pressure(hpa)
    batt = '正常'

    if bit3 == 1:
        batt = '低' 

    uvi = 0
    if 433 <= uv < 851:
        uvi = 1
        if 853 <= uv < 1210:
            uvi = 2 
            if 1211 <= uv < 1570:
                uvi = 3
                if 1571 <= uv < 2017:
                    uvi = 4
                    if 2018 <= uv < 2450:
                        uvi = 5
                        if 2451 <= uv < 2761:
                            uvi = 6
                            if 2762 <= uv < 3100:
                                uvi = 7
                                if 3101 <= uv < 3512:
                                    uvi = 8
                                    if 3513 <= uv < 3918:
                                        uvi = 9
                                        if 3919 <= uv < 4277:
                                            uvi = 10
                                            if 4278 <= uv < 4650:
                                                uvi = 11
                                                if 4651 <= uv < 5029:
                                                    uvi = 12
                                                    if uv >= 5230:
                                                        uvi = 13

    uvi2 = (uv * 10)%25


    print('时间：' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('风速：' + str(wind_spd) + 'm/s')
    print('风向：' + str(wind_dir) + '°')
    print('16秒平均风速：' + str(gust) + 'm/s')
    print('温度：' + str(temp) + '℃')
    print('湿度：' + str(humi) + '%')
    print('降水量：' + str(rain) + 'mm')
    print('紫外线辐射强度：' + str(uv) + 'uW/cm²')
    print('紫外线指数：' + str(uvi))
    #print('紫外线指数（WMO）：' + str(uvi2))
    print('光照强度：' + str(light) + 'lux')
    print('压强：' + str(pressure) + 'hPa')
    print('电池电量：' + batt)
    print('———————————————')

display_data()

while True:
    try:
        display_data()
    except:
        pass




