from flask import Flask,request,render_template
from multiprocessing import Process
import requests
def shutdown_server():
    func = request.environ.get("werkzeug.server.shutdown")
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()

app = Flask(__name__)

@app.route("/",methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/test_one",methods=["GET"])
def test_one():
    return "Hello World!"

@app.route("/test_two",methods=["GET"])
def test_two():
    return render_template("test_two.html")

@app.route("/shutdown",methods=["POST"])
def shutdown():
    shutdown_server()
    return "Server shutting down..."

app.run()
