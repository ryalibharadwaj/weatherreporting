import json
from urllib2 import urlopen, HTTPError

class WeatherInfo_Extractor(object):
    def __init__(self,name):
        self.name = name 

    def dump(self):
        try:
            self.data = urlopen(self.name)
            return self.data
        except HTTPError as err:
            if err.code == 404:
                return '{"cod":"404","message":"city not found"}'
            elif err.code == 401:
                return '{"cod":"401","message":"Invalid API key. Please see http://openweathermap.org/faq#error401 for more info."}'
            else:
                return '{"cod":"999","message":"Exception not verified."}'
        
    def getWeatherInfo(self):
        try:
            data =  json.load(self.dump())
        except:
            data =  json.loads(self.dump())
        return data
