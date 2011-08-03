# -*- coding: UTF-8 -*-
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label

from DataService import DataService

class AccountsSink(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self,
                               #HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               #VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               #Height="100%",
                               Spacing=5)
                               
        self.remote = DataService(['getaccounts'])
        
        self.accounts = []                       
                               
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
        
    def updateGrid(self):         
        rows = len(self.accounts)
        if rows > 0:
            self.grid.resize(rows+1, 1)
            for row in range(rows):
                self.grid.setText(row+1, 0, self.accounts[row])
                
    def onShow(self):
        self.remote.getaccounts(self)
        self.updateGrid()
                   
         
    def onRemoteResponse(self, response, request_info):
        '''
        Called when a response is received from a RPC.
        '''
        if request_info.method == 'getaccounts':
            #TODO
            self.self.accounts = response
        else:
            Window.alert('Unrecognized JSONRPC method.')
            
    def onRemoteError(self, code, message, request_info):
        Window.alert(message)
                
    
