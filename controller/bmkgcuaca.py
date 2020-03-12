import xmltodict
import requests as req
import json
from flask_restful import Resource
from flask import jsonify
import bonobo
from kamus import kamus_cuaca
final = {"data":"tidak dapat menemukan hasil"}
class Mastercuaca(Resource):
    def get(self,wilayah):
        def scrape_bmkg(wilayah):
            try:
                print("scrape ",wilayah)
                #wilayah = 'DIYogyakarta'
                url = 'http://data.bmkg.go.id/datamkg/MEWS/DigitalForecast/DigitalForecast-'+wilayah+'.xml'
                body = req.get(url)
                parse_data = xmltodict.parse(body.text,attr_prefix='')
                hasil = json.dumps(parse_data)
                final = json.loads(hasil)
                dt = final['data']['forecast']
                return dt, wilayah
            except :
                return None
            
            
        def extract(x):
            try:
                print("extract ",x)
                yield scrape_bmkg(x)[0]
            except :
                print("Data Tidak Ditemukan")
            

        def transform(dt):
            try:
                dCuaca = kamus_cuaca()
                _data = []
                for i in dt['area']:
                    x =  i['domain']
                    weather = []
                    area = {
                        'source': 'BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)',
                        'id': i['id'],
                        'latitude': i['latitude'],
                        'longitude': i['longitude'],
                        'coordinate': i['coordinate'],
                        'kabupaten': i['description'],
                        'propinsi': i['domain'],
                        'waktu': dt['issue']
                    }
                    for x in i['parameter']:
                        if x['id'] == 'weather':
                            for y in x['timerange']:
                                kd = y['value']['#text']
                                ketCuaca = dCuaca[int(kd)]
                                y['value']['#text'] = ketCuaca
                                weather.append(y)
                    temp = {
                        'weather':weather
                    }
                    area.update(temp)
                    _data.append(area)
                yield _data
            except :
                None
            

        def load(xyz):
            global final
            try:
                nama = xyz[0]['propinsi']
                nama = nama.replace(' ','')
                with open(nama+'.json', 'w') as fp:
                    json.dump(xyz, fp)
                y = xyz
                _hasil = {"data":y}
                print(type(_hasil))
                final = _hasil
            except :
                print("Tidak Dapat Menampilkan Hasil")
        
        x = wilayah
        graph = bonobo.Graph(
            extract(x),
            transform,
            load
        )
        bonobo.run(graph)
        return  final