from pyjamas import DOM
from pyjamas.ui.Label import Label

class PseudoLink(Label):
    def __init__(self, text=None, listener=None, **kwargs):
        if not kwargs.has_key('Element'):
            element = DOM.createElement('a')
            element.setAttribute("href", "javascript:void(0)")
            kwargs['Element'] = element
        if not kwargs.has_key('StyleName'):
            kwargs['StyleName'] = "pseudolink"
            
        Label.__init__(self, text, True, **kwargs)
        if listener:
            self.addClickListener(listener)

