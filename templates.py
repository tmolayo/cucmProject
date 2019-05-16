import json
from string import Template

#with open('config.json', 'r') as file:
#    config = json.load(file)


class Phone:
    def __init__(self, name):
        with open('./configuration/phone.json', 'r') as file:
            config = json.load(file)
            config = Template(json.dumps(config))
            config = config.safe_substitute(name=name)
        print(json.loads(config))
        self.attributes = config
        #self.attributes['name'] = name

    def __get__(self, instance, owner):
        return self.attributes

a = Phone(name='didid')
print(a.attributes)




class Phone1:

    def __init__(self, name):
        #self.attributes = config['COMPONENTS']['phone']
        self.attributes['name'] = name

    def __set__(self, instance, name):
        self.attributes['name'] = name

    def __delete__(self, instance):
        del self.attributes

    def __get__(self, instance, owner):
        return self.attributes


class Line:
    def __init__(self, lineId):
        lineId = str(lineId)
        #self.attributes = config['COMPONENTS']['line']
        self.attributes["pattern"] = lineId
        self.attributes["description"] = "description " + lineId
        self.attributes["alertingName"] = "alertingName " + lineId

    def __set__(self, instance, lineId):
        lineId = str(lineId)
        self.attributes["pattern"] = lineId
        self.attributes["description"] = "description " + lineId
        self.attributes["alertingName"] = "alertingName " + lineId

    def __get__(self, instance, owner):
        return self.attributes

    def __delete__(self, instance):
        del self.attributes


class PhoneWithLine:
    def __init__(self, phoneName, lineUuid, lineId):
        #self.attributes = config['COMPONENTS']['phoneWithLine']
        self.attributes['name'] = 'CSF' + phoneName
        self.attributes['lines']['line']['dirn']['uuid'] = lineUuid
        self.attributes['lines']['line']['dirn']['pattern'] = lineId

    def __set__(self, instance, phoneName, lineUuid, lineId):
        self.attributes['name'] = 'CSF' + phoneName
        self.attributes['lines']['line']['dirn']['uuid'] = lineUuid
        self.attributes['lines']['line']['dirn']['pattern'] = lineId

    def __get__(self, instance, owner):
        return self.attributes

    def __delete__(self, instance):
        del self.attributes