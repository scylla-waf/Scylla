#!/usr/bin/python3

from scylla import Config
from scylla_dependencies.WAF.parser.parsepetition import *  # parse GET, POST, get type of request...
from urllib.parse import unquote

class Analizer:

    def __init__(self, learn):
        self.parser = Parsepetition()
        self.blacklist = self.parser.getarray("config/blacklist.conf")  # load blacklist
        self.config = Config()
        self.learn = learn  # should AI learn or detect ?

    def log_attack(self, petition, attack, ip):
        if "GET" in self.parser.get_method(petition):
            parameters = petition.decode("utf-8").split("\r\n")[:1]
        elif "POST" in self.parser.get_method(petition):
            parameters = petition.decode("utf-8").split("\r\n")[-1]
        else:
            parameters = petition
        print("Blocked: " + str(attack))
        print("IP: " + str(ip))
        print("User-Agent: " + str(self.parser.parse_headers(petition)["User-Agent"]))
        print("Petition: " + str(parameters))

        with open("scylla_dependencies/WAF/log/petition.log", "a") as f:
            f.writelines("Detected: " + str(attack) + "\n")
            f.writelines("IP: " + str(ip) + "\n")
            f.writelines("Petition: " + str(parameters) + "\n")
            f.writelines("By User-Agent: " + str(self.parser.parse_headers(petition)["User-Agent"]))
            f.writelines("\n\n")

    def simple_analysis(self, petition, getorpost, ip):  # first blacklist analysis
        for i in getorpost:
            for list in self.blacklist:
                if getorpost[i] in list:
                    self.log_attack(petition, getorpost[i], ip)
                    return True
        return False

    def blockIP(self, petition, ip):
        with open("scylla/waf/ip.list") as fp:
            line = fp.readline()
            cnt = 1
            while line:

                if ip is line.strip():
                    print("Es la ip")
                    self.log_attack(petition, "Blocked IP", ip)
                    return True

                line = fp.readline()
            cnt += 1
            print(line)
            return False


    def verb_analysis(self, petition, ip):  # petition is raw
        allowed = self.config.getconfig("scylla_dependencies/WAF/waf.conf")["allowed_verbs"].split(
            ",")  # get allowed methods
        if self.parser.get_method(petition) not in allowed:  # if method not allowed
            reason = self.parser.get_method(petition) + " method used "  # print the used verb
            self.log_attack(petition, reason, ip)  # log it
            return True  # attack
        return False

    def request_analysis(self, data, ip):  # start request analysis

        if "GET" in self.parser.get_method(data):  # if GET

            get_data = data.decode("utf-8").split("\r\n")[:1]  # url decode
            get_data = ''.join(get_data)
            get_data = get_data.split("GET ")[1]
            get_data = ''.join(get_data)
            get_data = get_data.split(" ", 1)[0]  # returns url

            data = data.replace(bytes(get_data, encoding="utf-8"), bytes(unquote(get_data), encoding="utf-8"))  # URL decode
            if self.simple_analysis(data, self.parser.parse_get(data),ip): return True
        else:
            if self.simple_analysis(data, self.parser.parse_post(data), ip): return True
            if self.verb_analysis(data, ip): return True  # if used a blocked verb...

    def response_analysis(self):  # main def to start response analysis
        pass

    def scylla(self, received, conn_type, con_data):  # main def of firewall
        blocked = self.config.getconfig("scylla_dependencies/WAF/waf.conf")["replace"].split(
            ":")  # get chars to block
        for i in blocked:
            received.replace(bytes(i, encoding="utf-8"), b" ")  # remove bad chars

        if conn_type is 0:  # analyze petitions
            # if bad return / else return normal petition
            return received if not self.request_analysis(received, con_data[0]) else bytes(
                "GET / HTTP/1.1\r\nHost: 127.0.0.1:4440\r\nUser-Agent: curl/7.64.0\r\nAccept: */*\r\n\r\n",
                encoding='utf8')  # if True ( blocked ) return /

        else:  # analyze response
            return received  # response analysis
