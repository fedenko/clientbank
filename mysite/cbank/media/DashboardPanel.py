from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.FormPanel import FormPanel
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.Hidden import Hidden
from pyjamas import Window
from pyjamas.Cookies import getCookie

class DashboardPanel(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="95%",
                               Spacing=5)
                               
                       
        vpanel = VerticalPanel(Spacing=5) 
        vpanel.add(Label("Some dashboard panel"))
                                  
        self.add(vpanel)

       
