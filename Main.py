import gammu
from Validations import Validations

def main():
    state_machine = gammu.StateMachine()
    state_machine.ReadConfig()
    state_machine.Init()
    status = state_machine.GetSMSStatus()
    remain = status["SIMUsed"] + status["PhoneUsed"] + status["TemplatesUsed"]
    start = True
    validate = Validations()
    try:
        while remain > 0:
            if start:
                sms = state_machine.GetNextSMS(Start=True, Folder=0)
                start = False
            else:
                sms = state_machine.GetNextSMS(Location=sms[0]["Location"], Folder=0)
            remain = remain - len(sms)
            for m in sms:
                #if m["State"] == "UnRead":
                    print()
                    #print("{:<15}: {}".format("Date", str(m["DateTime"])))
                    #print("{:<15}: {}".format("State", m["State"]))
                    print("{:<15}: {}".format("Number", m["Number"]))
                    print("\n{}: {}".format("Texto", m["Text"]))
                    #metodo de validación.
                    print(validate.ValidationText('Hola mundo'))
    except gammu.ERR_EMPTY:
        print("Failed to read all messages!")

if __name__ == "__main__":
    main()