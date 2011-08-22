from pyjamas.Cookies import getCookie
from pyjamas.JSONService import JSONProxy

class DataService(JSONProxy):
    def __init__(self, methods):
        JSONProxy.__init__(self, 'services/', methods, {'X-CSRFToken': getCookie('csrftoken')})
        
class FormService(JSONProxy):
    def __init__(self, methods):
        JSONProxy.__init__(self, "formservice/", methods, {'X-CSRFToken': getCookie('csrftoken')})
