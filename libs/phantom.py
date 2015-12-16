import time
import subprocess
import json
import os
from confs import configs


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


def load_map_filters():
    mask_types = []
    map_filter_folder = os.path.join('.',configs.maskFilterFolder)
    for f in os.listdir(map_filter_folder):
        if f.endswith('.filter'):
            file_path = os.path.join(map_filter_folder, f)
            try:
              with open(file_path,'r') as ff:
                  filter_cont = ff.readlines()
            except Exception as e:
                configs.log.add('FATAL ERROR: can\' read filter file {filter}'.format(filter=f))
                exit()
            nf = {
              'name': f.split('.')[1],
              'filter': str(filter_cont),
            }
            mask_types.append(nf)
    return mask_types


def build_mask_set(data_plugin):
    for plugin in data_plugin:
        maskTypes =  load_map_filters()
        for mask in maskTypes:
            if not '{mask_name}_{mask_type}.msk'.format(mask_name=plugin['name'], mask_type=mask['name']) in os.listdir(plugin['dest_folder']):
                configs.log.add('INFO: Building masks \"{mask_type}\" for: {city}'.format(city=plugin['name'], mask_type=mask['name']))
                try:
                    subprocess.Popen([
                    'phantomjs',
                    '--ignore-ssl-errors=true',
                    './libs/create_masks.js',
                    plugin['dest_folder'],
                    str(plugin['width']),
                    str(plugin['height']),
                    str(plugin['zoom']),
                    plugin['format'],
                    str(plugin['quality']),
                    str(plugin['lat']),
                    str(plugin['lon']),
                    plugin['name'],
                    mask['name']])                    
                    configs.log.add('INFO: process Build Mask for: {city}, type:{mask_type} successful launched :D '.format(city=plugin['name'], mask_type=mask['name']))
                except Exception as e:
                    configs.log.add('WARNING: Can\'t create the mask({mask_type}) for {city}\n\t\t{error}'.format(city=plugin['name'], error=e, mask_type=mask['name']))            
       
def take_picts(cities):
    for city in cities:
        try:
            configs.log.add('INFO: Taking picts of %s' % city['name'])
            subprocess.Popen([
                'phantomjs',
                '--ignore-ssl-errors=true',
                './libs/get_maps.js',
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
    while True:
        start_time = time.time()
        cities = load_plugins()
        build_mask_set(cities)
        take_picts(cities)
        elapsed_time = time.time() - start_time
        if elapsed_time < configs.hrdCodedTime:
            sleep_time = int(configs.hrdCodedTime-elapsed_time)
            configs.log.add('INFO: Ok, now I take little snooze for %d seconds.. ZZZzzZZ.' % sleep_time)
            time.sleep(sleep_time)
        else:
            configs.log.add('WARNING: Cycle took too long, no time to sleep... :(')
