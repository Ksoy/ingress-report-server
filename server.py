import os
from datetime import timedelta
from flask import Flask, render_template, jsonify, make_response, request, current_app, send_from_directory
from functools import update_wrapper

app = Flask(__name__)
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route("/")
@crossdomain(origin='*')
def root():
    data = [{
        'subject': 'BerdychThomas, ryzsean, loll11030, greeniswinner, BWChoi, BruceChuang and Winnychenn are multiple accounts cheater',
        'description': '''Dear NIA:
This agent "BerdychThomas", "ryzsean", "loll11030", "greeniswinner", "BWChoi" and "BruceChuang" are not only GPS snoofer but also multiple accounts cheater, please check their walking distance. As I know it should be easy to reach Bronze/Silver Trekker badge when you are L5/L8!! But these two cheaters still only have no/Bronze Trekker badge, and how they have such resource to attack! There must be lots cheating!
Please see the attached file, you can see him cheating!

We almost pretty sure these cheating accounts may come from a famous cheater "Winnychenn" in Hsinchu. Lots of Resistance and Enlightened agents always heard or saw the asshole cheating all the time!

STOP HIM NOW!
''',
        'flynames':  ['BerdychThomas', 'ryzsean'],
        'cheattype': 'abuse_cheat',
        'file_link': 'http://140.113.215.24:7777/files/test.zip'
    }]

    return jsonify(data)

@app.route('/files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(current_app.root_path, 'files')
    return send_from_directory(directory=uploads, filename=filename)

@app.route('/report_record', methods=['POST', 'OPTIONS'])
def record():
    print(dir(request))
    return 'ok'

app.run(host="0.0.0.0", port="7777", threaded=True)
