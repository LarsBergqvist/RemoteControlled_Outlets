from typing_extensions import Protocol
from rpi_rf import RFDevice
from mylogger import logger
from outletdefinitions import outlets
from flask import current_app
from flask_rq2 import RQ

rq = RQ(app)

@rq.job
def sendCode(buttonNumber,state):
    validButton = next((sub for sub in outlets if sub['buttonNumber'] == buttonNumber), None)
    if(validButton == "None"):
        return

    if state == 'off':
        code = validButton['codeOff']
    elif state == 'on':
            code = validButton['codeOn']

    pulse = validButton['pulse']

    logger.info("Sending code: " + str(code))
    sender = RFDevice(17)
    sender.enable_tx()
    sender.tx_code(code, 1, pulse)
    # sender.tx_code(code, protocol, pulse)
    sender.cleanup()