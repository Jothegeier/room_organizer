from libs.alternativ import main, get_config_json
import libs.webserver as serv
import threading as th
import time
import datetime

def searches ():
    while True:
        serv.data = main()
        time.sleep(get_config_json("config.json")["request_time"])

def get_hour():
    now = datetime.datetime.now()
    stunden = now.hour
    minuten = now.minute
    
    # Stellen sicher, dass stunden und minuten immer zweistellig sind
    hhmm = f"{stunden:02d}{minuten:02d}"
    
    return hhmm

def program():
    request = th.Thread(target=searches, daemon=True)
    request.start()
    config_data = get_config_json("config.json")
    serv.start_server(config_data)

if __name__ == "__main__":
    program()