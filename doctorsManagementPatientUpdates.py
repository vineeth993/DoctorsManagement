#!/bin/python

import datetime

class patientUpdate():

    def __init__(self, dbObj):
        self.dbData = dbObj
        doctorsConfig = self.dbData.tableSelect("Doctors")[0]
        self.noOfPatients = doctorsConfig[0]
        self.examinationTime = int(doctorsConfig[1])
        self.emgNumber = doctorsConfig[2]
        self.consultationtime = doctorsConfig[3]
        self.notConsulting = doctorsConfig[4]
        self.noOfDays = doctorsConfig[5]
        self.consultationFinish = doctorsConfig[6]
        self.smsHeader = doctorsConfig[7]
        self.deletionTime = self.timeAddition(self.consultationFinish, 3600)
    '''    
    def paitentDataCheckAndUpdate(self, name, phoneNumber, date, time):
        presentTime, todayDate = self.getDateTime()
        name = name.replace("\r\n","")
        originalDate, originalTime = self.dateTimeConvertion(date, time)
        value = None
        if originalDate == todayDate:
            condition = "PhoneNumber="+phoneNumber
            value = self.dbData.tableSelect("Patients", condition)
            #if not value:
            token, time = self.getPatientData("Patients")
            if not token and not time:
                token = 1
                time = str(self.consultationtime)
                stat = "Data base Updated \r\n"
                self.dbData.tableInsertion("Patients", (token, str(time), name, phoneNumber, str(originalTime), str(originalDate)))
            else:
                token = int(token)
                token += 1 
                if token > self.noOfPatients:
                    stat = "Token Exceeds \r\n"
                else:
                    stat = "Data base Updated \r\n"
                    updatedTime = self.timeAddition(time, 300)
                    self.dbData.tableInsertion("Patients", (token, str(updatedTime), name, phoneNumber, str(originalTime), str(originalDate)))
            
        else:
            stat = "Date Not Correct \r\n"
        #self.logging(name, str(originalDate), str(originalTime), stat)
        print "hai"
        return value
    '''
    
    def doctorsUpdate(self, message, phoneNumber, date, time):
        presentTime, todayDate = self.getDateTime()
        originalDate, originalTime = self.dateTimeConvertion(date, time)
        if originalDate == todayDate and phoneNumber == self.emgNumber:
            self.dbData.tableDeletion("Patients", "1")
            self.dbData.tableDeletion("PatientsTransaction", "1")
            self.dbData.tableDeletion("DoctorTransaction", "1")
            token, _ = self.getPatientData("PatientsMessage")
            if message == "Cancelled\r\n":
                self.dbData.tableInsertion("DoctorTransaction", (True, "00:00:00"))
                stat =  None
            else:
                date, message = self.dateTimeConvertion(date, str(message.replace("\r\n","")))
                self.dbData.tableInsertion("DoctorTransaction", (False, str(message)))
                stat =  token
        return stat
                                                             
    def getDateTime(self):
        dateTime = datetime.datetime.now()
        date = dateTime.date()
        time = dateTime.time()
        return time, date
    
    def timeAddition(self, time,additive):
        dateTime = time + datetime.timedelta(0, additive)
        return dateTime
    
    def getPatientData(self, table):
        token = self.dbData.tableSelect(table, "last", "Token")[0][0]
        if table == "Patients":
            time = self.dbData.tableSelect(table, "last", "Time")[0][0]
        else:
            time = None
        return token, time

    def dateTimeConvertion(self, date1, time1):
        print "time = ",type(time1)
        print "date = ", date1
        if date1:
            gsmDate = datetime.datetime.strptime(date1, '%Y/%m/%d').date()
        else:
            gsmDate = None
        gsmTime = datetime.datetime.strptime(time1, '%H:%M:%S').time()
        print "gsmTime = ", gsmTime
        return gsmDate, gsmTime
        
    def logging(self, name, date, time, stat):
        logFile = open("updates.log", "a")
        logFile.write("***__________UPDATES__________*** \r\n")
        logFile.write("Name = ")
        logFile.write(name + "\r\n")
        logFile.write("Date = ")
        logFile.write(str(date) + "\r\n")
        logFile.write("Time = ")
        logFile.write(str(time) + "\r\n")
        logFile.write("Status = ")
        logFile.write(stat)
        logFile.close()

    def transactionalToken(self):
        token, time = self.getPatientData("Patients")
        token1, time1 = self.getPatientData("PatientsTransaction")
        if token1 != token:
            if not token1:
                token1 = 1
            else:
                token1 = token1 + 1
            condition = "Token="+str(token1)
            value = self.dbData.tableSelect("Patients", str(condition))[0]
            if value:
                patientToken = value[0]
                patientTime = value[1]
                patientName = value[2]
                patientPhNumber = value[3]
                return patientToken, patientTime, patientName, patientPhNumber
            else:
                return None, None, None, None
        else:
            return None, None, None, None


    def patientsTimeAddition(self):
        isCancelled = False
        token, time = self.getPatientData("Patients")
        msgToken, _ = self.getPatientData("PatientsMessage")
        data = self.dbData.tableSelect("DoctorTransaction")
        if data:
            if data[0][1] != "00:00:00":
                self.consultationtime = data[0][1]
            isCancelled = data[0][0]
        if not token and not time:
            token = 1
            time = self.consultationtime
        else:
            token += 1
            time = self.timeAddition(time, self.examinationTime*60)
        condition = "Token="+str(token)
        value = self.dbData.tableSelect("PatientsMessage", str(condition))
        if value:
            if isCancelled:
                time = "00:00:00"
                stat = "Cancelled"
            elif token == self.noOfPatients and time >= self.consultationFinish:
                time = "00:00:00"
                stat = "ConsultationCompleted"
            else:
                stat = None
            self.dbData.tableInsertion("Patients",(int(token), str(time), value[0][1], value[0][2], str(value[0][3]), str(value[0][4])))
        else:
            stat = None
        return stat
                
    def patientDbUpdate(self, name, phoneNumber, date, time):
        presentTime, todayDate = self.getDateTime()
        name = name.replace("\r\n","")
        print name, phoneNumber
        originalDate, originalTime = self.dateTimeConvertion(date, time)           
        if originalDate == todayDate:
            condition = "PhoneNumber="+phoneNumber
            value = self.dbData.tableSelect("PatientsMessage", condition)
            #if not value:
            token, time = self.getPatientData("PatientsMessage")
            if not token:
                token = 1
                self.dbData.tableInsertion("PatientsMessage", (int(token), name, phoneNumber, str(originalTime), str(originalDate)))
            else:
                token = int(token)
                token += 1 
                stat = "Data base Updated \r\n"
                self.dbData.tableInsertion("PatientsMessage", (int(token), name, phoneNumber, str(originalTime), str(originalDate)))

    def patientDoctorDbClearance(self):
        time, date = self.getDateTime()
        if str(self.deletionTime) >= str(time):
            self.dbData.tableDeletion("PatientsMessage", "1")
            self.dbData.tableDeletion("Patients", "1")
            self.dbData.tableDeletion("PatientsTransaction", "1")
            self.dbData.tableDeletion("DoctorTransaction", "1")
