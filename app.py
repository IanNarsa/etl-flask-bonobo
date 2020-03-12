from controller.bmkgcuaca import Mastercuaca
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

class Coba(Resource):
    def get(self):
        return {"data":"Berhasil"}


api.add_resource(Mastercuaca, '/master/cuaca/<wilayah>')
api.add_resource(Coba,'/')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8080')