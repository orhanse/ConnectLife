from flask import Flask
from flask import render_template

from datetime import datetime
import os


app = Flask(__name__)


@app.route('/')
def home():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())


if __name__ == '__main__':
    PORT = int(os.getenv('VCAP_APP_PORT', '5000'))
    app.run(host='0.0.0.0', port=int(PORT))
