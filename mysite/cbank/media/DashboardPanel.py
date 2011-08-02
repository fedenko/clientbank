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


from DataService import DataService

class MenuCmd:

    def __init__(self, handler):
        self.handler = handler

    def execute(self):
        self.handler()
        
class IntroSink(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="100%",
                               Spacing=5)
        self.add(Label(u"Hello, %username%!"))
        
class AccountsSink(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self,
                               #HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               #VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               #Height="100%",
                               Spacing=5)
        self.grid = Grid(1, 1,
                    BorderWidth=1,
                    CellPadding=4,
                    CellSpacing=1)
        self.grid.setStyleName("grid")
        self.grid.setText(0, 0, u"Account Number")
        
        formatter = self.grid.getCellFormatter()
        formatter.setStyleName(0, 0, "grid-header")
        
        self.add(Label(u"Accounts"))
        
        self.add(self.grid)
        
    def setAccounts(self, accounts):
        rows = len(accounts)
        if rows > 0:
            self.grid.resize(rows+1, 1)
            for row in range(rows):
                self.grid.setText(row+1, 0, accounts[row])

class DashboardPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self,
                               #HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               #VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="100%",
                               Spacing=5)
                               
        self.listener = listener
        
        self.remote = DataService(['getaccounts', 'logout'])
        
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
        self.remote.getaccounts(self)
        
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
        elif request_info.method == 'getaccounts':
            self.showSink('accountssink')
            self.accountssink.setAccounts(response)
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
        
