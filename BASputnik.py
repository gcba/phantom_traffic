import subprocess
import time
import json
import os
import threading
from confs import configs
from libs import iGui

def launchServer():
    iGui.app.run()

def load_plugins():
    cities = []
    plugin_folder = os.path.join('.', configs.plugins_confs["folder"])
    for filename in os.listdir(plugin_folder):
        if filename.endswith(".%s" % configs.plugins_confs["ext"]):
            file_path = os.path.join(plugin_folder, filename)
            with open(file_path) as plugin:
                city_dict = json.load(plugin)
                city = {
                    'name': city_dict['name'],
                    'lat':  city_dict['coordinates']['latitude'],
                    'lon':  city_dict['coordinates']['longitude'],
                    'width': city_dict['canvas']['width'],
                    'height': city_dict['canvas']['height'],
                    'zoom': city_dict['zoom'],
                    'times_per_hour': city_dict['obs_time']['obs_per_hour'],
                    'start_at': city_dict['obs_time']['start'],
                    'ends_at': city_dict['obs_time']['end'],
                    'dest_folder': os.path.join('img', city_dict['render']['str_folder']),
                    'format': city_dict['render']['out_format'],
                    'quality': city_dict['render']['quality'],
                }
            configs.log.add('INFO: \"%s\" plugin loaded...' % city_dict['name'])
            folder = os.path.join('.', city['dest_folder'])
            if not os.path.exists(folder):
                os.makedirs(folder)
            cities.append(city)
    configs.log.add('INFO: %d cities loaded!' % len(cities))
    return cities


def take_picts(cities):
    for city in cities:
        try:
            configs.log.add('INFO: Taking picts of %s' % city['name'])
            subprocess.Popen([
                'phantomjs',
                '--ignore-ssl-errors=true',
                'get_maps.js',
                city['dest_folder'],
                str(city['width']),
                str(city['height']),
                str(city['zoom']),
                city['format'],
                str(city['quality']),
                str(city['lat']),
                str(city['lon']),
                city['name']
            ])
        except Exception as e:
            configs.log.add('ERROR: %s \n\tSomething is not going well... ' % str(e))


def main():
    try:
        configs.log.add('INFO: Starting web-gui...')
        t = threading.Thread(target=launchServer)
        t.start()
        configs.log.add('INFO: love is in the air! and web-gui too!!!')
    except Exception as e:
        configs.log.add('ERROR: something going bad... can\'t start web-gui...[%s]' % e)
    while True:
        start_time = time.time()
        cities = load_plugins()
        iGui.cities = cities
        #take_picts(cities)
        elapsed_time = time.time() - start_time
        if elapsed_time < configs.hrdCodedTime:
            sleep_time = int(configs.hrdCodedTime-elapsed_time)
            configs.log.add('INFO: Ok, now I take little snooze for %d seconds.. ZZZzzZZ.' % sleep_time)
            time.sleep(sleep_time)
        else:
            configs.log.add('WARNING: Cycle took too long, no time to sleep... :(')

if __name__ == '__main__':
    main()
