from flask import Flask, request, render_template
import signposting
from signposting import cli
from io import StringIO
import urllib.request,urllib.parse,urllib.error


app = Flask(__name__)

@app.route("/signposting/check")
def home():
    landingpage = request.args.get('url')
    response = {}

    try:
        s = signposting.find_signposting_http(
            landingpage)
    except (ValueError, urllib.error.HTTPError) as ve:
        response["Error"] = str(ve)
        return response

    else:
        #print it out
        print(str(s))

        response = {}
        c = 1
        response[c] = "Signposting Landing Page: <" + landingpage + ">"

        for sp in s:
            l = sp.rel + ": <" + sp.target + ">"
            c = c+1
            response[c] = l;

        return  response

@app.route("/")
def sitehome():
    return render_template("signposting.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)