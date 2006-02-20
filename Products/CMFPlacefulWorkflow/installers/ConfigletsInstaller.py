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
#
# ***********************************************************
# ** (Un)installs the configlets for the portal config PMI **
# ***********************************************************
#
# Example:
#
#     ...
#     # Shortest possible
#     myConfiglet1 = {
#         'id': 'my_configlet',
#         'name': "Configure the features of my product",
#         'action': 'string:${portal_url}/prefs_my_product_form1'}
#     ci1 = ConfigletsInstaller(myConfiglet1)
#
#     # Several configlets
#     myConfiglets2 = (
#         {'id': 'my_configlet2',
#          'name': "Configure second group of features of my product",
#          'action': 'string:${portal_url}/prefs_my_product_form2',
#          'condition': "python: user.has_role('Manager')"},
#         {'id': 'my_configlet3',
#          'name': "Configure third group of features of my product",
#          'action': 'string:${portal_url}/prefs_my_product_form3',
#          'condition': "python: foo == bar",
#          'imageUrl': 'someIcon.gif'}
#         )
#     ci2 = ConfigletsInstaller(myConfiglets2)
#     ...
#

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from Products.CMFCore.CMFCorePermissions import ManagePortal

from utils import *

__all__ = ('ConfigletsInstaller',)

class ConfigletsInstaller(InstallerBase):

    _installerTitle = "configlet in portal configuration"


    def __init__(self, configlets, **kw):
        """Constructor
        @param configlet: (sequence of) mappings with keys:
            o * id: the id of the configlet
            o * name: a label for your configlet
            o * action: TALES expression
            o condition: TALES expression (default: empty expression)
            o permission: defaults to ManagePortal
            o category: defaults to 'Products'
            o visible: default is 1 (visible)
            o appId: defaults is the product's name
            o imageUrl: defaults ton None (no image)
            o description: defaults to empty string
            keys starting with '*' are mandatory

        @param kw: override defaults like stop_on_error attribute
        """
        if type(configlets) == type({}):
            configlets = [configlets]
        self.configlets = tuple(configlets)
        for k, v in kw.items():
            setattr(self, k, v)
        return


    def doInstall(self, context):
        """Adds configlets to the portal configuration utility
        """
        # building the default values for not provided keys
        defaults = {
            'permission': ManagePortal,
            'category': 'Products',
            'appId': context.productName()}
        for configlet in self.configlets:
            for k, v in defaults.items():
                if not configlet.has_key(k):
                    configlet[k] = v
            # FIXME: should check existing configlets first!
            try:
                context.portal_controlpanel.registerConfiglet(**configlet)
            except:
                pass
            context.logInfo("Added configlet '%s' to portal control panel" %
                            configlet['name'])
        return


    def doUninstall(self, context):
        """Uninstall of configlets is not supported by CMFQuickInstaller
        @param context: an InstallationContext object
        """
        for configlet in self.configlets:
            # FIXME: should check existing configlets and log problems
            try:
                context.portal_controlpanel.unregisterConfiglet(configlet['id'])
            except:
                pass
            context.logInfo("Removed configlet '%s' from portal control panel" %
                            configlet['name'])
        return
