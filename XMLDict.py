#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011 Dave Eddy <dave@daveeddy.com>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# XMLDict.py
# XMLDict class used to convert a dictionary into an XML string
#
# Author
#  Dave Eddy <dave@daveeddy.com>
#  http://www.daveeddy.com
#

# Modified by Matt Gabrenya, matt@gabrenya.com / matt.gabrenya.com -- 2/24/12
 
from xml.dom.minidom import parse, parseString
from xml.sax import saxutils 
import re


# Convenience Functions
def convert_dict_to_xml(d):
    """Convenience Function: This creates an XMLDict object, and returns the XML string"""
    a   = XMLDict(d)
    xml = a.get_xml()
    return xml
 
def prettify(xml):
    """Convenience Function: This returns a pretty version of the XML"""
    return parseString(xml).toprettyxml()
 
class XMLDict:
    """Class used to convert a python dictionary to XML"""
    def __init__(self, d):
        """Create the XML and store it"""
        self.d = d
        self.xml = self._convert_dict_to_xml(self.d)
 
    def get_xml(self):
        """Returns the XML"""
        return self.xml
 
    def get_pretty_xml(self):
        """Returns the pretty XML"""
        return parseString(self.xml).toprettyxml()
 
    def _convert_dict_to_xml(self, d):
        """Converts a dictionary to XML"""
        xml = ''
        for k,v in d.iteritems(): # iterate through the dictionary
            if str(type(v)).find('dict') != -1: # the value is a dictionary
                xml += "<%s>" % (k)
                xml += self._convert_dict_to_xml(v) # recursively call itself
                xml += "</%s>" % (k)
            else: #value is not a dictionary
                if str(type(v)).find('list') == -1:
                    v = [v]
		xml += "<%s>" %(k)
                for value in v:
                    if str(type(value)).find('dict') != -1:
                        xml += self._convert_dict_to_xml(value) # recursively call itself
	            else:
                        #xml += "<%s>%s</%s>" % (unicode(k),saxutils.escape(unicode(value)),unicode(k))
 			xml += "%s" %(saxutils.escape(unicode(value)))
		xml += "</%s>" %(k)  

	# from http://boodebr.org/main/python/all-about-python-and-unicode#UNI_XML
	RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
        	u'|' + \
		u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
		(unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
		unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
		unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff))
	xml = re.sub(RE_XML_ILLEGAL, "*?*", xml)
        return xml
	
