import datetime
import sys
import os


class Log:
    def __init__(self, folder_path, sufix, nice_os):
        self.folder_path = folder_path
        self.log_sufix = sufix
        if nice_os:
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
        self.SESSION = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')

    def add(self, msg):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        filelog = "%s_%s.log" % (self.log_sufix, self.SESSION)
        if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
        with open(os.path.join(self.folder_path, filelog), 'a') as logFile:
            msgf = ">> [%s]: %s \n" % (now, msg)
            logFile.write(msgf)
        if msg.find("ERROR") > -1:
            log_color = self.FAIL
        elif msg.find("WARNING") > -1:
            log_color = self.BOLD + self.WARNING
        elif msg.find("INFO") > -1:
            log_color = self.BOLD + self.OKGREEN
        else:
            log_color = self.ENDC
        msg = ">> %s[%s]%s %s \n" % (log_color, now, msg, self.ENDC)
        sys.stdout.write(msg)
