""" Pyjamas Django Forms Integration

    Copyright (C) 2009 Luke Kenneth Casson Leighton <lkcl@lkcl.net>

"""
from pyjamas import DOM
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.Grid import Grid
from pyjamas.ui.FormPanel import FormPanel
#from pyjamas.ui.Composite import Composite
from pyjamas.ui.FlowPanel import FlowPanel
from pyjamas.ui.Label import Label
from __pyjamas__ import console


class FormLabel(Label):
    def __init__(self, text=None, forid=None, wordWrap=True, **kwargs):
        if not kwargs.has_key('Element'):
            element = DOM.createLabel()
            if forid: 
                element.setAttribute("for", forid)
            kwargs['Element'] = element
        Label.__init__(self, text, wordWrap, **kwargs)
        
class ErrorLabel(Label):
    def __init__(self, text=None, wordWrap=True, **kwargs):
        if not kwargs.has_key('Element'):
            kwargs['Element'] = DOM.createElement('p')
        if not kwargs.has_key('StyleName'):
            kwargs['StyleName'] = "errorField"
        Label.__init__(self, text, wordWrap, **kwargs)
        
class CtrlHolder(FlowPanel):
    def __init__(self, name, description, widget, **kwargs):
        if not kwargs.has_key('StyleName'):
            kwargs['StyleName'] = "ctrlHolder"
        if not kwargs.has_key('ID'):
            kwargs['ID'] = "div_id_%s" % name
        FlowPanel.__init__(self, **kwargs)
        
        self.errors = []
        
        self.label = FormLabel(description, "id_%s" % name)
        self.widget = widget
        self.widget.setID("id_%s" % name)
        self.widget.setName(name)
            
        self.add(self.label)
        self.add(self.widget)
        
    def insert(self, widget, beforeIndex):
        if widget.getParent() == self: 
            return
            
        widget.removeFromParent()            
        DOM.insertChild(self.getElement(), widget.getElement(), beforeIndex)        
        widget.setParent(self)
        self.children.insert(beforeIndex, widget)
        
    def getValue(self):
        return self.widget.getValue()
        
    def setValue(self, val):
        self.widget.setValue(val)
            
    def setErrors(self, errors):
        for error in self.errors:
            self.remove(error)
            self.errors.remove(error)
            
        if errors:
            errors.reverse()
            for err in errors:
                w = ErrorLabel(err)
                self.errors.append(w)
                self.insert(w, 0)

class FieldSet(FlowPanel):
    def __init__(self, **kwargs):
        if not kwargs.has_key('Element'):
            kwargs['Element'] = DOM.createElement('fieldset')
        self.fields = {}
        FlowPanel.__init__(self, **kwargs)
        
    def addField(self, name, description, widget):
        if not self.fields.has_key(name):
            self.fields[name] = CtrlHolder(name, description, widget)
            self.add(self.fields[name])
            
    def removeField(self, fname):
        if self.fields.has_key(fname):
            self.remove(self.fields[fname])
            del self.fields[fname]
            
    def getValue(self, fname):
        if self.fields.has_key(fname):
            return self.fields[fname].getValue()
        else:
            return None
        
    def setValue(self, fname, val):
        if self.fields.has_key(fname):
            self.fields[fname].setValue(val)
        
    def setErrors(self, fname, errors=None):
        if self.fields.has_key(fname):
            self.fields[fname].setErrors(errors)


class CharField(TextBox):
    def __init__(self, **kwargs):
        if kwargs.get('input_type', 'text') == 'password':
            if not kwargs.has_key('Element'): 
                kwargs['Element'] = DOM.createInputPassword() 
            #if not kwargs.has_key('StyleName'): 
            #    kwargs['StyleName']="gwt-PasswordTextBox"
        if not kwargs.has_key('StyleName'): 
            kwargs['StyleName']="textInput"
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

class FormSavePanel:

    def __init__(self, sink):
        self.sink = sink

    def onRemoteResponse(self,  response, request_info):

        method = request_info.method

        console.log(repr(response))
        console.log("%d" % len(response))
        console.log("%s" % repr(response.keys()))

        self.sink.save_respond(response)

class FormGetPanel:

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

class FormDescribePanel:

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
        self.fieldset = FieldSet(StyleName = "inlineLabels")
        self.add(self.fieldset)
        self.describer = FormDescribePanel(self)
        self.saver = FormSavePanel(self)
        self.getter = FormGetPanel(self)
        self.formsetup(data)

    def addDescribeListener(self, l):
        self.describe_listeners.append(l)

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
        for fname in self.fields:
            self.fieldset.setErrors(fname, None)
            
    def set_errors(self, errors):
        for fname, err in errors.items():
            self.fieldset.setErrors(fname, err)
            
    def update_values(self, data = None):
        if data is not None:
            self.data = data

        for fname in self.fields:
            val = None
            if self.data.has_key(fname):
                val = self.data[fname]
            self.fieldset.setValue(fname, val)

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
            self.fieldset.addField(fname, field['label'], w)

        for l in self.describe_listeners:
            l.onDescribeDone(self)

    def getValue(self):

        res = {}
        for fname in self.fields:
            val = self.fieldset.getValue(fname)
            res[fname] = val
            self.data[fname] = val

        return res
