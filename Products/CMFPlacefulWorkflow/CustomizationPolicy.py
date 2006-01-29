# -*- coding: utf-8 -*-
## CMFPlacefulWorkflow
## A CMF/Plone product for locally changing the workflow of content types
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
"""
Simple customization policy
"""
__version__ = "$Revision$"
# $Source: /cvsroot/ingeniweb/CMFPlacefulWorkflow/CustomizationPolicy.py,v $
# $Id$
__docformat__ = 'restructuredtext'


from Products.CMFPlone import Portal
from Products.CMFPlone.CustomizationPolicy import ICustomizationPolicy
from Products.CMFCore.utils import getToolByName
from Products.CMFPlacefulWorkflow.global_symbols import placeful_prefs_configlet, PROJECTNAME
# Check for Plone 2.1
try:
    from Products.CMFPlone.migrations import v2_1
except ImportError:
    from Products.ATContentTypes.customizationpolicy import ATCTSitePolicy as CustomizationPolicy
else:
    from Products.Archetypes.customizationpolicy import ArchetypesSitePolicy as CustomizationPolicy

def register(context, app_state):
    Portal.addPolicy(PROJECTNAME+' Site', PWCustomizationPolicy())

class PWCustomizationPolicy(CustomizationPolicy):
    """ PlacefulWorkflow customization policy """
    __implements__ = ICustomizationPolicy

    availableAtConstruction = True

    def customize(self, portal):
        ATCTSitePolicy.customize(self, portal)

        # install Product
        installer = portal.portal_quickinstaller
        installer.installProducts([PROJECTNAME], stoponerror=True)

