import pi_switch
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
    sender = pi_switch.RCSwitchSender()
    sender.enableTransmit(0)
    sender.sendDecimal(code,24)
