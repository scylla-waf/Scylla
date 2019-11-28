#!/usr/bin/python3

class Parsepetition:

    def __init__(self):
        pass

    def getarray(self, file):  # get array of a file
        with open(file, "r+") as f:
            array_string = f.readlines()
            array_string = ''.join(array_string)
            array = eval(array_string.replace("\n", "").lower())
        return array

    def get_method(self, data):  # returns str of method (GET, POST...)
        method = data.decode("utf-8").split("\r\n")[:1]
        method = ''.join(method)
        method = method.split(" ", 1)[0]
        method = ''.join(method)

        return method

    def parse_headers(self, petition):  # returns dict with headers
        fields = petition.decode("utf-8").split("\r\n")[1:]
        headers = {}
        for field in fields:
            key, *value = field.split(":", 1)
            headers[key] = ''.join(value)

        return headers

    def parse_post(self, petition):  # returns dict with POST parameters, {} if none
        data = {}
        post = petition.decode("utf-8").split("\r\n")[-1]
        variables = post.split("&")
        try:
            for variable in variables:
                variable = ''.join(variable)
                parameter = variable.split("=")
                data[parameter[0]] = parameter[1]
        except:
            return {}  # if not variables return {}
        return data

    def parse_get(self, petition):  # returns dict with GET, {} if none
        data = {}
        get = petition.decode("utf-8").split("\r\n")[:1]
        get = ''.join(get)
        try:
            url = get.split("GET ")[1]
        except:  # is post
            return {}
        url = ''.join(url)
        url = url.split(" ", 1)[0]
        try:
            get = url.split("?", 1)[1]
        except:
            return {}  # no parameteres

        get = ''.join(get)
        variables = get.split("&")
        for variable in variables:
            variable = ''.join(variable)
            parameter = variable.split("=")
            data[parameter[0]] = parameter[1]
        return data 
