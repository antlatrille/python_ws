from bottle import Bottle, route, get, post, request
import json


class Api(Bottle):
    def __init__(self):
        super(Api, self).__init__()
        self.description = []
        self._route('/description', 'GET', self._description)

    def _route(self, path, method, callback):
        # add description
        self.description.append(
            {'path': path.replace('<', ':').replace('>', ''), 'method': method, 'doc': callback.__doc__})
        self.route(path, method=method, callback=callback)

    def _description(self):
        return json.dumps(self.description, indent=4)


class Api_v1(Api):
    def __init__(self):
        super(Api_v1, self).__init__()
        self._route('/hello/<id>', 'GET', self.hello)
        self._route('/hello/<id>', 'POST', self.hello_post)

    def hello(self, id):
        """says hello with a path param"""
        return f'Hello {str(id)}'

    def hello_post(self, id):
        """says hello too, with a path param and some json data"""
        return f'Hello too {str(id)}, you asked {str(request.json)}'
