# -*- coding: utf-8 -*-
import itertools
import os
import plistlib
import unicodedata
import sys

from xml.etree.ElementTree import Element, SubElement, tostring

"""
You should run your script via /bin/bash with all escape options ticked.
The command line should be

python yourscript.py "{query}" arg2 arg3 ...
"""
UNESCAPE_CHARACTERS = u""" ;()"""

_MAX_RESULTS_DEFAULT = 9

# preferences = plistlib.readPlist('info.plist')
bundleid = 'com.michaelwaterfall.datetime-format-converter'

class Item(object):
    @classmethod
    def unicode(cls, value):
        try:
            items = value.iteritems()
        except AttributeError:
            return value
        else:
            return dict(item for item in items)

    def __init__(self, attributes, title, subtitle, icon=None):
        self.attributes = attributes
        self.title = title
        self.subtitle = subtitle
        self.icon = icon

    def __str__(self):
        return tostring(self.xml(), encoding='utf-8')

    def xml(self):
        item = Element(u'item', self.unicode(self.attributes))
        for attribute in (u'title', u'subtitle', u'icon'):
            value = getattr(self, attribute)
            if value is None:
                continue
            try:
                (value, attributes) = value
            except:
                attributes = {}
            SubElement(item, attribute, self.unicode(attributes)).text = str(value)
        return item

def args(characters=None):
    return tuple(unescape(decode(arg), characters) for arg in sys.argv[1:])

def config():
    return _create('config')

def decode(s):
    return unicodedata.normalize('NFC', s)

def uid(uid):
    return '{}-{}'.format(bundleid, uid)

def unescape(query, characters=None):
    for character in (UNESCAPE_CHARACTERS if (characters is None) else characters):
        query = query.replace('\\%s' % character, character)
    return query

def work(volatile):
    path = {
        True: '~/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data',
        False: '~/Library/Application Support/Alfred 2/Workflow Data'
    }[bool(volatile)]
    return _create(os.path.join(os.path.expanduser(path), bundleid))

def write(text):
    sys.stdout.write(str(text, 'utf-8'))

def xml(items, maxresults=_MAX_RESULTS_DEFAULT):
    root = Element('items')
    for item in itertools.islice(items, maxresults):
        root.append(item.xml())
    return tostring(root, encoding='utf-8')

def _create(path):
    if not os.path.isdir(path):
        os.mkdir(path)
    if not os.access(path, os.W_OK):
        raise IOError('No write access: %s' % path)
    return path
