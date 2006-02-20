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
# **************************************************
# ** (Un)installs actions in any action provider. **
# **************************************************
#
# 'actions' is a simple action mapping or a sequence of actions mappings
# 'portal_actions' is the default action provider but you may add your custom
# actions to any other one.
#
#
# Example:
#     myaction = {
#         'id': 'myaction',
#         'name': 'My action',
#         'action': '$portal_url/some_action',
#         'permission': CMFCorePermissions.View,
#         'category': 'object'
#         }
#     ai1 = ActionsInstaller(myactions)
#
#     myactions = (
#         {'id': 'myaction',
#          'name': 'My action',
#          'action': '$portal_url/some_action',
#          'permission': CMFCorePermissions.View,
#          'category': 'object'
#         },
#         {'id': 'otheraction',
#          'name': 'Another action'
#          'action': '$portal_url/another_action',
#          'permission': CMFCorePermissions.View,
#          'category': 'object'
#          })
#     ai2 = ActionsInstaller(myactions, actions_provider='portal_types')
__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from utils import *

__all__ = ('ActionsInstaller',)

class ActionsInstaller(InstallerBase):

    _installerTitle = "action(s) in portal"


    def __init__(self, actions, actions_provider='portal_actions', **kw):
        """Constructor
        @param actions: a sequence of action defintions, each one being a mapping with keys:
            o * id: <string>,
            o * name: <string>,
            o * action: <TAL expression as string>,
            o condition: TAL expression as string (default empty string)
            o permission: string or imported permission (default: 'View')
            o * category: <string>,
            o visible: 1 or 0 (default: 1)
            keys starting with * are mandatory
            See class Products.CMFCore.ActionProviderBase.ActionProviderBase for more infos.
        @param actions_provider: the id of a Plone action provider tool
        @param kw: override defaults like stop_on_error attribute
        """
        if type(actions) == type({}):
            actions = [actions]
        self.actions = tuple(actions)

        self.actions_provider = actions_provider
        for k, v in kw.items():
            setattr(self, k, v)
        return


    def doInstall(self, context):
        """Sets the actions
        @param context: InstallationContext object
        """
        # FIXME: what is the rule for avoiding conflicts when adding actions ?
        # Do we have to do a lookup on all action providers or only that one ?
        defaults = {
            'permission': 'View',
            'condition': '',
            'visible': 1}
        provider = getattr(context.portal, self.actions_provider, None)
        if provider:
            for action in self.actions:
                for k, v in defaults.items():
                    if not action.has_key(k):
                        action[k] = v
                action_exists = 0
                for existing_action in provider.listActions():
                    if existing_action.id==action['id']:
                        action_exists = 1
                if action_exists:
                    pass # Action exists already, do nothing
                else:
                    provider.addAction(**action)
                context.logInfo("Action '%s' added to '%s' action provider" % (action['id'], self.actions_provider))
        else:
            context.logInfo("ActionProvider %s not found. Can't install actions." % self.actions_provider)

        return


    def doUninstall(self, context):
        """Remove the actions
        @param context: InstallationContext object
        """
        # FIXME: it seems that the ActionProviderBase enables id + name duplicates :(
        # thus "removing" an action may remove another one but checking bot id + name
        # would reduce the risk of mismatch.
        provider = getattr(context.portal, self.actions_provider, None)
        if provider:
            installedActions = [(a.id, a.title) for a in provider.listActions()]
            newActions = [(a['id'], a['name']) for a in self.actions]
            selection = []
            for action in newActions:
                try:
                    index = installedActions.index(action)
                    selection.append(index)
                except ValueError, e:
                    # FIXME: log this? (warning)
                    pass
            selection = tuple(selection)
            provider.deleteActions(selections=selection)
            context.logInfo("Actions removed from '%s'" % self.actions_provider)
        else:
            context.logInfo("Action Provider %s not found" % self.actions_provider)

        # FIXME: log warning on actions not found if any
        return

