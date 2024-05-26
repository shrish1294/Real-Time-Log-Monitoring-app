import traceback
from flask import Flask, render_template
from flask_sse import sse
import sched
from test_func import return_last_10_lines
from apscheduler.schedulers.background import BackgroundScheduler
import logging 
logger = logging.Logger("gunicorn.error")
import json
import os
from test_func import return_last_10_lines

app = Flask(__name__)


app.register_blueprint(sse, url_prefix='/stream')
app.config["REDIS_URL"] = "redis://localhost"



def latest_changes(path = 'log_file.txt'):
    """yields any latest change in the file"""
    with open(path , 'rb') as f:
        f.seek(0, 2)
        while True:
            val  = f.readline()
            if val:
                yield val
            else:
                yield None

updates = latest_changes()
last_10_lines = return_last_10_lines('log_file.txt')
msgs  = last_10_lines



@app.route('/')
def test_endpoint():
    """endpoint to test if app is working"""
    return 'app is working'

@app.route('/log')
def get_changes():
    """returns the new changes present in the logfile"""
    val = next(updates)
    print(val)
    if val:
        return val
    else:
        return "no new changes"


@app.route('/monitor')
def index():
    """returns landing page showing log changes"""
    return render_template("index.html")



@app.route('/hello')
def publish_hello():
    """test function to check publish functionality"""
    sse.publish({"message": "Hello!"}, type='message')
    return "Message sent!"


def update_logs():
    """check if log is updated or not"""
    with app.app_context():
        logger.info("update called")
        print("update")
        val = next(updates)
        print(val)
        if val:
            val = str(val, "utf-8")
            msgs.append(val)
            msgs.append("<br>")
            print(msgs)
        sse.publish(json.dumps({"message": msgs}), type='message')



sched = BackgroundScheduler()



job = sched.add_job(update_logs, 'interval', seconds=2)
sched.start()


if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)