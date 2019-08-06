import json
import datetime
import pandas as pd

import altair as alt

from flask import Flask,  request,  render_template

from classes import VegaGraph, SensLogData

def sum(arr):
    if len(arr)==1:
        return arr[0]
    else:
        sum=arr[0]
        for i in range(1,len(arr)):
            sum=sum+arr[i]
        return sum

def sum_v(arr):
    if len(arr)==1:
        return arr[0]
    else:
        sum=arr[0]
        for i in range(1,len(arr)):
            sum=alt.vconcat(sum, arr[i])
        return sum
        
        
application = Flask(__name__)

endpoint_dict={'foodie':'http://foodie.lesprojekt.cz:8080/senslogOT/rest/observation'}

@application.route('/get_number', methods=['GET'])
def get_number():
    return json.dumps({'number':'5'})

@application.route('/get_graph', methods=['GET'])
def get_params_of_get_graph():
    timestamp_from=str(request.args.get('time_from'))
    timestamp_to=str(request.args.get('time_to'))
    endpoint=str(request.args.get('senslog_endpoint'))
    endpoint_url=endpoint_dict[endpoint]
    graph_type=str(request.args.get('graph_type'))
    unit_id=json.loads(str(request.args.get('unit_id')))
    if 'sensor_id' in list(request.args.keys()):
        sensor_id=int(request.args.get('sensor_id'))
    format=str(request.args.get('format'))
    return do_send_graph(endpoint_url, unit_id, timestamp_from, timestamp_to, graph_type, format,  sensor_id)

def do_send_graph(endpoint_url, unit_id, timestamp_from, timestamp_to, graph_type, format,  sensor_id=None):
    #s=SensLogData(endpoint=endpoint_url,timestamp_from=timestamp_from,timestamp_to=timestamp_to, unit_id=unit_id)
    #s.set_request_params()
    #s.download_data()
    frames=[]
    for i in unit_id['id']:
        s=SensLogData(endpoint=endpoint_url,timestamp_from=timestamp_from,timestamp_to=timestamp_to, unit_id=i, sensor_id=sensor_id)
        s.set_request_params()
        s.download_data()
        if len(s.get_data().index)>0:
            frames.append(s.get_data())
    df=pd.concat(frames)
    print(df.head())
    if sensor_id!=None:
        vg=VegaGraph(title=("Sensor "+str(sensor_id)), type=graph_type,data=df)
        vg.generate_visual()
        return vg.export_visual(format)
    else:
        charts=[]
        for j in pd.unique(df['sensor_id']):
            vg=VegaGraph(title=("Sensor "+str(j)), type=graph_type,data=df[df['sensor_id']==j])
            vg.generate_visual()
            charts.append(vg.get_chart())
        return sum_v(charts).to_json()

    
@application.route("/")
def index():
    return render_template("sensors.html", vegajsobject=(do_send_graph(endpoint_url='http://foodie.lesprojekt.cz:8080/senslogOT/rest/observation', unit_id={"id":[1305167549144045,1305167549158198,1305167549167050,1305167549173046,1305167549167886,1305167549149707]}, timestamp_from=(datetime.datetime.now()-datetime.timedelta(hours=72)).strftime('%Y-%m-%d %H:%M:%S'), timestamp_to=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), graph_type='line', format='json')));

if __name__ == "__main__":
    application.run()
''''http://senslograph-senslograph.apps.us-east-1.online-starter.openshift.com/
get_graph?time_from=2019-06-30 12:00:00&time_to=2019-07-01 12:00:00&senslog_endpoint=foodie&unit_id=1305167549167050&format=json

get_graph?
time_from=...&
time_to=...&
senslog_endpoint=...&
unit_id=...&
measure=...||sensor_id=...&
format=…
: mereni jedne veliciny pouze z jedne jednotky
: mereni jedne veliciny napric jednotek
akurat brat ohled na typ promenne: jestli je int anebo int[]

unit_id IN(
1305167549144045,
1305167549158198,
1305167549167050,
1305167549173046,
1305167549167886,
1305167549149707)

sensor_id IN (
340360001,
340350001,
360200000,
540090005,
550900004,
540090004,
550020004,
340370004,
560030000)

firstObservationTime:"2019-01-10 19:35:00+01"

for i in json.loads(unit_id)['id']:
...     s=SensLogData(endpoint=endpoint_dict[endpoint],timestamp_from=time_from,timestamp_to=time_to, unit_id=i)
...     s.set_request_params()
...     s.download_data()
...     for j in json.loads(sensor_id)['id']:                                                                                                                                  
...             s.get_data()[s.get_data()['sensor_id'].isin([j])]


'''
