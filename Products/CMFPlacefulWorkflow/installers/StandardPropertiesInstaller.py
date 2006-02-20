# -*- coding: utf-8 -*-
## PloneSubscription
## A Plone tool supporting different levels of subscription and notification
## Copyright (C)2006 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

#
# $Id$
#
# *****************************************************************************
# ** Changes the value of properties from the Plone standard property sheets
# **
# *****************************************************************************
#
# Example:
#
#     ...
#     ntPropItems = (
#         ('batchSize', 40),
#         ('idsNotToList', ['secret', 'confidential']))
#     spi = StandardPropertiesInstaller('navtree_properties', propItems)
#     ...
#
# FIXME: There's no easy way to "unchange" what has been done here.
#

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from utils import *

__all__ = ('StandardPropertiesInstaller',)

class StandardPropertiesInstaller(InstallerBase):

    _installerTitle = "new values for standard properties"


    def __init__(self, sheetName, properties, **kw):
        """Constructor
        @param sheetName: the name as appearing in portal_properties
        @param properties: a sequence of (id, value, type) tuples
        @param kw: override defaults like stop_on_error attribute
        """
        self.sheetName = sheetName
        self.properties = properties
        for k, v in kw.items():
            setattr(self, k, v)
        return


    def doInstall(self, context):
        """Changes existing properties
        @param context: an InstallationContext object
        """
        propertySheet = getattr(context.portal_properties, self.sheetName)
        for property in self.properties:
            id = property[0]
            value = property[1]
            tipe = None
            
            if len(property) > 2:
                tipe = property[2]
            
            if propertySheet.hasProperty(id) or tipe is None:
                propertySheet._setPropValue(id, value)
            else:
                propertySheet._setProperty(id, value, tipe)
            
            context.logInfo("Property '%s' set to %s in property sheet '%s'" %
                            (id, str(value), self.sheetName))
        return


    def doUninstall(self, context):
        """Can't undo changes
        @param context: an InstallationContext object
        """
        propIds = ' ,'.join(["'" + p[0].strip() + "'" for p in self.properties])
        context.logWarning("Can't reset the previous property values for %s in '%s' property sheet" %
                           (propIds, self.sheetName))
        return
