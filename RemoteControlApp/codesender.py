from typing_extensions import Protocol
from rpi_rf import RFDevice
from mylogger import logger
from outletdefinitions import outlets

def sendCode(buttonNumber,state):
    pulse = 185
    validButton = next((sub for sub in outlets if sub['buttonNumber'] == buttonNumber), None)
    if(validButton == "None"):
        return

    if state == 'off':
        code = validButton['codeOff']
    elif state == 'on':
            code = validButton['codeOn']

    logger.info("Sending code: " + str(code))
    sender = RFDevice(17)
    sender.enable_tx()
    sender.tx_code(code, 1, pulse)
    # sender.tx_code(code, protocol, pulse)
    sender.cleanup()