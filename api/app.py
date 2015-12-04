from flask import Flask, request
from generate_index import main
app = Flask(__name__)

@app.route("/<website>/<depth>",methods=["POST"])
def index(website,depth):
    try:
        main(website,depth)
        return "success"
    except:
        return "failure"


app.run(debug=True)
