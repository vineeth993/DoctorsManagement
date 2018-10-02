import serial

ser = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
gsmStat = 'ERROR'
ser.write('ATE0')
ser.write('\r')
time.sleep(0.5)


def test():
    
