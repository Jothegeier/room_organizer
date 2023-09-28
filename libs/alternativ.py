import webuntis
import datetime
import json
import os
import sys
import re
#erforderlich: pip install webuntis

data = []
#user = input('User:')
#pw = input('Passwort:')

# Returns Path of libs-folder
def get_path():
    ending = sys.argv[0].split(sep=".")
    exec_path = ""
    if ending[len(ending)-1] == "exe":
        exec_path = os.path.join(os.path.dirname(sys.executable),"libs")
    elif ending[len(ending)-1] == "py":
        exec_path = os.path.dirname(__file__)
    return exec_path

def get_config_json(json_file):
    path = get_path()
    try:
        with open(os.path.join(path, json_file),'r') as file:
            jsondata = json.load(file)
    except FileNotFoundError:
        try:
            with open(os.path.join(os.path.dirname(path), json_file),'r') as file:
                jsondata = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Error: Could not find Json file!")
    return jsondata

def get_lesson(js):
    times = get_config_json("config.json")["lesson_times"]
    for i in times.keys():
        if js['startTime'] == times[i]:
            return str(i)

def main():
    json_data=get_config_json("config.json")
    s = webuntis.Session(
        server=json_data['url'],
        username=json_data['credentials']['user'],
        password = json_data['credentials']['pwd'],
        school=json_data['credentials']['school'],
        useragent=json_data['credentials']['useragent']
    )
    try:
        s.login()
        r = s.rooms()
        ru=r.__str__().replace("'",'"')
        room = json.loads(ru.__str__().replace("True",'true'))
        t = s.teachers()
        ta=t.__str__().replace("'",'"')
        teacher = json.loads(ta.__str__().replace("True",'true'))
        k = s.klassen()
        ks=k.__str__().replace("'",'"')
        students = json.loads(ks.__str__().replace("True",'true'))
        su=s.subjects()
        sub=su.__str__().replace("'",'"')
        subjects = json.loads(sub.__str__().replace("True",'true'))
        old_date = datetime.date.today()
        new_date = datetime.date.today()
        tt=[]
        for i in range(int(r.__len__())):
            tt.append(s.timetable(start=old_date, end=new_date,room=r[i]))
    except:
        print("Connection to API failed")
        return []
    listofdicts=[]
    result_dict = {
    'teachers': [],
    'students': [],
    'rooms': [],
    'subjects': [],
    'floor':[],
    'lesson':0
    }
    for i in range(tt.__len__()):
        for j in range(tt[i].__len__()):
            js=json.loads(tt[i][j].__str__().replace("'",'"'))
            for te in range(js['su'].__len__()):
                for ta in range(teacher.__len__()):
                    for tee in range(js['te'].__len__()):
                        if(teacher[ta]['id']==js['te'][tee]['id']):
                            result_dict['teachers'].append(teacher[ta]['name'])
                for ta in range(students.__len__()):
                    if(students[ta]['id']==js['kl'][0]['id']):
                        result_dict['students'].append(students[ta]['name'])
                for ta in range(room.__len__()):
                    for taa in range(js['ro'].__len__()):
                        if(room[ta]['id']==js['ro'][taa]['id']):
                            result_dict['rooms'].append(room[ta]['name'])
                for ta in range(subjects.__len__()):
                    if(subjects[ta]['id']==js['su'][0]['id']):
                        result_dict['subjects'].append(subjects[ta]['name'])


                # Get the time of the lessons
                result_dict['lesson'] = get_lesson(js)
                # for i in result_dict:
                #     if result_dict['lesson'] == None:
                #         result_dict['lesson'] == "0"


                listofdicts.append(result_dict)
                result_dict = {
                    'teachers': [],
                    'students': [],
                    'rooms': [],
                    'subjects': [],
                    'floor':[],
                    'lesson':0
                }
                #print("\n")
    print("Data received!")
    for i in range(listofdicts.__len__()):
        unit=listofdicts[i]    
        suchmuster = r"(\d+)"
        for j in range(unit['rooms'].__len__()):
            for k in range(json_data['rooms'].__len__()):
                if unit['rooms'][j]==json_data['rooms'][k]['name']:
                    listofdicts[i]['floor'].append(json_data['rooms'][k]['ebene'])
            if unit['floor'].__len__() ==0:
                ergebnis =re.search(suchmuster, unit['rooms'][j])
                if ergebnis:
                    erste_gefundene_zahl = ergebnis.group(1)
                    #print('Die erste gefundene Zahl ist:', erste_gefundene_zahl[0])
                    listofdicts[i]['floor'].append(erste_gefundene_zahl[0])
    s.logout() # see remark below
    #print(sorted(sorted(listofdicts, key=lambda x: x['floor']), key=lambda x: x['lesson']))
    return sorted(sorted(listofdicts, key=lambda x: x['floor']), key=lambda x: x['lesson'])

if __name__ == "__main__":
    main()