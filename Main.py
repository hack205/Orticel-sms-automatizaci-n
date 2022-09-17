from re import X
from typing import Text
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
                if m["State"] == "UnRead":
                    print()
                    print("{:<15}: {}".format("Number", m["Number"]))
                    print("\n{}: {}".format("Texto", m["Text"]))
                    isValidate = validate.ValidationText(m["Text"])
                    if(isValidate):
                        print('es valido')
                    else:
                        print('no es valido')
                        message = {
                            'Text': 'Recuerda que el número tiene que tener 10 digitos',
                            'SMSC': {'Location': 1},
                            'Number': m["Number"]
                        }
                        print('mensaje',message)
                    respuesta = state_machine.SendSMS(message)
                    print(respuesta)
    except gammu.ERR_EMPTY:
        print("Failed to read all messages!")

if __name__ == "__main__":
    main()