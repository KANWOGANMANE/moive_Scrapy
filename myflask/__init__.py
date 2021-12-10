from flask import Flask,render_template,redirect,url_for

app = Flask(__name__)

def serveron():
    app.run(debug=True,port='5000',host='127.0.0.1')
