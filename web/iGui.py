from flask import Flask, render_template
import os
from confs import configs
from confs import server_conf

app = Flask(
    __name__,
    template_folder='../web/templates',
    static_folder='../web/static'
)
cities = []


def start_server():
    app.run(host=server_conf.server_ip, port=int(server_conf.server_port))


@app.route('/index')
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/reports')
def reports():
    return 'Here, in the future, you can see the reports!!'


def countImgRendered(DIR=configs.imgFolder, format='png'):
    rFounded = 0
    for filename in os.listdir(DIR):
        if filename.endswith('.%s' % format):
            rFounded += 1
    return rFounded


def existCity(city):
    for i in range(0, len(cities)):
        if cities[i]['name'] == city:
            return i
    return -1


@app.route('/status')
@app.route('/status/<username>')
@app.route('/status/<city>')
def status(username=None, city=None):
    return 'TODO'


@app.route('/login', methods=['POST'])
def login():
    # TODO: https://github.com/maxcountryman/flask-login
    return