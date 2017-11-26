from flask import render_template, jsonify, request

from app import app
import json
import os

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard', methods=["GET"])
def dashboard():
    name = request.args.get("name")
    print(name)
    with open("data.json","r") as data:
        d = json.load(data)
        chats = d[name]["questions"]
    return render_template('dashboard.html', chats = chats)


@app.route('/_model_data',methods=["GET"])
def get_model_data():
    #get outputs from model

    #test outputs
    name = request.args.get("name")
    with open(os.path.join("web_app","data.json"),"r") as data:
        d = json.load(data)
        for id in d:
            if d[id]["name"].lower() == name.lower():
                outs = d[id]["model"]

        #outs = [0,0.1,0.1,0.1,0.05,0.05,0.3,0.15,0.15,0,0,0,0]
    return jsonify(out=outs)

@app.route('/_chat_data', methods=["GET"])
def get_chat_data():
    #get chat data from json
    name = request.args.get("name")
    outs = {}
    with open(os.path.join("web_app","data.json"),"r") as data:
        d = json.load(data)
        for id in d:
            if d[id]["name"].lower() == name.lower():
                outs = d[id]["pains"]
    print(outs)
    return jsonify(out=outs)
    