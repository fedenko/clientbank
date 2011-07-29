from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.FormPanel import FormPanel
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.Hidden import Hidden
from pyjamas import Window

from DataService import DataService

class DashboardPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="95%",
                               Spacing=5)
                               
        self.listener = listener
        
        self.remote = DataService(['logout'])
                              
        vpanel = VerticalPanel(Spacing=5) 
        vpanel.add(Label("Some dashboard panel"))
        logout_button = Button("logout", self.onLogoutButtonClick)
        vpanel.add(logout_button)
                                  
        self.add(vpanel)
        
    def onLogoutButtonClick(self, sender):
        self.remote.logout(self)            
         
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'logout':
            if response == True:
                self.listener.onBackToLogin(self)
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
         

       
