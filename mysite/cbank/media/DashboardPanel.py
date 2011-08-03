# -*- coding: UTF-8 -*-
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.SimplePanel import SimplePanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.FormPanel import FormPanel
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.Hyperlink import Hyperlink
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.Hidden import Hidden
from pyjamas.ui.MenuBar import MenuBar
from pyjamas.ui.MenuItem import MenuItem
from pyjamas import Window
from pyjamas.ui.HTML import HTML

from IntroSink import IntroSink
from AccountsSink import AccountsSink

from DataService import DataService

class MenuCmd:

    def __init__(self, handler):
        self.handler = handler

    def execute(self):
        self.handler()
        
class DashboardPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self,
                               #HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               #VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="100%",
                               Spacing=5)
                               
        self.listener = listener
        
        self.remote = DataService(['logout'])
        
        self.cursink=None
        self.introsink = IntroSink()
        self.accountssink = AccountsSink()
        
        menu_account = MenuBar(vertical=True)
        menu_account.addItem(u"My Accounts", MenuCmd(self.onMyAccounts))
        
        menubar = MenuBar(vertical=False)
        menubar.addItem(MenuItem(u"Account", menu_account))
        menubar.addItem(u"Logout", MenuCmd(self.onLogoutButtonClick))
                              
        self.sinkcontainer = SimplePanel()
        self.sinkcontainer.setHeight("100%")
         
        self.add(menubar)                          
        self.add(self.sinkcontainer)
        self.setCellHeight(self.sinkcontainer, "100%")
        
        
    def onMyAccounts(self, sender):
        self.showSink('accountssink')
        
    def onLogoutButtonClick(self, sender):
        self.remote.logout(self)
        
    def showSink(self, sink):
        if self.cursink <> None:
            self.sinkcontainer.remove(getattr(self, self.cursink))
            
        self.cursink = sink
        s = getattr(self, self.cursink)
        self.sinkcontainer.add(s)
        if hasattr(s, 'onShow'):
            s.onShow()
        
    def onShow(self):
        self.showSink('introsink')           
         
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
        
