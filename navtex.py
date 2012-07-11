import serial
import smtplib
import time
import ConfigParser
import sys

def readConfig(configfile):
    config = ConfigParser.RawConfigParser()
    config.read(configfile)
    res = {
           "server":config.get("email", "server"),
           "username":config.get("email", "username"),
           "password":config.get("email","password"),
           "sender": config.get("email","sender"),
           "recipient":config.get("email","recipient"),
           "serialport":config.get("serial","port"),
           "baudrate":config.getint("serial","baud")
           }
    return res

def sendMessage(message,config):
    print message
    smtp = smtplib.SMTP(config["server"]);
    smtp.login(config["username"],config["password"]);
    smtp.sendmail(config["sender"],config["recipient"],message)
    smtp.quit()

def getConfigFilename():
    if (len(sys.argv) > 1):
        return sys.argv[1]
    else:
        print "Usage: python navtex.py configfile.cfg"
        return None

#Read config-filename from commandline argument
configfilename = getConfigFilename()
if configfilename == None:
    sys.exit(0)

#read configfile
config = readConfig(configfilename)
print "Using config: "
print config

#init serial port
try:
    ser = serial.Serial(config["serialport"],config["baudrate"],timeout=None)
except:
    print "Error: cannot connect to serial port"
    sys.exit(1)

#waiting for messages
print "waiting for new..."
message = ""
for line in ser:
    print line
    if line.startswith(">"):
        lt = time.localtime()
        message = time.strftime("%Y-%m-%d %H:%M:%S\n",lt)
    if line.startswith("<"):
        message += line
        sendMessage(message)
    else:
        message += line
