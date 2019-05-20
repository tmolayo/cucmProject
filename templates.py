import json
from jinja2 import Template


class GeneralTemplate:
    def __init__(self, path, **kwargs):
        with open(path) as file:
            config = json.load(file)

        if kwargs is not None:
            config = Template(json.dumps(config))
            config = config.render(**kwargs)
            self.attributes = json.loads(config)


class Phone(GeneralTemplate):
    def __init__(self, path='./configuration/phone.json', **kwargs):
        GeneralTemplate.__init__(self, path=path, **kwargs)


class Line(GeneralTemplate):
    def __init__(self, path='./configuration/line.json', **kwargs):
        GeneralTemplate.__init__(self, path=path, **kwargs)


class PhoneWithLine(GeneralTemplate):
    def __init__(self, path='./configuration/phoneWithLine.json', **kwargs):
        GeneralTemplate.__init__(self, path=path, **kwargs)


# print(PhoneWithLine(name='dani123', id=8129664, uuid=12323123).attributes)
