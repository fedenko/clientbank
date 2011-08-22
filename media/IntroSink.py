# -*- coding: UTF-8 -*-
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui import HasAlignment
from pyjamas.ui.Label import Label

from __pyjamas__ import JS

class IntroSink(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self,
                               HorizontalAlignment=HasAlignment.ALIGN_CENTER,
                               VerticalAlignment=HasAlignment.ALIGN_MIDDLE,
                               Width="100%",
                               Height="100%",
                               Spacing=5)
        self.add(Label(JS('gettext("Hello, \%username\%!")')))
