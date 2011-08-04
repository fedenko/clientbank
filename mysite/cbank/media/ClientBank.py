from pyjamas.ui.Label import Label
from pyjamas.ui.RootPanel import RootPanel
from LoginPanel import LoginPanel
from RegisterPanel import RegisterPanel
from DashboardPanel import DashboardPanel
from pyjamas import Window
import dynamic

from __pyjamas__ import JS

from DataService import DataService
        
class ClientBank:
    def onModuleLoad(self):
               
        dynamic.ajax_import("/jsi18n/", names = ['gettext'])
    
        self.remote = DataService(['isauthenticated'])
        
        self.curpanel = None
                                                        
        self.loginpanel = LoginPanel(self)              
        self.registerpanel = RegisterPanel(self)        
        self.dashboardpanel = DashboardPanel(self)      
        self.remote.isauthenticated(self)
        
    def onLogin(self, sender):
        self.showPanel('dashboardpanel')
        
    def onBackToLogin(self, sender):
        self.showPanel('loginpanel')
        
    def onRegister(self, sender):
        self.showPanel('registerpanel')
        
    def showPanel(self, panel):
        if self.curpanel <> None:
            RootPanel().remove(getattr(self, self.curpanel))
            
        self.curpanel = panel
        p = getattr(self, self.curpanel)
        RootPanel().add(p)
        if hasattr(p, 'onShow'):
            p.onShow()  
        
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'isauthenticated':
            if response == True:
                self.showPanel('dashboardpanel')
            else:
                self.showPanel('loginpanel')
        else:
            Window.alert(JS('gettext("Unrecognized JSONRPC method.")'))
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
        
if __name__ == '__main__':    
    app = ClientBank()
    app.onModuleLoad()

