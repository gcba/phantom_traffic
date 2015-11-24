import time
import datetime
import sys


class log:
    def __init__(self, sufix, niceOS):
        self.logSufix = sufix
        if (niceOS):
            self.HEADER = '\033[95m'
            self.OKBLUE = '\033[94m'
            self.OKGREEN = '\033[92m'
            self.WARNING = '\033[93m'
            self.FAIL = '\033[91m'
            self.ENDC = '\033[0m'
            self.BOLD = '\033[1m'
            self.UNDERLINE = '\033[4m'
        else:
            self.HEADER = ""
            self.OKBLUE = ""
            self.OKGREEN = ""
            self.WARNING = ""
            self.FAIL = ""
            self.ENDC = ""
            self.BOLD = ""
            self.UNDERLINE = ""
        self.SESSION = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H_%M_%S')

    def add(self, msg):
        lColor = self.ENDC
        now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        filelog = "%s_%s.log" % (self.logSufix, self.SESSION)
        with open(filelog, 'a') as logFile:
            msgf = ">> [%s]: %s \n" % (now, msg)
            logFile.write(msgf)
            if (msg.find("ERROR") > -1):
                lColor = self.FAIL
            elif (msg.find("WARNING") > -1):
                lColor = self.BOLD + self.WARNING
            elif (msg.find("INFO") > -1):
                lColor = self.BOLD + self.OKGREEN
            else:
                lColor = self.ENDC
            msg = ">> %s[%s]%s %s \n" % (lColor, now, msg, self.ENDC)
            sys.stdout.write(msg)
