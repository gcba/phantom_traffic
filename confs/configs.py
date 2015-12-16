from libs import logs
import platform

appName = ''

actOS = platform.system().upper()
coolOs = actOS != 'WINDOWS'
log = logs.Log('logs', 'log-%s_' % appName, actOS)

plugins_confs = {
    "folder": "plugins",
    "ext": "plugin"
}
imgFolder = './IMG'
hrdCodedTime = 120

map_filter_ext = 'filter'
maskFilterFolder = './libs/filters'
maskTypes = []