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

import string
from cStringIO import StringIO

from Acquisition import aq_base
from zope.component import getUtility, getSiteManager

from Products.CMFCore.interfaces import ISkinsTool
from Products.CMFCore.DirectoryView import addDirectoryViews

from Products.CMFPlone.interfaces import IControlPanel

from Products.CMFPlacefulWorkflow import install_globals
from Products.CMFPlacefulWorkflow.global_symbols import placeful_prefs_configlet
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import addPlacefulWorkflowTool
from Products.CMFPlacefulWorkflow.interfaces import IPlacefulWorkflowTool

skin_name = 'CMFPlacefulWorkflow'

def setupTools(self):
    tool = 'Placeful Workflow Tool'
    id = "portal_placeful_workflow"
    found = False
    for obj in self.objectValues():
        if obj.getId() == id:
            if obj.meta_type == tool:
                found = True
            else:
                raise NameError, "The tool id is already taken"

    if not found:
        addPlacefulWorkflowTool(self)

    tool = aq_base(self[id])
    getSiteManager(self).registerUtility(tool, IPlacefulWorkflowTool)

def installSubSkin(self, skinFolder, out):
    """ Install a subskin, i.e. a folder/directoryview.
    """
    skins_tool = getUtility(ISkinsTool)
    addDirectoryViews(skins_tool, 'skins', install_globals)
    for skin in skins_tool.getSkinSelections():
        path = skins_tool.getSkinPath(skin)
        path = map( string.strip, string.split( path,',' ) )
        if not skinFolder in path:
            try:
                path.insert( path.index( 'custom')+1, skinFolder )
            except ValueError:
                path.append(skinFolder)
            path = string.join( path, ', ' )
            skins_tool.addSkinSelection( skin, path )
            out.write('*** Subskin installed into %s.\n' % skin) 
        else:
            out.write('*** Subskin was already installed into %s.\n' % skin) 

def install(self, out=None):
    if out is None:
        out = StringIO()

    setupTools(self)
    installSubSkin(self, skin_name, out)

    # Install configlet
    cptool = getUtility(IControlPanel)
    try:
        cptool.unregisterConfiglet(placeful_prefs_configlet['id'])
    except:
        pass
    try:
        cptool.registerConfiglet(**placeful_prefs_configlet)
    except:
        pass
    return out.getvalue()


def uninstall(self, out=None):
    if out is None:
        out = StringIO()

    getSiteManager(self).unregisterUtility(self['portal_placeful_workflow'], IPlacefulWorkflowTool)
    # uninstall configlets
    try:
        cptool = getUtility(IControlPanel)
        cptool.unregisterConfiglet(placeful_prefs_configlet['id'])
        out.write('Removing CMFPlacefulWorkflow Configlet')
    except:
        out.write('Failed to remove CMFPlacefulWorkflow Configlet')

    return out.getvalue()
