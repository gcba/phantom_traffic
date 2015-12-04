from flask import Flask, render_template, url_for
import os
from confs import configs
from confs import server_conf

app = Flask(__name__)
cities = []
@app.route('/index')
@app.route('/')
def index():
    #INDEX PAGE
    return 'Hello I\'m a index :D'

@app.route('/reports')
def reports():
    return 'Here, in the future, you can see the reports!!'

def countImgRendered(DIR = configs.imgFolder, format = 'png'):
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
def status(username = None, city = None ):
    printme = '<html>' \
              '<head></head>' \
              '</body>'
    databulk = []
    if not username == None:
        pass
    else:
        pass
    if not city == None:
        cID = existCity(city)
        if cID > -1:
            ifol = configs.imgFolder+cities[cID]['dest_folder']
            if os.path.exists(ifol):
                imgCount = countImgRendered(ifol, cities[cID]['format'])

    else:
        #yes... the hard way! (fuck!)
        printme ='<table style=\"border:0px; border-spacing:1px;\"><tr style=\"background-color:#333333; color:#FFF;\">'\
                '<td><strong> Pluguin Name </strong></td>'\
                '<td><strong> Pluguin Status </strong></td>'\
                '<td><strong> Inicio Obs. </strong></td>'\
                '<td><strong> Img Folder </strong></td>'\
                '<td><strong> Obs. por hora </strong></td>'\
                '<td><strong> Get it all! </strong></td>'\
                '</tr>'
        print 'Cities: %d' % len(cities)

        for i in range(0,len(cities)):
            view_data = {}
            ifol = configs.imgFolder+cities[i]['dest_folder']
            printme += '<tr style=\"background-color:#FFFFCC; color:#333; font-family:sans; font-size:10\">' \
                       '<td>{n}</td>' \
                       '<td>{st}</td>' \
                       '<td>{since}</td>' \
                       '<td>{la}</td>' \
                       '<td>{oph}</td>' \
                       '<td><a href scr={download}> >> </a></td>'\
                       '</tr>'.format(n=cities[i]['name'],
                                      st='Running',
                                      since=cities[i]['start_at'],
                                      la=cities[i]['dest_folder'],
                                      oph=cities[i]['times_per_hour'],
                                      download='http://{host}:{port}/{uri}'.format(host=server_conf.server_ip,
                                                                                   port=server_conf.server_port,
                                                                                   uri=cities[i]['dest_folder'],
                                                                                   )
                                      )
        printme +='</table>'

    printme += '</body>' \
               '</html>'
    #view_data  = {
        #     'img_count': countImgRendered(ifol, cities[i]['format']),
        #     'name' : cities[i]['name'],
        #     'status': 'running', #HARDCODEO!
        #     'located_at': cities[i]['dest_folder'],
        #     'Obs_per_hour': cities[i]['times_per_hour'],
        #     }
        # databulk.append(view_data)
        #return render_template('status.html', data=databulk)
    return printme

def printRoutes():
    with app.test_request_context():
        print url_for('index')
        print url_for('reports')
        print url_for('status', next='/')



def launchServer():
    app.run()