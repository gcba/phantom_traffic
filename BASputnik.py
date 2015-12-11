import sys
import multiprocessing
import signal
from confs import configs
from confs import server_conf
from libs import phantom
from web import iGui

process = []


def start_thread(task):
    try:
        configs.log.add('INFO: Starting web-gui...')
        p = multiprocessing.Process(target=task)
        p.start()
        configs.log.add('INFO: love is in the air! and web-gui too!!!')
        process.append(p)
    except Exception as e:
        configs.log.add('ERROR: something going bad... can\'t start web-gui...[%s]' % e)


def signal_handler(signal, frame):
    for p in process:
        p.terminate()
    exit()
signal.signal(signal.SIGINT, signal_handler)


def main():
    params = sys.argv
    with_server = 'server' in params
    with_phantom = 'phantom' in params
    if with_server:
        start_thread(iGui.app.run(host='0.0.0.0', port=80))
    if with_phantom:
        start_thread(phantom.main)
    if not with_server and not with_phantom:
        configs.log.add('WARNING: No service launched')
    else:
        signal.pause()

if __name__ == '__main__':
    main()
