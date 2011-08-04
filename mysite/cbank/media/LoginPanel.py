from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas import Window

from DataService import DataService

from __pyjamas__ import JS

class LoginPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="95%",
                               Spacing=5)
                               
        self.listener = listener
                               
        self.remote = DataService(['login'])                 
                               
        vpanel = VerticalPanel(Spacing=5) 
        
        grid = Grid(2, 2,
                    BorderWidth=0,
                    CellPadding=5,
                    CellSpacing=0)
                
        grid.setWidget(0, 0, Label(JS('gettext("Username:")')))
        self.tb = TextBox(Name="username") 
        grid.setWidget(0, 1, self.tb)
        
        grid.setWidget(1, 0, Label(JS('gettext("Password:")')))
        self.ptb = PasswordTextBox(Name="password")
        grid.setWidget(1, 1, self.ptb)
        
        formatter = grid.getCellFormatter()
        formatter.setAlignment(0, 0, hAlign = HasAlignment.ALIGN_RIGHT)
        formatter.setAlignment(1, 0, hAlign = HasAlignment.ALIGN_RIGHT)
        
        vpanel.add(Label(JS('gettext("User Login")')))
        vpanel.add(grid)
        
        hpanel = HorizontalPanel(Width="100%")
        
        register_button = Button(JS('gettext("Create an account")'),
                                    self.onRegisterButtonClick)
        submit_button = Button("Login", self.onSubmitButtonClick)
        
        hpanel.add(register_button)
        hpanel.add(submit_button)        
        
        hpanel.setCellHorizontalAlignment(submit_button,
                                          HasAlignment.ALIGN_RIGHT)
        
        vpanel.add(hpanel)
                                                  
             
        self.add(vpanel)
                
    def onRegisterButtonClick(self, sender):
        self.listener.onRegister(self)
        
    def onSubmitButtonClick(self, sender):
        self.remote.login(self.tb.getText(), self.ptb.getText(), self)
        
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'login':
            if response == True:
                self.listener.onLogin(self)
            else:
                #TODO
                Window.alert(response)
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
