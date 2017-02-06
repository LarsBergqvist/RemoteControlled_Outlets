#!/usr/bin/env python
# coding=utf-8

from flask import Flask, jsonify, request, render_template, abort
from outletdefinitions import outlets
import codesender, statestorage

app = Flask(__name__)

@app.route("/Outlets/api/outlets", methods=["GET"])
def get_outlets():
    return jsonify({"outlets" : outlets})

@app.route("/Outlets/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/Outlets/api/outlets/<int:groupNumber>/<int:buttonNumber>",methods=["GET"])
def get_outlet_state(groupNumber, buttonNumber):

    return statestorage.get_state(groupNumber, buttonNumber)

@app.route("/Outlets/api/outlets/<int:groupNumber>/<int:buttonNumber>",methods=["PUT","POST"])
def update_outlet_state(groupNumber, buttonNumber):
    state=None
    if request.json is not None:
        state=request.json.get("state")
    else:
        state=request.data

    if (state is None):
        abort(400)
    if (state.lower() != 'on' and state.lower() != 'off'):
        abort(400)

    statestorage.set_state(groupNumber, buttonNumber, state)
    codesender.sendCode(groupNumber, buttonNumber, state)
    return state

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5000)
