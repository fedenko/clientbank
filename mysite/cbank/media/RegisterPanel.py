from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas import Window
from pyjamas.django.Form import Form
from pyjamas import log

from pyjamas.Cookies import getCookie

from __pyjamas__ import JS

from DataService import DataService, FormService

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
                
        grid.setWidget(0, 0, Label(JS('gettext("Username:")')))
        self.tb = TextBox(Name="username") 
        grid.setWidget(0, 1, self.tb)
        
        grid.setWidget(1, 0, Label(JS('gettext("Password:")')))
        self.ptb1 = PasswordTextBox(Name="password1")
        grid.setWidget(1, 1, self.ptb1)
        
        grid.setWidget(2, 0, Label(JS('gettext("Password confirmation:")')))
        self.ptb2 = PasswordTextBox(Name="password2")
        grid.setWidget(2, 1, self.ptb2)
        
        formatter = grid.getCellFormatter()
        
        for row in range(3):
            formatter.setAlignment(row, 0, hAlign = HasAlignment.ALIGN_RIGHT)
        
        vpanel.add(Label(JS('gettext("Create an account")')))
        vpanel.add(grid)
        
        hpanel = HorizontalPanel(Width="100%")
        
        submit_button = Button(JS('gettext("Create the account")'), self.onSubmitButtonClick)
        cancel_button = Button(JS('gettext("Cancel")'), self.onCancelButtonClick)
        
        hpanel.add(cancel_button)
        hpanel.add(submit_button)
        hpanel.setCellHorizontalAlignment(submit_button,
                                          HasAlignment.ALIGN_RIGHT)
        
        vpanel.add(hpanel)
                     
        self.add(vpanel)
        
    def onShow(self):
        self.onFormLoad()
                
    def onFormLoad(self):
        self.formsvc = FormService(['usercreationform'])
        
        self.form = Form(getattr(self.formsvc, "usercreationform"), data = None,
                         listener=self)
        self.add(self.form)
        
    def onErrors(self, form, response):
        log.writebr("onErrors %s" % repr(response))
        
    def onRetrieveDone(self, form):
        log.writebr("onRetrieveDone: %s" % repr(form))
                
        
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
            Window.alert(JS('gettext("Unrecognized JSONRPC method.")'))
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
