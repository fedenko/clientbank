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

class LoginPanel(VerticalPanel):
    def __init__(self, handler=None ):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="95%",
                               Spacing=5)
                               
        self.handler = handler                      
                               
        self.form = FormPanel()
        
        self.form.setAction("/accounts/login/")        
        self.form.setEncoding(FormPanel.ENCODING_MULTIPART)
        self.form.setMethod(FormPanel.METHOD_POST)
                         
        vpanel = VerticalPanel(Spacing=5) 
        
        self.form.setWidget(vpanel)                  

        grid = Grid(2, 2,
                    BorderWidth=0,
                    CellPadding=5,
                    CellSpacing=0)
                
        grid.setWidget(0, 0, Label("Username:"))
        grid.setWidget(0, 1, TextBox(Name="username"))
        
        grid.setWidget(1, 0, Label("Password:"))
        grid.setWidget(1, 1, PasswordTextBox(Name="password"))
        
        formatter = grid.getCellFormatter()
        formatter.setAlignment(0, 0, hAlign = HasAlignment.ALIGN_RIGHT)
        formatter.setAlignment(1, 0, hAlign = HasAlignment.ALIGN_RIGHT)
        
        login_button = Button("Login", self)
        
        
        vpanel.add(Hidden("csrfmiddlewaretoken", getCookie('csrftoken')))
        vpanel.add(Label("User Login"))
        vpanel.add(grid)
        vpanel.add(login_button)
        vpanel.setCellHorizontalAlignment(login_button,
                                          HasAlignment.ALIGN_RIGHT)
                                          
                                          
        self.form.addFormHandler(self)                                  
        self.add(self.form)
                
        
    def onClick(self, sender):
        self.form.submit()
        
    def onSubmitComplete(self, event):
        # When the form submission is successfully completed, this event is
        # fired. Assuming the service returned a response of type text/plain,
        # we can get the result text here (see the FormPanel documentation for
        # further explanation).
        if self.handler != None:
            self.handler(event)
        else:
            Window.alert(event.getResults())

    def onSubmit(self, event):
        pass
       
