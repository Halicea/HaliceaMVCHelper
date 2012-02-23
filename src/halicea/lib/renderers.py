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
#along with this program.  If not, see <http://www.gnu.org/licenses/>.from django import template

from django.template.loader import *
class HalTemplate(object):
    def __init__(self, text):
        self.text = text
    def render(self, context):
        raise NotImplementedError('This class needs to be inherited')

class Django(HalTemplate):
    def __init__(self, text):
        HalTemplate.__init__(self, text)
        self.template = template.Template(text)
    def render(self, dict):
        return self.template.render(template.Context(dict))

