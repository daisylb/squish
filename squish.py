from flask import Flask
import lxml.html
from BeautifulSoup import UnicodeDammit
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>squish</h1>"

@app.route("/<mode>/<path:url>")
def convert(mode, url):

    # get the page and parse it with lxml
    html_str = requests.get(url).text
    html_str = UnicodeDammit(html_str).unicode
    html = lxml.html.document_fromstring(html_str, base_url=url)

    # clean up the page
    for el in html.iter():
        # completely remove bad tags
        if el.tag in ('img', 'link', 'script', 'style'):
            el.getparent().remove(el)
            continue

        # remove bad attributes
        for attr in ('style',):
            if attr in el.attrib:
                del el.attrib[attr]

    return lxml.html.tostring(html)

if __name__ == "__main__":
    app.run(debug=True)

