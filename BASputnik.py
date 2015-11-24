import subprocess
import time
import json
import os
from confs import configs


def load_plugins():
    cities = []
    pfolder = "./%s" % configs.plugins_confs["folder"]
    for file in os.listdir(pfolder):
        if file.endswith(".%s" % configs.plugins_confs["ext"]):
            with open('%s/%s' % (pfolder, file)) as plugin:
                d = json.load(plugin)

                c = {
                    'name': d['name'],
                    'lat':  d['coordinates']['latitude'],
                    'lon':  d['coordinates']['longitude'],
                    'width': d['canvas']['width'],
                    'height': d['canvas']['height'],
                    'zoom': d['zoom'],
                    'times_per_hour': d['obs_time']['obs_per_hour'],
                    'start_at': d['obs_time']['start'],
                    'ends_at': d['obs_time']['end'],
                    'dest_folder': d['render']['str_folder'],
                    'format': d['render']['out_format'],
                    'quality': d['render']['quality'],
                }
            configs.log.add('INFO: \"%s\" plugin loaded...' % d['name'])
            folder = './%s' % c['dest_folder']
            if not os.path.exists(folder):
                os.mkdir(folder)
            cities.append(c)
    configs.log.add('INFO: %d Cities loaded!' % len(cities))
    return cities


def take_picts(cities):
    for i in range(0, len(cities)):
        try:
            configs.log.add('INFO: Taking picts from: %s' % cities[i]['name'])
            city_pict = subprocess.Popen(
                ['phantomjs', '--ignore-ssl-errors=true', 'get_maps.js', cities[i]['dest_folder'],
                 str(cities[i]['width']),
                 str(cities[i]['height']),
                 str(cities[i]['zoom']),
                 cities[i]['format'],
                 str(cities[i]['quality']),
                 str(cities[i]['lat']),
                 str(cities[i]['lon']),
                 cities[i]['name']]
            )
            city_pict.wait()
        except Exception as e:
            configs.log.add('ERROR: %s \n\tSomething is not goin well... ' % e)


def main():
    while True:
        start_time = time.time()
        cities = load_plugins()
        take_picts(cities)
        elapsed_time = time.time() - start_time
        if elapsed_time < configs.hrdCodedTime:
            sleep_time = int(configs.hrdCodedTime-elapsed_time)
            configs.log.add('INFO: Ok, now I take little snooze for %d seconds.. ZZZzzZZ.' % sleep_time)
            time.sleep(sleep_time)
        else:
            configs.log.add('WARNING: Cycle took too long, no time to sleep')

if __name__ == '__main__':
    main()
