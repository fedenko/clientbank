from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Grid import Grid
from pyjamas.ui.Label import Label
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.PasswordTextBox import PasswordTextBox
from pyjamas.ui.Button import Button
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas import Window
from __pyjamas__ import JS, console

from DjangoForm import Form
from Widgets import PseudoLink
from DataService import FormService


class RegisterPanel(VerticalPanel):
    def __init__(self, listener):
        VerticalPanel.__init__(self, StyleName = "register")
                               
        self.listener = listener
                               
        self.form_panel = VerticalPanel(ID = "container", StyleName = "form")         
        
        self.form_panel.add(Label(JS('gettext("Create an account")')))
        
        button_box = HorizontalPanel(Width="100%")
        
        submit_button = Button(JS('gettext("Create the account")'), self.onSubmitButtonClick)
        cancel_button = PseudoLink(JS('gettext("Cancel")'), self.onCancelButtonClick)
        
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
            self.form.clear_errors()
               
    def onFormLoad(self):
        self.formsvc = FormService(['usercreationform'])
        
        self.form = Form(getattr(self.formsvc, "usercreationform"), data = None,
                         listener=self, StyleName = "uniForm")
        self.form_panel.insert(self.form, 1)
        
    def onErrors(self, form, response):
        console.log("onErrors %s" % repr(response))
        
    def onRetrieveDone(self, form):
        self.listener.onBackToLogin(self)
                        
    def onSubmitButtonClick(self, sender):
        self.form.save()
                             
    def onCancelButtonClick(self, sender):
        self.listener.onBackToLogin(self)
