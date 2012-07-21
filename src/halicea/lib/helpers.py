#!/usr/bin/env python
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
from UserDict import DictMixin

class NotSuportedException(Exception):
    def __init__(self, message):
        self.message = message or "Operation is not supported"
    def __str__(self):
        return self.message

def ClassImport(name):
    components = name.split('.')
    mod = __import__('.'.join(components[:-1]), fromlist=[components[-1]])
    klass = getattr(mod, components[-1])
    return klass

class DynamicParameters(object):
    def __init__(self, dictObject={}, default=None):
        self.dictObject = dictObject
        self.defaultValue= default
    def __getattr__(self, name):
        if self.dictObject.has_key(name):
            return self.dictObject[name]
        else:
            return self.defaultValue
    def __setattr__(self, name, value):
        if(name!='dictObject' and name!='defaultValue'):
            self.dictObject[name] = value
        else:
            self.__dict__[name]=value
    def get(self, name , default=None):
        if self.dictObject.has_key(name):
            return self.dictObject[name]
        else:
            return default

class RequestDictMixin(DictMixin):
    """Represents a Web request in a form of dict like object
        This is situable for ExpandoObject instantiation
        Example: 
        
          >>r = ExpandoObject(RequestDictMixin(request))
          >>r.name #instead of request.get('name')
        It is used in the HalRequestHandler class as the params parameter:
          
          >>self.params.name
    """
    def __init__(self, request):
        self.request = request
        self.error_msg = "Request parameters are read only"
    def __getitem__(self, key):
        return self.request.get(key)
    def __setitem__(self, key, item):
        raise NotSuportedException(self.error_msg)
    def __delitem__(self, key):
        raise NotSuportedException(self.error_msg)
    def keys(self):
        raise NotImplementedError()

class LazyDict(DictMixin):
    """
    Gives dict-like object which values are lazy loaded(only when accessed)
    it uses the init_method patameter to setup the the value when it is first accessed
    Example:
      
      >>>d = LazyDict({'p1':'packages.module.className', 'p2':'packages.module.className2'}, 'init', some, init , parameters='test')
      >>>d['p1'] #returns a classname instance initialized with the class provided by calling the clasName.init(some, init, parameters='test')
    Note: all of the classes added in the dictionary should implement the method, otherwise exception is thrown.
    Usage: 
      
      It is convinient for constructing dynamic objects with the ExpandoObject like:
      
          >>>d = ExpandoObject(d)
          >>>d.p1 #or
          >>>d.p2.someInstanceProperty
    """
    def __init__(self, types, init_method, *args, **kwargs):
        self.objects = {}
        self.init_method = ''
        self.args = args
        self.kwargs = kwargs
        for k in types:
            self.objects[k[0]] = [ClassImport(k[1]), None]
    def __getitem__(self, key):
        if not self.objects[key]:
            raise Exception("Invalid Property "+key)
        elif not self.objects[key][1]:
            self.objects[key][1] = self.objects[key][0]()
            if hasattr(self.objects[key][1],  self.init_method):
                getattr(self.objects[key][1], self.init_method)(self.objects[key][1], *self.args, **self.kwargs)
        return self.objects[key][1]
    def __setitem__(self, key, item):
        self.objects[key] = (item.__class__, item)
    def __delitem__(self, key):
        del self.objects[key]
    def keys(self):
        return self.objects.keys()
    