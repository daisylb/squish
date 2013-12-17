from flask import Flask
import lxml.html
from BeautifulSoup import UnicodeDammit
import requests
import re

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>squish</h1>"

@app.route("/<mode>/<path:url>")
def convert(mode, url):

    url_translator = URLTranslator(mode, url)

    # get the page and parse it with lxml
    html_str = requests.get(url).text
    html_str = UnicodeDammit(html_str).unicode
    html = lxml.html.document_fromstring(html_str, base_url=url)

    # clean up the page
    for el in html.iter():
        # support the HTML 'base' tag
        if el.tag == 'base' and el.get('href'):
            url_translator.register_base(el.get('href'))

        # remove comments
        if isinstance(el, lxml.html.HtmlComment):
            el.getparent().remove(el)
            continue

        # completely remove bad tags
        if el.tag in ('img', 'link', 'script', 'style', 'meta', 'iframe'):
            el.getparent().remove(el)
            continue

        # remove bad attributes
        for attr, value in el.attrib.iteritems():
            if attr.startswith('on') or attr in ('style', 'class', 'id'):
                del el.attrib[attr]

        # translate input[type=image] to submit
        if el.tag == 'input' and el.get('type') == 'image':
            el.attrib['type'] = 'submit'
            if el.get('src'):
                del el.attrib['src']
            if el.get('alt'):
                el.attrib['value'] = el.get('alt')
                del el.attrib['alt']

        # TODO: translate <noscript> to regular text

        # translate URL-containing attributes
        for attr in ('src', 'href'):
            if attr in el.attrib and el.attrib[attr]:
                el.attrib[attr] = url_translator(el.attrib[attr])

    return lxml.html.tostring(html, encoding='utf-8')

class URLTranslator (object):
    DOMAIN_RE = re.compile(r'(https?:)(\/\/[^\/]+\/)(.*\/|)([^\/]*)')
    def __init__(self, mode, base_url):
        self.mode = mode
        self.register_base(base_url)

    def register_base(self, base_url):
        self.base_url = base_url
        (self.protocol, self.domain, self.path, self.file
            ) = self.DOMAIN_RE.match(base_url).groups()

    def __call__(self, url_to_translate):
        # full http(s) path URL
        matchobj = self.DOMAIN_RE.match(url_to_translate)
        if matchobj:
            return "/{}/{}".format(self.mode, url_to_translate)

        # protocol-relative URL
        if url_to_translate.startswith('//'):
            return "/{}/{}{}".format(self.mode, self.protocol,
                url_to_translate)

        # domain-relative URL
        if url_to_translate.startswith('/'):
            return "/{}/{}{}".format(self.mode, self.protocol, self.domain,
                url_to_translate[1:])

        # everything else should be fine
        return url_to_translate

if __name__ == "__main__":
    app.run(debug=True)

