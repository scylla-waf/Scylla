#!/usr/bin/python3

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

    config = Config()  # instance of Config class
    options = config.getconfig("config/scylla.conf")
    proxy = Proxy(options["proxyhost"], options["proxyport"], options["server_addr"], options["server_port"],
                  options["maxlength"])  # instance of Proxy class

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
        # print("Starting HTTP Server in {}:{}".format(options["HTTPhost"], options["HTTPport"]))  # start DJango ?
        # startHTTP(options)
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
