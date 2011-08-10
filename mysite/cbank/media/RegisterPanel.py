from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas import Window
from DjangoForm import Form
from pyjamas import log

from DataService import FormService

from __pyjamas__ import JS

class RegisterPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="95%",
                               Spacing=5)
                               
        self.listener = listener
                               
        self.form_panel = VerticalPanel(Spacing=5) 
        
        
        self.form_panel.add(Label(JS('gettext("Create an account")')))
        
        button_box = HorizontalPanel(Width="100%")
        
        submit_button = Button(JS('gettext("Create the account")'), self.onSubmitButtonClick)
        cancel_button = Button(JS('gettext("Cancel")'), self.onCancelButtonClick)
        
        button_box.add(cancel_button)
        button_box.add(submit_button)
        button_box.setCellHorizontalAlignment(submit_button,
                                          HasAlignment.ALIGN_RIGHT)
        
        self.form_panel.add(button_box)
                     
        self.add(self.form_panel)
        
    def onShow(self):
        if not hasattr(self, 'form'):
            self.onFormLoad()
        else:
            #self.form.clear()
            pass
               
    def onFormLoad(self):
        self.formsvc = FormService(['usercreationform'])
        
        self.form = Form(getattr(self.formsvc, "usercreationform"), data = None,
                         listener=self)
        self.form_panel.insert(self.form, 1)
        
    def onErrors(self, form, response):
        log.writebr("onErrors %s" % repr(response))
        
    def onRetrieveDone(self, form):
        self.listener.onBackToLogin(self)
                        
    def onSubmitButtonClick(self, sender):
        self.form.save()
                             
    def onCancelButtonClick(self, sender):
        self.listener.onBackToLogin(self)
