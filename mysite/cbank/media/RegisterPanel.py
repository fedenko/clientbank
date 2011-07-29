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

class RegisterPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="95%",
                               Spacing=5)
                               
        self.listener = listener
                               
        self.remote = DataService(['register'])                 
                               
        vpanel = VerticalPanel(Spacing=5) 
        
        grid = Grid(3, 2,
                    BorderWidth=0,
                    CellPadding=5,
                    CellSpacing=0)
                
        grid.setWidget(0, 0, Label("Username:"))
        self.tb = TextBox(Name="username") 
        grid.setWidget(0, 1, self.tb)
        
        grid.setWidget(1, 0, Label("Password:"))
        self.ptb1 = PasswordTextBox(Name="password1")
        grid.setWidget(1, 1, self.ptb1)
        
        grid.setWidget(2, 0, Label("Password confirmation:"))
        self.ptb2 = PasswordTextBox(Name="password2")
        grid.setWidget(2, 1, self.ptb2)
        
        formatter = grid.getCellFormatter()
        
        for row in range(3):
            formatter.setAlignment(row, 0, hAlign = HasAlignment.ALIGN_RIGHT)
        
        vpanel.add(Label("Create an account"))
        vpanel.add(grid)
        
        hpanel = HorizontalPanel(Width="100%")
        
        submit_button = Button("Create the account", self.onSubmitButtonClick)
        cancel_button = Button("Cancel", self.onCancelButtonClick)
        
        hpanel.add(cancel_button)
        hpanel.add(submit_button)
        hpanel.setCellHorizontalAlignment(submit_button,
                                          HasAlignment.ALIGN_RIGHT)
        
        vpanel.add(hpanel)
                     
        self.add(vpanel)
                
        
    def onSubmitButtonClick(self, sender):
        self.remote.register(self.tb.getText(),
                             self.ptb1.getText(),
                             self.ptb2.getText(),
                             self)
                             
    def onCancelButtonClick(self, sender):
        self.listener.onBackToLogin(self)
        
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'register':
            if response == True:
                self.listener.onBackToLogin(self)
            else:
                #TODO
                Window.alert(response)
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
