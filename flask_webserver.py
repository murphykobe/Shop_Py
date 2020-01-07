#!/usr/bin/env python
# coding=utf-8

from flask import Flask, jsonify
from monitor import Monitor
app = Flask(__name__)
monitor = Monitor.getInstance()

@app.route("/")
def index():
    return jsonify({"Welcome": "This is a shopify bot."})

@app.route("/add")
def pop_proxy():
    if proxy[:5] == "https":
        return jsonify({"https": proxy})
    else:
        return jsonify({"http": proxy})

@app.route("/get/<int:count>")
def get_proxy(count):
    res = []
    for proxy in redis_conn.get_proxies(count):
        if proxy[:5] == "https":
            res.append({"https": proxy})
        else:
            res.append({"http": proxy})
    return jsonify(res)


@app.route("/count")
def count_all_proxies():
    count = redis_conn.count_all_proxies()
    return jsonify({"count": str(count)})


@app.route("/count/<int:score>")
def count_score_proxies(score):
    count = redis_conn.count_score_proxies(score)
    return jsonify({"count": str(count)})


@app.route("/clear/<int:score>")
def clear_proxies(score):
    if redis_conn.clear_proxies(score):
        return jsonify({"Clear": "Successful"})
    return jsonify({"Clear": "Score should >= 0 and <= 10"})
