if not isCancelled :
            if token != msgToken :
                if not token and not time:
                    token = 1
                    time = self.consultationtime
                else:
                    token += 1
                    time = self.timeAddition(time, self.examinationTime*60)
                if time != None:
                    if time <= self.consultationFinish and token != self.noOfPatients:
                        condition = "Token="+str(token)
                        value = self.dbData.tableSelect("PatientsMessage", str(condition))[0]
                        self.dbData.tableInsertion("Patients",(int(token), str(time), value[1], value[2], str(value[3]), str(value[4])))
                        stat    = None
                    else:
                        stat = "ConsultationCompleted"
                else:
                    condition = "Token="+str(token)
                    value = self.dbData.tableSelect("PatientsMessage", str(condition))[0]
                    self.dbData.tableInsertion("Patients",(int(token), str(time), value[1], value[2], str(value[3]), str(value[4])))
                    stat = None
            else:
                stat = None
                
        else:
            #time = "000:00:00"
            #self.dbData.tableInsertion("Patients",(int(token), str(time), value[1], value[2], str(value[3]), str(value[4])))
            stat = "Cancelled"
        return stat
