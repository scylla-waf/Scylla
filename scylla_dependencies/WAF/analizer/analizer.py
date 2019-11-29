#!/usr/bin/python3

from urllib.parse import unquote
import ast  # for eval() dict

from scylla import Config
from scylla_dependencies.WAF.intelligence.intelligence import *
from scylla_dependencies.WAF.learn.trainAI import *
from scylla_dependencies.WAF.parser.parsepetition import *  # parse GET, POST, get type of request...


class Analizer:

    def __init__(self, learn):
        self.parser = Parsepetition()
        self.blacklist = self.parser.getarray("config/blacklist.conf")  # load blacklist
        self.config = Config()
        self.learn = learn  # should AI learn or detect ?
        self.deffendbyAI = IntelligentDetect()
        self.train = trainAI()

    def AI(self, dict):
        for i in dict:
            if self.learn:
                self.train.learn_from_petitions(dict[i])
            else:
                if self.deffendbyAI.identify(dict[i]):
                    return True
                else:
                    return False

    def variable_type(self, petition, dict, ip):
        variable1 = self.config.getconfig("config/variables.conf")  # ex. {"id": "numeric', "lol":"string"}

        numeric = variable1["numeric"]  # get numeric
        string = variable1["string"]  # get string
        strange = variable1["strange"]  # get strange

        for key in dict:  # for each variable
            if key in variable1:  # if variable in conf file
                type = variable1[key]  # type is the value of variable in conf file
                for i in dict[key]:
                    if type == "numeric":
                        testin = numeric
                    elif type == "string":
                        testin = string
                    else:
                        testin = strange
                    if not str(i) in testin:
                        self.log_attack(petition, "Used bad type in " + key, ip)
                        return True  # blocked
                return False

    def log_attack(self, petition, attack, ip):
        if "GET" in self.parser.get_method(petition):
            parameters = petition.decode("utf-8").split("\r\n")[:1]
        elif "POST" in self.parser.get_method(petition):
            parameters = petition.decode("utf-8").split("\r\n")[-1]
        else:
            parameters = petition

        print("Blocked: " + str(attack))
        print("IP: " + str(ip))
        try:
            print("User-Agent: " + str(self.parser.parse_headers(petition)["User-Agent"]))
        except:
            pass
        print("Petition: " + str(parameters))

        with open("scylla_dependencies/WAF/log/petition.log", "a") as f:
            f.writelines("Detected: " + str(attack) + "\n")
            f.writelines("IP: " + str(ip) + "\n")
            f.writelines("Petition: " + str(parameters) + "\n")
            try:
                f.writelines("By User-Agent: " + str(self.parser.parse_headers(petition)["User-Agent"]))
            except:
                f.writelines("By User-Agent: Cant Detect UA")
            f.writelines("\n*\n")

    def simple_analysis(self, petition, getorpost, ip):  # first blacklist analysis
        for i in getorpost:
            for list in self.blacklist:
                if getorpost[i] in list:
                    self.log_attack(petition, getorpost[i], ip)
                    return True
        return False

    def blockIP(self, petition, ip):

        with open("scylla_dependencies/WAF/ip.list") as fp:
            ips = fp.readlines()
            for ip_list in ips:
                if ip_list == ip:
                    self.log_attack(petition, "Blocked IP", ip)
                    return True
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
        if not self.learn:
            if "GET" in self.parser.get_method(data):  # if GET
                get_data = data.decode("utf-8").split("\r\n")[:1]  # url decode
                get_data = ''.join(get_data)
                get_data = get_data.split("GET ")[1]
                get_data = ''.join(get_data)
                get_data = get_data.split(" ", 1)[0]  # returns url

                data = data.replace(bytes(get_data, encoding="utf-8"),
                                    bytes(unquote(get_data), encoding="utf-8"))  # URL decode
                # if self.AI(self.parser.parse_get(data)): return True
                if self.variable_type(data, self.parser.parse_get(data), ip): return True
                if self.simple_analysis(data, self.parser.parse_get(data), ip): return True
                if self.blockByLen(data, self.parser.parse_get(data),ip): return True
            else:
                # if self.AI(self.parser.parse_post(data)): return True
                if self.variable_type(data, self.parser.parse_post(data), ip): return True
                if self.simple_analysis(data, self.parser.parse_post(data), ip): return True
                if self.verb_analysis(data, ip): return True  # if used a blocked verb...
                if self.blockByLen(data, self.parser.parse_post(data), ip): return True

        else:
            pass  # analiza IA

    def response_analysis(self):  # main def to start response analysis
        pass

    def savepetition(self, file, method):
        with open(file, "a+") as f:
            f.writelines("," + method)

    def blockByLen(self, petition, variables_dict, ip):
        with open("scylla_dependencies/WAF/log/len_block.log", "r") as f:
            length_dict = f.readlines()
            length_dict = ''.join(length_dict)
            try:
                length_dict = ast.literal_eval(length_dict)
            except Exception:
                print("Bad len_block.log")
                exit()

        for variable in variables_dict:
            if variable in length_dict:
                if len(variables_dict[variable]) * 0.25 >= length_dict[
                    variable]:  # if variable is 175 % bigger of average
                    attack = "'" + str(variables_dict[variable]) + "' is too big, average: " + str(
                        length_dict[variable]) + " digits"
                    self.log_attack(petition, attack, ip)
                    return True
                else:
                    new_len = (len(variables_dict[variable]) + length_dict[variable]) / 2
                    new_len = int(new_len)
                    length_dict[variable] = new_len

            else:
                new_len = int(len(variables_dict[variable]))
                length_dict[variable] = new_len  # if variable is new add it to file
        print("[DEBUG] Saving : " + str(length_dict))
        with open("scylla_dependencies/WAF/log/len_block.log", "w+") as f:
            f.writelines(str(length_dict))
        return False

    def scylla(self, received, conn_type, con_data):  # main def of firewall

        blocked = self.config.getconfig("scylla_dependencies/WAF/waf.conf")["replace"].split(
            ":")  # get chars to block

        for i in blocked:
            received.replace(bytes(i, encoding="utf-8"), b" ")  # remove bad chars

        if conn_type is 0:  # analyze petitions
            # if bad return / else return normal petition
            if not self.request_analysis(received, con_data[0]):
                self.savepetition("scylla_dependencies/WAF/log/good.log", self.parser.get_method(received))
                return received
            else:
                return bytes("GET / HTTP/1.1\r\nHost: 127.0.0.1:4440\r\nUser-Agent: curl/7.64.0\r\nAccept: */*\r\n\r\n",
                             encoding='utf8')  # if True ( blocked ) return /

        else:  # analyze response
            return received  # response analysis
