from flask import Flask, render_template, request, redirect, send_file, send_from_directory, url_for
import os
import sys
from datetime import datetime, timedelta

data = []
jsondata_global = {}

# initialize Flask app
app = Flask(__name__, static_folder= 'static', template_folder='templates')


def get_hour(time_subtract, hour_length):
    now = datetime.now() - timedelta(minutes=time_subtract + hour_length)
    stunden = now.hour
    minuten = now.minute
    
    # Stellen sicher, dass stunden und minuten immer zweistellig sind
    hhmm = f"{stunden:02d}{minuten:02d}"
    return hhmm

def get_lesson(jsondata):
    time_now = get_hour(jsondata["lesson_switch_difference"], jsondata["lesson_length"])
    
    times = jsondata["lesson_times"]
    for lesson in times.items():
        try:
            if int(time_now) <= lesson[1]:
                return lesson[0]
        except KeyError:
            pass
    
    return str(times.items()[0][1])


# Returns Path of libs-folder
def get_path():
    ending = sys.argv[0].split(sep=".")
    exec_path = ""
    if ending[len(ending)-1] == "exe":
        exec_path = os.path.join(os.path.dirname(sys.executable),"libs")
    elif ending[len(ending)-1] == "py":
        exec_path = os.path.dirname(__file__)
    
    return exec_path


# Standart forewarder
@app.route('/')
def index():
    return redirect(url_for('raumstundenplan'))


# Homepage
@app.route('/raumstundenplan')
def raumstundenplan():
    current_lesson = get_lesson(jsondata_global)
    return render_template('room_lesson_list.html', title='Raumplan', jsondata_time = jsondata_global["website_refresh_time"], current_lesson = current_lesson)


# Data for the History-DataTable
@app.route('/raumstundenplan/data')
def history_table():
    return {'data': data}


# Make sure that files can be opened
@app.route("/<path:path>", methods=["GET"])
def get_resource(path):  # pragma: no cover
    complete_path = get_path()
    file_path = ""
    if path.split(".")[-1] in ["css","js"]:
        if os.path.exists(os.path.join(complete_path, "static", path)):
            file_path = os.path.join(complete_path, "static", path)
    elif path.split(".")[-1] in ["html","ico", "png"]:
        if os.path.exists(os.path.join(complete_path, "templates", path)):
            file_path = os.path.join(complete_path, "templates", path)
    else:
        if os.path.exists(os.path.join(complete_path, os.path.dirname(get_path()),"ORDER_LOG", path)):
            file_path = os.path.join(complete_path, os.path.dirname(get_path()),"ORDER_LOG", path)
    if file_path != "":
        return send_file(file_path)
    else:
        return redirect(url_for('raumstundenplan'))


# the ME-Symbol
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates'),
        'ATIW.ico',mimetype='image/vnd.microsoft.icon')


# Start Function
def start_server(jsondata):
    print("\nShopping-Server at 'http://{}:{}/raumstundenplan'!\n\n".format(jsondata["server_url"],jsondata["server_port"]))
    global jsondata_global
    jsondata_global = jsondata
    app.run(host=jsondata["server_url"],debug=False, port=jsondata["server_port"],)
