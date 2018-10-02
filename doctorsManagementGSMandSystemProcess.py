import serial
import time
import os
import doctorsManagementPatientUpdates
import doctorsManagementDBProcess

class gsmSystemProcess():

    def __init__(self):
        #threading.Thread.__init__(self)
        self.dbData = doctorsManagementDBProcess.dbManagement()
        self.gsmSer = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
        self.tempGsmMsg = None
        self.gprsStat = "Deactivated"
        self.dbValueStat = "Nil"
        self.httpReadStatus = "notCompleted"
        self.dbUpdateStat = False
        self.shieldCommands()
        self.shieldGPRSCommands()
        self.shieldInit()
        self.tokenStat = 1
        self.tokenValue = None
        self.patientUpdates = doctorsManagementPatientUpdates.patientUpdate(self.dbData)

    def shieldInit(self):
        #self.shieldWrite(self.gsmEchoOff)
        gsmStat= 'ERROR'
        while gsmStat != 'OK\r\n':
            self.shieldWrite(self.gsmTest)
            gsmStat = self.shieldRead()
            print "gsmStat = ", gsmStat
        self.shieldWrite(self.gsmSleepMode)
        self.shieldWrite(self.gsmMode)
        self.shieldWrite(self.gsmTxtMode)
        self.shieldWrite(self.gsmDeleteMsg)
        self.shieldWrite(self.gsmRecvMsg)
        #self.shieldGetDateTimeMsg()
        self.shieldFlush()
        self.shieldGprsInit()
        self.shieldFlush()
        
    def shieldGprsInit(self):
        gprsStat = None
        self.shieldWrite(self.gsmGPRS)
        self.shieldWrite(self.gsmApnSet)
        self.shieldFlush()
        '''
        while gprsStat != "OK\r\n":
            self.shieldWrite(self.gsmGprsEnable)
            gprsStat = self.shieldRead()
            if gprsStat != "OK\r\n":
                self.shieldWrite(self.gsmGprsTerm)
            print "gprsStat = ", gprsStat
        '''
        self.shieldWrite(self.gsmHttpEnable)
        self.shieldWrite(self.gsmBearerProfile)
        self.shieldFlush()
            
                
    def shieldCommands(self):
        self.gsmEchoOff =    "ATE0"
        self.gsmTest    =    "AT"
        self.gsmMode    =    'AT+CSCS="GSM"'
        self.gsmTxtMode =    "AT+CMGF=1"
        self.gsmDeleteMsg=   'AT+CMGD="ALL"'
        self.gsmRecvMsg  =   "AT+CNMI=1,2,0,0,0"
        self.gsmClock    =   "AT+CCLK?"
        self.gsmSleepMode=   "AT+CSCLK=2"
        self.gsmSndMsg   =   "AT+CMGS="
        self.msgTermination= "\x1A"

    def shieldGPRSCommands(self):
        self.gsmGPRS        = 'AT+SAPBR=3,1,"Contype","GPRS"'   
        self.gsmApnSet      = 'AT+SAPBR=3,1,"APN","INTERNET"'
        self.gsmGprsEnable  = 'AT+SAPBR=1,1'
        self.gsmHttpEnable  = 'AT+HTTPINIT'
        self.gsmBearerProfile='AT+HTTPPARA="CID",1'
        self.gsmHttpCommit  = 'AT+HTTPACTION=1'
        self.gsmGprsRead    = 'AT+HTTPREAD'
        self.gsmHttpPost    = 'AT+HTTPPARA="URL",'
        self.gsmHttpTerm    = 'AT+HTTPTERM'
        self.gsmGprsTerm    = 'AT+SAPBR=0,1'
        self.gsmIp          = 'AT+SAPBR=2,1'
        
    def shieldWrite(self, commands):
        self.gsmSer.write(commands)
        self.gsmSer.write("\r")
        time.sleep(0.5)

    def shieldRead(self):
        gsmAck = self.gsmSer.readline()
        return gsmAck

    def shieldFlush(self):
        self.gsmSer.flushInput()
        self.gsmSer.flushOutput()

    def shieldDataParsing(self):
        gsmMsg = []
        while self.gsmSer.inWaiting():
            gsmMsg.append(self.shieldRead())
            
        try:
            if gsmMsg:
                print gsmMsg
                gsmTemp = gsmMsg[1].split(",")
                gsmTemp2 = gsmTemp[0].split(":")

                if gsmTemp2[0]== "+CMT":
                    phoneNumber = gsmTemp2[1].replace('"', '')
                    phoneNumber = phoneNumber.replace(" ", "")
                    date, time  = self.shieldDateTimeExtraction(gsmTemp)
                    if gsmMsg[2].startswith("Dr ") or gsmMsg[2].startswith("PP "):
                        nameTemp = gsmMsg[2].split(" ")
                        if len(nameTemp) > 2:
                            name = nameTemp[len(nameTemp)-1]
                        else:
                            name = nameTemp[1]
                        if gsmMsg[2].startswith("Dr "):
                            self.patientUpdates.patientDbUpdate(name, phoneNumber, date, time)                      
                        elif gsmMsg[2].startswith("PP "):
                            print "hai in doctorsUpdate"
                            self.tokenValue = self.patientUpdates.doctorsUpdate(name, phoneNumber, date, time)
                    elif phoneNumber == "BT-BSNLKR":
                        self.systemDateTimeUpdate(date, time)

                elif gsmMsg[1].startswith("+HTTPACTION:1,200"):
                    print "httpSend"
                    #self.gsmTempMsg = gsmTemp2[0]
                    self.shieldWrite(self.gsmGprsRead)
                elif gsmMsg[1] ==  '+SAPBR 1: DEACT\r\n':
                    print "in sapbr"
                    self.gprsStat = "Deactivated"
                elif gsmMsg[1].startswith("+SAPBR: 1,1"):
                    self.gprsStat = "Activated"
                elif gsmMsg[1].startswith("+HTTPREAD:"):
                    print "httpRead = ",gsmMsg[2]
                    tempMsg = gsmMsg[2]
                    gsmMsg = []
                    self.gsmMsgProcess(tempMsg)
                        
                gsmMsg   = []
                gsmTemp  = []
                gsmTemp2 = []
                nameTemp = []
                #self.shieldFlush()
        except:
            gsmMsg   = []
            gsmTemp  = []
            gsmTemp2 = []
            nameTemp = [] 
            self.shieldFlush()
            pass

    def shieldDateTimeExtraction(self, data):
        date = "20"+data[2].replace('"', '')
        time = data[3].replace('"', '').split("+")
        time = time[0]
        return date, time

    def systemDateTimeUpdate(self, date, time):
        dateCommand = "date +%D -s "+date
        timeCommand = "date +%T -s "+time
        os.system(dateCommand)
        os.system(timeCommand)

    def shieldGetDateTimeMsg(self):
        self.shieldWrite(self.gsmSndMsg +'"53733"')
        self.shieldWrite("DATA 2G")
        self.shieldWrite(self.msgTermination)

    def sheildGprsActivate(self):
        if self.gprsStat == "Deactivated":
            print "GPRS Activation Started = "
            self.shieldWrite(self.gsmGprsEnable)
            self.shieldFlush()
            self.shieldWrite(self.gsmIp)
        
    def shieldSendMsg(self, message=None, phoneNumber=None):
        self.dbUpdateStat = True
        msgApi = "http://bulksms.mysmsmantra.com:8080/WebSMS/SMSAPI.jsp?username=""&password=""&sendername=""&mobileno="+phoneNumber+"&message="+message
        print "msgApi = ", msgApi
        print "msgCommand = ",self.gsmHttpPost + '"'+msgApi+'"'
        self.shieldWrite(self.gsmHttpPost + '"'+msgApi+'"')
        self.shieldFlush()
        time.sleep(0.5)
        self.shieldWrite(self.gsmHttpCommit)
        self.shieldFlush()
        
    def takeTokenAndTime(self): 
        self.token, self.time, self.name, self.phoneNumber = self.patientUpdates.transactionalToken()
        if self.token and  self.name and self.phoneNumber:
            if self.tokenValue and self.tokenValue != self.tokenStat:
                message = "postponed Token="+str(self.token)+",Time="+str(self.time)
                self.tokenStat += 1
            elif self.cancelMessage == "ConsultationCompleted":
                message = "Today Consultation Completed Please Visit tommorrow"
            elif self.cancelMessage == "Cancelled":
                message = "Cancelled"
            else:
                message = "Name="+self.name+",Token="+str(self.token)+",Time="+str(self.time)
                self.tokenStat = 1
                self.cancelMessage = None
                self.tokenValue = None
            phoneNumber = self.phoneNumber.replace("+","")
            self.dbValueStat = "Value"
        else:
            self.tokenStat = 1
            self.tokenValue = None
            self.dbValueStat = "Nil"
            self.token = None
            self.time = None
            self.name = None
            self.phoneNumber = None
            message = None
            phoneNumber = None
        return message, phoneNumber
            

    def gsmMsgProcess(self, message):
        if message.startswith("DND"):
            print "in DnD"
            self.dbData.tableInsertion("PatientsTransaction", (int(self.token), str(self.time), self.name, self.phoneNumber, False))
        elif message.startswith("Your message is successfully sent to"):
            self.dbData.tableInsertion("PatientsTransaction", (int(self.token), str(self.time), self.name, self.phoneNumber, True))
        self.dbUpdateStat = False
    
    def shieldStart(self):
        while True:
            self.shieldDataParsing()
            self.sheildGprsActivate()
           # print self.shieldRead()
            self.cancelMessage = self.patientUpdates.patientsTimeAddition()
            message, phoneNumber = self.takeTokenAndTime()
            #self.patientUpdates.patientDoctorDbClearance()
            if  self.gprsStat == "Activated" and not self.dbUpdateStat and self.dbValueStat=="Value": 
                print "message = ", message
                self.shieldSendMsg(message, phoneNumber)
                
gsm = gsmSystemProcess()
gsm.shieldStart()
