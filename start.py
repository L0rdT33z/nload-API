#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import re
import flask
import json
from flask import request

app = flask.Flask(__name__)
app.config['DEBUG'] = True


def getResult():
    out = ''
    proc = subprocess.Popen(['nload'], stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    try:
        (outs, errs) = proc.communicate(timeout=2)
    except:
        proc.kill()
        (outs, errs) = proc.communicate()
        out = outs.decode('utf-8')
    return out


def match(test_str, regex):
    matches = re.findall(regex, test_str, re.MULTILINE)[0]
    return matches


@app.route('/', methods=['GET'])
def home():
    res = getResult()
    result = {}
    incoming_curr = match(res, r"Incoming.+Curr:\s([^\u001B]+)").strip()
    incoming_avg = match(res, r"Incoming.+Avg:\s([^\u001B]+)").strip()
    incoming_min = match(res, r"Incoming.+Min:\s([^\u001B]+)").strip()
    incoming_max = match(res, r"Incoming.+Max:\s([^\u001B]+)").strip()
    incoming_ttl = match(res, r"Incoming.+Ttl:\s([^\u001B]+)").strip()
    outgoing_curr = match(res, r"Outgoing.+Curr:\s([^\u001B]+)").strip()
    outgoing_avg = match(res, r"Outgoing.+Avg:\s([^\u001B]+)").strip()
    outgoing_min = match(res, r"Outgoing.+Min:\s([^\u001B]+)").strip()
    outgoing_max = match(res, r"Outgoing.+Max:\s([^\u001B]+)").strip()
    outgoing_ttl = match(res, r"Outgoing.+Ttl:\s([^\u001B]+)").strip()
    result['incoming'] = {}
    result['incoming']['curr'] = incoming_curr
    result['incoming']['avg'] = incoming_avg
    result['incoming']['min'] = incoming_min
    result['incoming']['max'] = incoming_max
    result['incoming']['ttl'] = incoming_ttl
    result['outgoing'] = {}
    result['outgoing']['curr'] = outgoing_curr
    result['outgoing']['avg'] = outgoing_avg
    result['outgoing']['min'] = outgoing_min
    result['outgoing']['max'] = outgoing_max
    result['outgoing']['ttl'] = outgoing_ttl
    return json.dumps(result, indent=4)

app.run()
