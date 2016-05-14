import pi_switch

byte0codeON = 0x55
byte0codeOFF = 0x54
byte2 = 0x15 #This is group 1

buttonToIDCodesMap = { 
1: 0x15,
2: 0x45,
3: 0x51,
4: 0x54
}

def sendCode(buttonNumber,state):
    idcode = buttonToIDCodesMap[buttonNumber]
    byte0code = byte0codeON
    if state == 'off':
        byte0code = byte0codeOFF
    code = (byte2 << 16) | (idcode << 8) | byte0code
    print(format(code,'000000x'))
    sender = pi_switch.RCSwitchSender()
    sender.enableTransmit(0)
    sender.sendDecimal(code,24)
