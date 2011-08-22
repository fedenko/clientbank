""" Pyjamas Django Forms Integration

    Copyright (C) 2009 Luke Kenneth Casson Leighton <lkcl@lkcl.net>

"""
from pyjamas import DOM
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.Grid import Grid
from pyjamas.ui.FormPanel import FormPanel
#from pyjamas.ui.Composite import Composite
from __pyjamas__ import console


class CharField(TextBox):
    def __init__(self, **kwargs):
        if kwargs.get('input_type', 'text') == 'password':
            if not kwargs.has_key('Element'): 
                kwargs['Element'] = DOM.createInputPassword() 
            if not kwargs.has_key('StyleName'): 
                kwargs['StyleName']="gwt-PasswordTextBox" 
        TextBox.__init__(self, **kwargs)
        self.max_length = kwargs.get('max_length', None)
        self.min_length = kwargs.get('min_length', None)
        self.required = kwargs.get('required', None)
        if kwargs.get('initial'):
            self.setValue(kwargs['initial'])

    def setValue(self, val):
        if val is None:
            val = ''
        self.setText(val)

    def getValue(self):
        return self.getText()

class FloatField(TextBox):
    def __init__(self, **kwargs):
        TextBox.__init__(self)
        self.max_length = kwargs.get('max_length', None)
        self.min_length = kwargs.get('min_length', None)
        self.required = kwargs.get('required', None)
        if kwargs.get('initial'):
            self.setValue(kwargs['initial'])

    def setValue(self, val):
        if val is None:
            val = ''
        self.setText(val)

    def getValue(self):
        return self.getText()

widget_factory = {'CharField': CharField,
                  'FloatField': FloatField
                 }

class FormSaveGrid:

    def __init__(self, sink):
        self.sink = sink

    def onRemoteResponse(self,  response, request_info):

        method = request_info.method

        console.log(repr(response))
        console.log("%d" % len(response))
        console.log("%s" % repr(response.keys()))

        self.sink.save_respond(response)

class FormGetGrid:

    def __init__(self, sink):
        self.sink = sink

    def onRemoteResponse(self,  response, request_info):

        method = request_info.method

        console.log(method)
        console.log(repr(response))
        console.log("%d" % len(response))
        console.log("%s" % repr(response.keys()))

        self.sink.do_get(response)

    def onRemoteError(self, code, message, request_info):
        console.log("Server Error or Invalid Response: ERROR %d" % code + " - " + str(message) + ' - Remote method : ' + request_info.method)

class FormDescribeGrid:

    def __init__(self, sink):
        self.sink = sink

    def onRemoteResponse(self,  response, request_info):

        method = request_info.method

        console.log(method)
        console.log(repr(response))
        console.log("%d" % len(response))
        console.log("%s" % repr(response.keys()))

        self.sink.do_describe(response)

    def onRemoteError(self, code, message, request_info):
        writebr("Server Error or Invalid Response: ERROR %d" % code + " - " + str(message) + ' - Remote method : ' + request_info.method)

class Form(FormPanel):

    def __init__(self, svc, **kwargs):

        self.describe_listeners = []
        if kwargs.has_key('listener'):
            listener = kwargs.pop('listener')
            self.addDescribeListener(listener)

        if kwargs.has_key('data'):
            data = kwargs.pop('data')
        else:
            data = None
        console.log(repr(data))

        FormPanel.__init__(self, **kwargs)
        self.svc = svc
        self.grid = Grid()
        self.grid.resize(0, 3)
        self.add(self.grid)
        self.describer = FormDescribeGrid(self)
        self.saver = FormSaveGrid(self)
        self.getter = FormGetGrid(self)
        self.formsetup(data)

    def addDescribeListener(self, l):
        self.describe_listeners.append(l)

    def add_widget(self, description, widget):
        """ adds a widget, with error rows interspersed
        """

        num_rows = self.grid.getRowCount()
        self.grid.resize((num_rows+1), 3)
        self.grid.setHTML(num_rows, 0, description)
        self.grid.setWidget(num_rows, 1, widget)

    def get(self, **kwargs):
        console.log(repr(kwargs))
        self.svc({}, {'get': kwargs}, self.getter)

    def save(self, data=None):
        self.clear_errors()
        if data is None:
            data = self.getValue()
        self.data = data
        console.log(repr(self.data))
        self.svc(data, {'save': None}, self.saver)

    def save_respond(self, response):

        if not response['success']:
            errors = response['errors']
            self.set_errors(errors)
            for l in self.describe_listeners:
                l.onErrors(self, errors)
            return

        for l in self.describe_listeners:
            l.onSaveDone(self, response)
        
    def formsetup(self, data=None):

        if data is None:
            data = {}
        self.data = data
        console.log(repr(self.data))
        self.svc(data, {'describe': None}, self.describer)

    def clear_errors(self):

        for idx, fname in enumerate(self.fields):
            self.grid.setHTML(idx, 2, None)
            
    def set_errors(self, errors):

        offsets = {}
        for idx, fname in enumerate(self.fields):
            offsets[fname] = idx
        for k, err in errors.items():
            err = "<br />".join(err)
            idx = offsets[k]
            self.grid.setHTML(idx, 2, err)
            
    def update_values(self, data = None):
        if data is not None:
            self.data = data

        for idx, fname in enumerate(self.fields):
            val = None
            if self.data.has_key(fname):
                val = self.data[fname]
            w = self.grid.getWidget(idx, 1)
            w.setValue(val)

    def do_get(self, response):
        fields = response.get('instance', None)
        if fields:
            self.update_values(fields)
        for l in self.describe_listeners:
            l.onRetrieveDone(self, fields)

    def do_describe(self, fields):

        self.fields = fields.keys()
        for idx, fname in enumerate(self.fields):
            field = fields[fname]
            if self.data and self.data.has_key(fname):
                field['initial'] = self.data[fname]
            console.log("%s %s %d" % (fname, field['label'], idx))
            field_type = field['type']
            widget_kls = widget_factory.get(field_type, CharField)
            fv = {}
            for (k, v) in field.items():
                fv[str(k)] = v
            w = widget_kls(**fv)
            self.add_widget(field['label'], w)

        for l in self.describe_listeners:
            l.onDescribeDone(self)

    def getValue(self):

        res = {}
        for idx, fname in enumerate(self.fields):
            w = self.grid.getWidget(idx, 1)
            val = w.getValue()
            res[fname] = val
            self.data[fname] = val

        return res
