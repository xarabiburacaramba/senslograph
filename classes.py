from altair import Chart
from pandas.io.json import json_normalize
import json
import requests

class VegaGraph():
    def __init__(self,type, data=None):
        self._type=type
        self._data=data
        self._chart=None
    
    def get_data(self):
        return self._data
        
    def set_data(self, data):
        self._data=data
        
    def get_type(self):
        return self._type
        
    def generate_visual(self):
        self._chart = Chart(self._data).mark_point().encode(
        x='time_stamp',
        y='value'
        ).interactive()
        
    def export_visual(self, kind):
        if kind=='json':
             return self._chart.to_json()
        else:
            return json.dumps({'error':('kind '+str(kind)+' is not implemented')})

class SensLogData():
    def __init__(self,endpoint, timestamp_from,timestamp_to, unit_id=None, sensor_id=None, data_url=None,  data=None):
        self._endpoint=endpoint
        self._timestamp_from=timestamp_from
        self._timestamp_to=timestamp_to
        self._data_url=data_url
        self._unit_id=unit_id
        self._sensor_id=sensor_id
        self._data=data
    
    def get_endpoint(self):
        return self._endpoint
        
    def get_timestampfrom(self):
        return self._timestamp_from
        
    def get_timestampto(self):
        return self._timestamp_to
        
    def get_unitid(self):
        return self._unit_id
        
    def get_sensorid(self):
        return self._sensor_id
        
    def get_data(self):
        return self._data
        
    def set_data(self, data):
        self._data=data
        
    def set_request_params(self):
        self._url_params={'from_time':str(self._timestamp_from),'to_time':str(self._timestamp_to),'unit_id':self._unit_id}
      
    def download_data(self):
        r=requests.get(self._endpoint, params=self._url_params)
        if r.status_code==200:
            a=json.loads(r.text)
            self._data=json_normalize(a, record_path='sensors', meta=['time_stamp','unit_id'])
        else:
            return json.dumps({'error':('error downloading data. status code:'+str(r.status_code))})
