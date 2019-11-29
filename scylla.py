#!/usr/bin/python3

import sys, os
from scylla_dependencies.colors.colourandwarnings import colours, alerts, errors
from scylla_dependencies.proxy.proxy import *

__version__ = "1.0.0"


class Config:  # handle .conf files

    def __init__(self):
        pass

    def getconfig(self, file):  # returns dict of conf file
        conf = {}
        with open(file, "r+") as f:
            for line in f.readlines():
                if not "#" in line and "=" in line:
                    value = line.split("=")
                    value = [val.strip() for val in value]
                    conf.update({value[0]: value[1]})
        return conf


def init():  # start main
    print(colourful.red + "Starting Scylla [Paranoid Firewall]" + colourful.end + "\n")
    try:
        if sys.argv[1] is "learn":
            learn = True
        else:
            learn = False
    except:
        learn = False
    config = Config()  # instance of Config class
    options = config.getconfig("config/scylla.conf")
    proxy = Proxy(options["proxyhost"], options["proxyport"], options["server_addr"], options["server_port"],
                  options["maxlength"], learn)  # instance of Proxy class

    try:
        print("[*] Starting Proxy Server in {}:{}".format(options["proxyhost"], options["proxyport"]))
        t = threading.Thread(target=proxy.startproxy, args=())
        t.start()  # start proxy server threat

    except Exception as e:
        print(error.proxy)
        print(e)
        exit()

    try:
        pass
        try:
            print("Django Executed 127.0.0.1:{}".format(options["HTTPport"]))
            #Make Migrations
            command = 'python3 "scylla_dependencies/HTTPServer/scylla/manage.py" makemigrations > /dev/null'
            os.system(command)
            #Migrate
            command = 'python3 "scylla_dependencies/HTTPServer/scylla/manage.py" migrate > /dev/null'
            os.system(command)
            #Execute Django
            command = 'python3 "scylla_dependencies/HTTPServer/scylla/manage.py" runsslserver 127.0.0.1:' + options["HTTPport"] + ' > /dev/null 2>&1'
            os.system(command)
        except Exception as e:
            print("Error starting Django")
            print(e)
            exit()
    except Exception as e:
        print("Error starting HTTP server")
        print(e)
        exit()


if __name__ == "__main__":
    colourful = colours()  # instance if colours, use: colourful.red + " text " + colourful.end (end color) ( from
    # scylla_dependencies.colour_warnings.colourandwarnings )
    alert = alerts()  # instance of alerts (from scylla_dependencies.colour_warnings.colourandwarnings )
    error = errors()  # instance of errors (from scylla_dependencies.colour_warnings.colourandwarnings )
    try:
        init()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e)
        print(alert.unknown)
        exit()
