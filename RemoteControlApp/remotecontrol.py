from flask import Flask, jsonify, request
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

@app.route("/Outlets/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/Outlets/api/outlet/<int:buttonNumber>",methods=['PUT'])
def clickButton(buttonNumber):
    state=request.json.get("state")
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
    return state

#@app.route("/")
#def start():
#    return render_template('rcremote.html')

if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0',port=5000)
