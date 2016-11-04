#!/usr/bin/env python
# coding=utf-8

from flask import Flask, jsonify, request, render_template, abort
from outletdefinitions import outlets
import codesender

app = Flask(__name__)

@app.route("/Outlets/api/outlets", methods=["GET"])
def get_outlets():
    return jsonify({"outlets" : outlets})

@app.route("/Outlets/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/Outlets/api/outlets/<int:groupNumber>/<int:buttonNumber>",methods=["PUT"])
def clickButton(groupNumber, buttonNumber):
    state=request.json.get("state")
    if (state is None):
        abort(400)
    if (state.lower() != 'on' and state.lower() != 'off'):
        abort(400)
        
    codesender.sendCode(groupNumber,buttonNumber,state)
    return state

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5000)
