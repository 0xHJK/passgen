#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_from_directory,abort, redirect
from passgen import PassGen

app = Flask(__name__)

@app.route('/zip/<filename>')
def download(filename):
    if request.method == 'GET':
        return send_from_directory('zip', filename, as_attachment = True)
        abort(404)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {key: dict(request.form)[key][0] for key in dict(request.form)}
        pg = PassGen(data)
        return redirect(pg.filelink)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    # app.debug=True
    app.run(host='0.0.0.0')
