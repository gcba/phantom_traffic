from flask import Flask, render_template
import os
from confs import configs

app = Flask(
    __name__,
    template_folder='../web/templates',
    static_folder='../web/static'
)
cities = []


@app.route('/index')
@app.route('/')
def index():
    return render_template('base.html')


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
