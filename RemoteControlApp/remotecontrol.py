#!/usr/bin/env python3
# coding=utf-8

from flask import Flask, jsonify, request, render_template, abort
from outletdefinitions import outlets
from flask_rq2 import RQ



app = Flask(__name__)
rq = RQ(app)

@app.route("/Outlets/api/outlets", methods=["GET"])
def get_outlets():
    return jsonify({"outlets" : outlets})

@app.route("/Outlets/",methods=["GET"])
def index():
    return render_template("index.html")

import statestorage

@app.route("/Outlets/api/outlets/<int:buttonNumber>",methods=["GET"])
def get_outlet_state(buttonNumber):

    return statestorage.get_state(buttonNumber)

# 
# importing codesender library only here due to circular dependency error when importing at the beginning og the file
# https://stackoverflow.com/questions/43077599/flask-circular-dependency
#
import codesender

@app.route("/Outlets/api/outlets/<int:buttonNumber>",methods=["PUT","POST"])
def update_outlet_state(buttonNumber):
    state=None
    if request.json is not None:
        state=request.json.get("state")
    else:
        state=request.data.decode("utf-8")

    if (state is None):
        abort(400)
    if (state.lower() != 'on' and state.lower() != 'off'):
        abort(400)

    statestorage.set_state(buttonNumber, state)
    codesender.sendCode.queue(buttonNumber, state)
    return state

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=443)