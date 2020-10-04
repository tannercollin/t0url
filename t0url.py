# t0url - url.t0.vc
# MIT License

import random
import shelve
import string
import validators

from flask import abort, Flask, request, redirect
from werkzeug.exceptions import HTTPException

DB = 'data/t0url'
PORT = 5004
DOMAIN = 'url.t0.vc'
URL = 'https://' + DOMAIN
POST = 'url'

def help():
    form = (
        '<form action="{0}" method="POST" accept-charset="UTF-8">'
	'<input name="web" type="hidden" value="true">'
        '<input name="{1}">'
        '<br><button type="submit">Submit</button></form>'.format(URL, POST)
    )
    return """
<pre>
                        url.t0.vc
NAME
    t0url: command line short URL.

USAGE
    &lt;command&gt; | curl -F '{0}=&lt;-' {1}
    or upload from the web:

{2}

EXAMPLES
    ~$ cat yourfile | curl -F '{0}=&lt;-' {1}
       {1}/VFAR
    ~$ firefox {1}/VFAR

    Add this to your .bashrc:

    alias {0}="curl -F '{0}=<-' {1}"

    Now you can pipe a URL directly into {0}!

SOURCE CODE
    https://txt.t0.vc/RWFA
    https://github.com/tannercollin/t0url

SEE ALSO
    https://txt.t0.vc
    https://pic.t0.vc
</pre>""".format(POST, URL, form)

def new_id():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(4))

flask_app = Flask(__name__)

@flask_app.route('/', methods=['GET'])
def index():
    return '<html><body>{}</body></html>'.format(help())

@flask_app.route('/', methods=['POST'])
def new():
    try:
        with shelve.open(DB) as db:
            nid = new_id()
            while nid in db:
                nid = new_id()

            url = request.form['url'].strip()

            if not url: abort(400, 'Error: URL missing')
            if DOMAIN in url: abort(400, 'Error: use a different URL')
            if not url.startswith('http'):
                url = 'http://' + url
            if not validators.url(url): abort(400, 'Error: invalid URL')

            db[nid] = url

            print('Adding url {}:\n{}'.format(nid, url))

        return '{}/{}'.format(URL, nid) + '\n'
    except HTTPException:
        raise
    except:
        abort(400, 'Error: unknown problem')

@flask_app.route('/<nid>', methods=['GET'])
def get(nid):
    try:
        with shelve.open(DB) as db:
            return redirect(db[nid])
    except:
        abort(404)

flask_app.run(port=PORT)
