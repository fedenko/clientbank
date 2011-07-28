from pyjamas.ui.Label import Label
from pyjamas.ui.RootPanel import RootPanel
from LoginPanel import LoginPanel
from DashboardPanel import DashboardPanel
from pyjamas import Window

from pyjamas.Cookies import getCookie
from pyjamas.JSONService import JSONProxy
        
class ClientBank:
    def onModuleLoad(self):
    
        self.remote = DataService()
        
        self.curpanel = None
        self.loginpanel = LoginPanel(self.onSubmitComplete)
        self.dashboardpanel = DashboardPanel()

        self.remote.isAuthenticated(self)
        
    def onSubmitComplete(self, event):
        result = event.getResults()
        if result == "ok":
             self.showPanel('dashboardpanel')
        else: 
            Window.alert(result)
        
    def showPanel(self, panel):
        if self.curpanel <> None:
            RootPanel().remove(getattr(self, self.curpanel))
            
        self.curpanel = panel
        RootPanel().add(getattr(self, self.curpanel)) 
        
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'isAuthenticated':
            if response:
                self.showPanel('dashboardpanel')
            else:
                self.showPanel('loginpanel')
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
        
          
class DataService(JSONProxy):
    methods = ['isAuthenticated']
    
    def __init__(self):
        JSONProxy.__init__(self, 'services/', DataService.methods, {'X-CSRFToken': getCookie('csrftoken')})            

if __name__ == '__main__':    
    app = ClientBank()
    app.onModuleLoad()

