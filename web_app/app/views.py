from flask import render_template, jsonify

from app import app
import json

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard', methods=["GET"])
def dashboard():
    return render_template('dashboard.html')

@app.route('/_model_data',methods=["GET"])
def get_model_data():
    #get outputs from model

    #test outputs
    with open("data.json","w") as data:
        d = json.loads(data)
        outs = d[name]["model"]
        #outs = [0,0.1,0.1,0.1,0.05,0.05,0.3,0.15,0.15,0,0,0,0]
    return jsonify(out=outs)

@app.route('/_chat_data', methods=["GET"])
def get_chat_data():
    #get chat data from json
    with open("data.json","w") as data:
        d = json.loads(data)
        outs = d[name]["questions"]
    return jsonify(outs=outs)
    