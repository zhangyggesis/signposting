from flask import Flask, request, render_template
import signposting
from signposting import cli
from io import StringIO
import sys

app = Flask(__name__)

#tmp = sys.stdout
#my_result = StringIO()

@app.route("/signposting/api")
def home():
    landingpage = request.args.get('url')
    s = signposting.find_signposting_http(
        landingpage)

    for d in s.describedBy:
        print(d.target)
        print(d.type)

    response = []
    for sp in s:
        response.append("%s<p>" % str(sp))
    #ss = cli.main(landingpage)
    #tt = cli.print_signposting(s)

    header = "<h1>Signposting: %s</h1>" % landingpage
    return header + str(response)

@app.route("/signposting")
def sitehome():
    return render_template("signposting.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)