from libs import logs
import platform

appName = ''

actOS = platform.system().upper()
coolOs = True if actOS != 'WINDOWS' else False
log = logs.log('log-%s_' % appName, actOS)

plugins_confs={
    "folder": "plugins",
    "ext": "plugin"
}

hrdCodedTime = 120