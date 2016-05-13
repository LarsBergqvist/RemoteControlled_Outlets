from flask import Flask
from flask import render_template, redirect, url_for
import pi_switch

buttonToIDCodesMap = { 
1: 0x15,
2: 0x45,
3: 0x51,
4: 0x54
}

byte0codeON = 0x55
byte0codeOFF = 0x54

byte2 = 0x15

app = Flask(__name__)

@app.route("/button/<int:buttonNumber>/<string:state>",methods=['GET'])
def clickButton(buttonNumber,state):
    print(buttonNumber)
    print(state)
    idcode = buttonToIDCodesMap[buttonNumber]
    byte0code = byte0codeON
    if state == 'off':
        byte0code = byte0codeOFF
    code = (byte2 << 16) | (idcode << 8) | byte0code
    print(format(code,'000000x'))
    sender = pi_switch.RCSwitchSender()
    sender.enableTransmit(0)
    sender.sendDecimal(code,24)
    return redirect(url_for('start'))

@app.route("/")
def start():
    return render_template('rcremote.html')

if __name__ == "__main__":
#    app.debug = True
    app.run(host='0.0.0.0',port=5000)
