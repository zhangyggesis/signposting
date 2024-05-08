from flask import Flask, request, render_template
import signposting
import urllib.request, urllib.parse, urllib.error
from urllib.error import HTTPError, URLError
from signposting.htmllinks import UnrecognizedContentType, find_signposting_html
from signposting.linkset import LinksetParseError, find_signposting_linkset

app = Flask(__name__)


@app.route("/signposting/check")
def home():
    landingpage = request.args.get('url')
    response = {}
    print(str(landingpage))
    s_html = None
    s_http = None
    # ignore all warnings.
    # warnings.simplefilter('ignore')

    try:
        s_http = signposting.find_signposting_http(landingpage)
        print("s http " + str(s_http))
        # linkset is not supported at this moment.
        # s_linkset = find_signposting_linkset(landingpage)
        # print("s linkset " + str(s_linkset))
        print("Signpopsting: HTTP links " + str(s_http))

    except (ValueError, urllib.error.HTTPError, URLError, IOError) as ve:
        response["Error"] = str(ve)
        return response

    except UnrecognizedContentType as uc:
        pass

    try:
        s_html = signposting.find_signposting_html(landingpage)
        print("s html " + str(s_html))
        # linkset is not supported at this moment.
        # s_linkset = find_signposting_linkset(landingpage)
        # print("s linkset " + str(s_linkset))
        print("Signpopsting: HTML links " + str(s_html))

    except (ValueError, urllib.error.HTTPError, URLError, IOError) as ve:
        response["Error"] = str(ve)
        return response

    except UnrecognizedContentType as uc:
        pass

    hm = "htmlLinks"
    hp = "httpLinks"
    url = "PID"
    # The assessment result.

    assessment = {}
    signposting_html = {}
    signposting_http = {}
    response["assessment"] = assessment
    assessment[hm] = signposting_html
    assessment[url] = landingpage
    assessment[hp] = signposting_http

    # populate signposting html and http, starting from html
    s = s_html
    if s:
        c = 0
        for sp in s:
            l = sp.rel + ": <" + sp.target + ">"
            c = c + 1
            signposting_html[c] = l;
    s = s_http
    if s:
        c = 0
        for sp in s:
            l = sp.rel + ": <" + sp.target + ">"
            c = c + 1
            signposting_http[c] = l;

    return response


@app.route("/")
def sitehome():
    return render_template("signposting.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
