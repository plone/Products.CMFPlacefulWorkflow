# -*- coding: utf-8 -*-
## CMFPlacefulWorkflow
## Copyright (C)2005 Ingeniweb

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
"""
Product installation
"""
__version__ = "$Revision$"
# $Source: /cvsroot/ingeniweb/CMFPlacefulWorkflow/Extensions/Install.py,v $
# $Id$
__docformat__ = 'restructuredtext'

from Products.CMFPlacefulWorkflow import install_globals
from Products.CMFPlacefulWorkflow.global_symbols import *
from Products.CMFPlacefulWorkflow.Installation import Installation
from OFS.Cache import Cache
from Products.CMFCore.utils import getToolByName
from cStringIO import StringIO
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import addPlacefulWorkflowTool
import string
from Products.CMFCore.DirectoryView import addDirectoryViews

#perms_list = (PlacefulWorkflowPolicy_editPermission, )

skin_name = 'CMFPlacefulWorkflow'

def setupTools(self):
    tool = 'Placeful Workflow Tool'
    id = "portal_placeful_workflow"
    found=0
    for obj in self.objectValues():
        if obj.meta_type == tool:
            self.manage_delObjects([id, ])
    addPlacefulWorkflowTool(self)

def install(self):
    installation=Installation(self)
    addDirectoryViews(installation.skinsTool, 'skins', install_globals)
    installation.installSubSkin(skin_name)
#    installation.setPermissions(perms_list)
    setupTools(self)

    # Install configlet
    cptool = getToolByName(self, 'portal_controlpanel')
    try:
        cptool.unregisterConfiglet(placeful_prefs_configlet['id'])
    except:
        pass
    try:
        cptool.registerConfiglet(**placeful_prefs_configlet)
    except:
        pass
    return installation.report()

def uninstall(self):
    out = StringIO()
    
    # uninstall configlets
    try:
        cptool = getToolByName(self, 'portal_controlpanel')
        cptool.unregisterConfiglet(placeful_prefs_configlet['id'])
        out.write('Removing CMFPlacefulWorkflow Configlet')
    except:
        out.write('Failed to remove CMFPlacefulWorkflow Configlet')
        
    return out.getvalue()
