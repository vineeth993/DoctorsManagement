import serial
import time
import os
import datetime

ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
gsmStat = 'ERROR'
ser.write('ATE0')
ser.write('\r')
time.sleep(0.5)
print "x1A"
while gsmStat != 'OK\r\n':
        ser.write("AT")
        ser.write('\r')
        #time.sleep(0.5)        
        gsmStat = ser.readline()
        print gsmStat
       
print "hai"
ser.write('AT+CSCS="GSM"')
ser.write('\r')
time.sleep(0.5)
ser.write("AT+CMGF=1")
ser.write('\r')
time.sleep(0.5)
ser.write('AT+CMGD="ALL"')
ser.write('\r')
time.sleep(0.5)
ser.write("AT+CNMI=1,2,0,0,0")
ser.write('\r')
time.sleep(0.5)
ser.flushInput()
ser.flushOutput()
msg = []
ser.write('AT+CMGS="53733"')
ser.write('\r')
time.sleep(0.2)
ser.write("DATA 2G")
ser.write('\r')
ser.write("\x1A")
ser.write('\r')
while True:
        while ser.inWaiting():
                msg.append(ser.readline())
                

        try:    
                if msg :
                        temp =  msg[1].split(',')
                        temp2 = temp[0].split(":")
                        if temp2[0] == "+CMT" :
                                print msg
                                date1 = "20"+temp[2].replace('"', '')
                                time1 = temp[3].replace('"', '').split("+")[0]
                                date1 = datetime.datetime.strptime(date1, '%Y/%m/%d').date()
                                time1 = datetime.datetime.strptime(time1, '%H:%M:%S').time()
                                print date1
                                print time1
                                #print "message = ", msg[2]
                                #print "number = ", temp2[1]
                                break
                        msg = []
                        temp = []
                        temp2 = []
        except:
                msg = []
                temp = []
                temp2 = []
                pass




