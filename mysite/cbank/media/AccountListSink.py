# -*- coding: UTF-8 -*-
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label

from pyjamas import Window

from DataService import DataService

class AccountListSink(VerticalPanel):
    def __init__(self, hendler = None):
        VerticalPanel.__init__(self,
                               #HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               #VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               #Height="100%",
                               Spacing=5)
                               
        self.remote = DataService(['getaccounts'])        
                               
        self.grid = Grid(1, 3,
                    BorderWidth=1,
                    CellPadding=4,
                    CellSpacing=1,
                    StyleName="grid")
        self.grid.setText(0, 0, u"Number")
        self.grid.setText(0, 1, u"Type")
        self.grid.setText(0, 2, u"Balance")
        
        formatter = self.grid.getRowFormatter()
        formatter.setStyleName(0, "grid-header")
        
        self.add(Label(u"Accounts"))
        
        self.add(self.grid)
        
    def updateGrid(self, accounts):         
        rows = len(accounts)
        if rows > 0:
            self.grid.resize(rows+1, 3)
            for row in range(rows):
                link = Label(text=accounts[row]['number'],
                             StyleName="pseudo-link",
                             ID=accounts[row]['number'])
                link.addClickListener(self.onClick)
                self.grid.setWidget(row+1, 0, link)
                self.grid.setText(row+1, 1, accounts[row]['type'])
                self.grid.setText(row+1, 2, accounts[row]['balance'])
                
    def onShow(self):
        self.remote.getaccounts(self)
        
    def onClick(self, sender):
        Window.alert(sender.getID())
         
                 
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'getaccounts':
            #TODO
            self.updateGrid(response)
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
                
    
