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
# ******************************************
# ** (Un)installation of a Plone/CMF tool **
# ******************************************
#
# Example:
#
#     ...
#     from Products.MyProduct.MyTool import MyTool
#     ti = ToolInstaller(MyTool)
#     ...
#

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from Products.CMFCore.ActionProviderBase import ActionProviderBase

from utils import *

__all__ = ('ToolInstaller',)

class ToolInstaller(InstallerQISupportBase):

    _installerTitle = "tool in portal"


    def __init__(self, tool_class, **kw):
        """Constructor
        @param tool_class: class definition of the tool.
            Assumes that class provides 'title' and 'meta_type' attributes.
        @param kw: override defaults like stop_on_error attribute
        """
        self.tool_class = tool_class
        for k, v in kw.items():
            setattr(self, k, v)
        return


    def doInstall(self, context):
        """Registers the types in portal_types
        @param context: InstallationContext object
        """
        addTool = context.portal.manage_addProduct[context.productName()].manage_addTool
        if not context.portal.objectIds(spec=self.tool_class.meta_type):
            addTool(self.tool_class.meta_type, None)
            context.logInfo("'%s' tool installed" % self.tool_class.title)
            # Tool may be an actions provider
            if issubclass(self.tool_class, ActionProviderBase):
                context.portal_actions.addActionProvider(self.tool_class.id)
                context.logInfo("'%s' tool is a new actions provider" % self.tool_class.title)

        else:
            context.logWarning("'%s' already installed, skipped" % self.tool_class.title)
        return
