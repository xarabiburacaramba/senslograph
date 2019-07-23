import json
import datetime

from flask import Flask,  request,  render_template

from classes import VegaGraph, SensLogData

application = Flask(__name__)

@application.route('/get_number', methods=['GET'])
def get_number():
    return json.dumps({'number':'5'})

@application.route('/get_graph', methods=['GET'])
def get_params_of_get_graph():
    timestamp_from=str(request.args.get('time_from'))
    timestamp_to=str(request.args.get('time_to'))
    endpoint=str(request.args.get('senslog_endpoint'))
    if endpoint=='foodie':
        endpoint_url='http://foodie.lesprojekt.cz:8080/senslogOT/rest/observation'
    graph_type=str(request.args.get('graph_type'))
    unit_id=int(request.args.get('unit_id'))
    format=str(request.args.get('format'))
    return do_send_graph(endpoint_url, unit_id, timestamp_from, timestamp_to, graph_type, format)

def do_send_graph(endpoint_url, unit_id, timestamp_from, timestamp_to, graph_type, format):
    s=SensLogData(endpoint=endpoint_url,timestamp_from=timestamp_from,timestamp_to=timestamp_to, unit_id=unit_id)
    s.set_request_params()
    s.download_data()
    vg=VegaGraph(type=graph_type,data=s.get_data())
    vg.generate_visual()
    return vg.export_visual(format)
    
@application.route("/")
def index():
    return render_template("sensors.html", vegajsobject=(do_send_graph(endpoint_url='http://foodie.lesprojekt.cz:8080/senslogOT/rest/observation', unit_id=1305167549167050, timestamp_from=(datetime.datetime.now()-datetime.timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S'), timestamp_to=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), graph_type='point', format='json')));

if __name__ == "__main__":
    application.run()
