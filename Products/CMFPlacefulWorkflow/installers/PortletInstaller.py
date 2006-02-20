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
# ***************************************************************
# ** (Un)installer for portlets in the slots of the plone root **
# ***************************************************************
#
# Example:
#
#     ...
#     # Your left portlet
#     pi1 = PortletInstaller('here/myportlet/macros/portlet')
#     # Your right portlets
#     pi2 = PortletInstaller(('here/fooportlet/macros/portlet',
#                             'here/barportlet/macros/portlet'),
#                             slot_prop_name='right_slots')
#     ...
#

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from utils import *

__all__ = ('PortletInstaller',)

class PortletInstaller(InstallerBase):

    _installerTitle = "portlet(s) in portal"


    def __init__(self, portlet_path, slot_prop_name='left_slots', **kw):
        """Constructor
        @param portlet_path: (sequence of) path expression(s) to the portlet macro(s).
        @type portlet_path: string or sequence of strings
        @param slot_prop_name: name of the slots property
        @param kw: override defaults like stop_on_error attribute
        """
        if type(portlet_path) == type(''):
            portlet_path = [portlet_path]
        self.paths = tuple(portlet_path)
        self.slot_prop_name = slot_prop_name
        for k, v in kw.items():
            setattr(self, k, v)
        return


    def doInstall(self, context):
        """Append new portlets to the portal root if required
        @param context: an InstallationContext object
        """
        portlets = list(context.portal.getProperty(self.slot_prop_name))
        for portlet in self.paths:
            if portlet not in portlets:
                portlets.append(portlet)
                context.logInfo("Portlet '%s' installed in '%s'." % (portlet, self.slot_prop_name))
            else:
                context.logWarning("portlet '%s' is already in '%s', skipped" % (portlet, self.slot_prop_name))
        context.portal.manage_changeProperties({self.slot_prop_name: portlets})
        return


    def doUninstall(self, context):
        """Removes portlets
        @param context: InstallationContext object
        """
        portlets = list(context.portal.getProperty(self.slot_prop_name))
        for portlet in self.paths:
            try:
                portlets.remove(portlet)
                context.logInfo("Portlet '%s' removed from '%s'." % (portlet, self.slot_prop_name))
            except ValueError, e:
                context.logWarning("portlet '%s' is not in '%s', skipped" % (portlet, self.slot_prop_name))
        context.portal.manage_changeProperties({self.slot_prop_name: portlets})
        return
