import serial
import time

ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
gsmStat = []
ser.write('ATE0')
ser.write('\r')
time.sleep(0.5)
print "\x1A"
'''
while gsmStat != 'OK\r\n':
	ser.write("AT")
	ser.write('\r')
	time.sleep(0.5)	
	gsmStat = ser.readline()
	print "gsmStat= ", gsmStat
'''
ser.write('AT+SAPBR=3,1,"Contype","GPRS"')
ser.write('\r')
time.sleep(0.3)
ser.write('AT+SAPBR=3,1,"APN","INTERNET"')
ser.write('\r')
time.sleep(0.3)

gprsStat = []
ser.flushInput()
ser.flushOutput()
#while gprsStat != 'OK\r\n':
while gprsStat != "ERROR\r\n":
        ser.write('AT+SAPBR=1,1')
        ser.write('\r')
        time.sleep(0.5)
        ser.write("AT+SAPBR=2,1")
        ser.write('\r')
        time.sleep(0.5)
        gprsStat = ser.readline()
        print "gprsStat= ", gprsStat

print "hai"

ser.flushInput()
ser.flushOutput()



ser.write("AT+HTTPINIT")
ser.write('\r')
time.sleep(0.3)
ser.write('AT+HTTPPARA="CID",1')
ser.write('\r')
time.sleep(0.3)
url =  "http://bulksms.mysmsmantra.com:8080/WebSMS/SMSAPI.jsp?username=myfloorcs&password=821609184&sendername=MFMART&mobileno=919995221218&message=vineeth"
ser.write('AT+HTTPPARA="URL","http://bulksms.mysmsmantra.com:8080/WebSMS/SMSAPI.jsp?username=myfloorcs&password=821609184&sendername=MFMART&mobileno=919387697077&message=vineeth"')
ser.write('\r')
time.sleep(0.3)
ser.flushInput()
ser.flushOutput()
ser.write('AT+HTTPACTION=1')
ser.write('\r')
time.sleep(0.3)
gsmMsg = []
gsmMsg1 = []
gsmMsg2 = []
ser.flushInput()
ser.flushOutput()

gsmMsg  = []
while True:
        while ser.inWaiting():
		gsmMsg.append(ser.readline())
		print gsmMsg

	try:    
                if gsmMsg :
                        if gsmMsg[1].startswith("+HTTPACTION:1,200"):
                                ser.write("AT+HTTPTERM")
                                ser.write('\r')
                                time.sleep(0.3)
                                gsmMsg = []
        except:
                msg = []
                temp = []
                temp2 = []
                pass
