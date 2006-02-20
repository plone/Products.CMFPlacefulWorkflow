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
# *********************************************************
# ** (Un)installs a new role with associated permissions **
# *********************************************************
#
# Examples:
#
# # New role with only 'View' permission
# ri = RoleInstaller('SomeRole', allowed='View')
#
# # New role based on Member plus one permission
# ri = RoleInstaller('SomeRole', model='Member',
#                    allowed='Some permission')
# # New role based on Reviewer that cannot review portal content :)
# ri = RoleInstaller('SomeRole', model='Reviewer',
#                    denied='Review portal content')
#

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from Products.ExternalMethod.ExternalMethod import ExternalMethod
from AccessControl.Role import RoleManager

from utils import *

__all__ = ('RoleInstaller',)

class RoleInstaller(InstallerBase):
    """Role installation handling with associated permissions"""

    _installerTitle = "role in portal security matrix"


    def __init__(self, role, model='Anonymous', allowed=(), denied=(), **kw):
        """Constructor
        @param role: name of the new role
        @param model: new role has the same permissions granted as 'model' role
        @param allowed: sequence of allowed permissions
        @param denied: sequence of denied permissions
        @param kw: override defaults like stop_on_error attribute
        """
        self.role = role
        self.model = model
        if type(allowed) == type(''):
            allowed = (allowed,)
        self.allowed = list(allowed)
        if type(denied) == type(''):
            denied = (denied,)
        self.denied = list(denied)
        for k, v in kw.items():
            setattr(self, k, v)
        return


    def doInstall(self, context):
        """Creates the new role
        @param context: an InstallationContext object
        """
        context.portal._addRole(self.role)
        context.logInfo("Added role '%s'" % self.role)
        if self.model:
            permissions = self._currentPermissions(context, self.model)
            context.portal.manage_role(self.role, permissions=permissions)
            context.logInfo("Give permissions of '%s' to '%s'" %
                            (self.model, self.role))
        if self.allowed:
            context.portal.manage_role(self.role, permissions=self.allowed)
            context.logInfo("Allowed permissions %s to '%s'" %
                            (', '.join(["'" + p + "'" for p in self.allowed]),
                             self.role))
        if self.denied:
            permissions = self._currentPermissions(context, self.role)
            for p in self.denied:
                permissions.remove(p)
            context.portal.manage_role(self.role, permissions=permissions)
            context.logInfo("Denied permissions %s to '%s'" %
                            (', '.join(["'" + p + "'" for p in self.denied]),
                             self.role))
        return


    def doUninstall(self, context):
        """Removes this role
        @param context: InstallationContext object
        """
        context.portal._delRoles([self.role])
        context.logInfo("Removed role '%s'" % self.role)
        return


    def _currentPermissions(self, context, role):
        """List of permissions granted to role"""
        return [p['name'] for p in context.portal.permissionsOfRole(role)
                if p['selected'] == 'SELECTED']
