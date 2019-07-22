import json

from flask import Flask,  request

from classes import VegaGraph, SensLogData

app = Flask(__name__)

@app.route('/get_number', methods=['GET'])
def get_number():
    return json.dumps({'number':'5'})

@app.route('/get_graph', methods=['GET'])
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

if __name__ == "__main__":
    app.run(debug=True,  host='0.0.0.0', port=5000)
