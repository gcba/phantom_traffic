import subprocess
import time
import json
import os
from confs import configs
cities = []

def loadPlugins():
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
                    'times_per_hour':d['obs_time']['obs_per_hour'],
                    'start_at':d['obs_time']['start'],
                    'ends_at':d['obs_time']['end'],
                    'dest_folder': d['render']['str_folder'],
                    'format': d['render']['out_format'],
                    'quality': d['render']['quality'],
                }
            configs.log.add('INFO: \"%s\" plugin loaded...' % d['name'])
            folder = './%s' % c['dest_folder']
            if not os.path.exists(folder):
                os.mkdir(folder)
            cities.append(c)
            c = {}
    configs.log.add('INFO: %d Cities loaded!' % len(cities))

def takePicts():
    for i in range(0, len(cities)):
        try:
            configs.log.add('INFO: Taking picts from: %s' % cities[i]['name'])
            cityPict = subprocess.Popen(['phantomjs', '--ignore-ssl-errors=true', 'get_maps.js', cities[i]['dest_folder'], str(cities[i]['width']), str(cities[i]['height']), str(cities[i]['zoom']), cities[i]['format'], str(cities[i]['quality']), str(cities[i]['lat']), str(cities[i]['lon']), cities[i]['name']])
            cityPict.wait()
        except Exception as e:
            configs.log.add('ERROR: %s \n\tSomething is not goin well... ' % e)


def main():
    while True:
        st = time.time()
        loadPlugins()
        takePicts()
        et = time.time()
        snooze = int(configs.hrdCodedTime-(et - st)) if et - st < configs.hrdCodedTime else 0
        configs.log.add('INFO: Ok, now I take little snooze for %d seconds.. ZZZzzZZ.' %  snooze)
        time.sleep(snooze)


if __name__ == '__main__':
    main()
