from flask import Flask, jsonify, request, render_template
from outletdefinitions import outlets
import codesender

app = Flask(__name__)

@app.route("/Outlets/api/outlets", methods=["GET"])
def get_outlets():
    return jsonify({"outlets" : outlets})

@app.route("/Outlets/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/Outlets/api/outlets/<int:buttonNumber>",methods=["PUT"])
def clickButton(buttonNumber):
    state=request.json.get("state")
    print(buttonNumber)
    print(state)
    codesender.sendCode(buttonNumber,state)
    return state

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5000)
