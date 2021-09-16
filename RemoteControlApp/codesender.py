from typing import Protocol
from rpi_rf import RFDevice
from mylogger import logger

byte0codeON = 0x55
byte0codeOFF = 0x54

groupToCodeMap = {
1: 0x15,
2: 0x45,
3: 0x51,
4: 0x54
}

buttonToCodeMap = { 
1: 0x15,
2: 0x45,
3: 0x51,
4: 0x54
}

def sendCode(groupNumber,buttonNumber,state):
    if not buttonNumber in buttonToCodeMap.keys():
        return
    if not groupNumber in groupToCodeMap.keys():
        return

    numberCode = buttonToCodeMap[buttonNumber]
    groupCode = groupToCodeMap[groupNumber]

    byte0code = byte0codeON
    if state == 'off':
        byte0code = byte0codeOFF
    code = (groupCode << 16) | (numberCode << 8) | byte0code
    logger.info("Sending code: " + format(code,'000000x'))
    sender = RFDevice(17)
    sender.enable_tx()
    sender.tx_code(code)
    # sender.tx_code(code, protocol, pulse)
    sender.cleanup()
