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
Product installation
"""
__version__ = "$Revision$"
# $Source: /cvsroot/ingeniweb/CMFPlacefulWorkflow/Extensions/Install.py,v $
# $Id$
__docformat__ = 'restructuredtext'

from Products.CMFPlacefulWorkflow.global_symbols import *

from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import PlacefulWorkflowTool
from Products.CMFPlacefulWorkflow.installers.utils import InstallationRunner, InstallationContext
from Products.CMFPlacefulWorkflow.installers.ToolInstaller import ToolInstaller
from Products.CMFPlacefulWorkflow.installers.SkinLayersInstaller import SkinLayersInstaller
from Products.CMFPlacefulWorkflow.installers.ConfigletsInstaller import ConfigletsInstaller

def getRunners():

    installers = []

    sti = ToolInstaller(PlacefulWorkflowTool)
    installers.append(sti)

    si = SkinLayersInstaller()
    installers.append(si)

    ci = ConfigletsInstaller(placeful_prefs_configlet)
    installers.append(ci)

    return InstallationRunner(*tuple(installers))

def install(self):

    # Always start with the creation of the InstallationContext
    ic = InstallationContext(self, GLOBALS)

    # Runs the installation and return the report
    report = getRunners().install(ic, auto_reorder=True)
    return report

def uninstall(self):

    # Always start with the creation of the InstallationContext
    ic = InstallationContext(self, GLOBALS)

    # Runs the uninstallation and return the report
    report = getRunners().uninstall(ic, auto_reorder=True)

    return report
