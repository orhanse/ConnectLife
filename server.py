import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())



@app.route('/kisiler')
def kisiler_sayfasi():
    now = datetime.datetime.now()
    return render_template('kisiler.html', current_time=now.ctime())

@app.route('/universiteler')
def universiteler_sayfasi():
    now = datetime.datetime.now()
    return render_template('universiteler.html', current_time=now.ctime())

@app.route('/gruplar')
def gruplar_sayfasi():
    now = datetime.datetime.now()
    return render_template('gruplar.html', current_time=now.ctime())

@app.route('/sirketler')
def sirketler_sayfasi():
    now = datetime.datetime.now()
    return render_template('sirketler.html', current_time=now.ctime())

@app.route('/isilanlari')
def isilanlari_sayfasi():
    now = datetime.datetime.now()
    return render_template('isilanlari.html', current_time=now.ctime())




if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
