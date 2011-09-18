from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas import Window
from Widgets import PseudoLink

from DataService import DataService

from __pyjamas__ import JS

class LoginPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self, StyleName = "login")
                               
        self.listener = listener
                               
        self.remote = DataService(['login'])                 
                               
        form_panel = VerticalPanel(ID = "container", StyleName = "form")
        
        self.error_message = Label(StyleName = "error-message") 
        
        grid = Grid(2, 2,
                    CellPadding=0,
                    CellSpacing=0,
                    StyleName = "form-grid")
                
        grid.setWidget(0, 0, Label(JS('gettext("Username:")'),
                                   StyleName = "label"))
        self.tb = TextBox(Name="username") 
        grid.setWidget(0, 1, self.tb)
        
        grid.setWidget(1, 0, Label(JS('gettext("Password:")'),
                                   StyleName = "label"))
        self.ptb = PasswordTextBox(Name="password")
        grid.setWidget(1, 1, self.ptb)
        
        form_panel.add(Label(JS('gettext("User Login")'), StyleName = "form-title"))
        form_panel.add(self.error_message)
        form_panel.add(grid)
        
        button_box = HorizontalPanel(Width="100%")
        
        register_button = PseudoLink(JS('gettext("Create an account")'),
                                 self.onRegisterButtonClick)
        submit_button = Button(JS('gettext("Login")'),
                               self.onSubmitButtonClick)
        
        button_box.add(register_button)
        button_box.add(submit_button)        
        
        button_box.setCellHorizontalAlignment(submit_button,
                                          HasAlignment.ALIGN_RIGHT)
        
        form_panel.add(button_box)
             
        self.add(form_panel)
        
    def onShow(self, sender):
        self.error_message.setText("")
                
    def onRegisterButtonClick(self, sender):
        self.listener.onRegister(self)
        
    def onSubmitButtonClick(self, sender):
        self.remote.login(self.tb.getText(), self.ptb.getText(), self)
        
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'login':
            if response['success']:
                self.listener.onLogin(self)
            else:
                self.error_message.setText(response['error_message'])
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
