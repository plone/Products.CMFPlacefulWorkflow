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
# *************************************************
# ** (Un)installation of a set of new skin layer **
# ** (FS directory) in the skins tool            **
# *************************************************
#
# Examples:
#     ...
#     # Defaults may work for 99% of Products
#     sli = SkinLayersInstaller()
#     ...
#     # Strange way to do it...
#     sli = SkinLayersInstaller(layers_dir='altskins', marker='portal_prefs')
#     ...
#

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

import os

from Globals import package_home

from Products.CMFCore.DirectoryView import addDirectoryViews

from utils import *

__all__ = ('SkinLayersInstaller',)

class SkinLayersInstaller(InstallerBase):

    _installerTitle = "layer(s) in portal skins"


    def __init__(self, layers_dir='skins', marker='custom', **kw):
        """Constructor
        @param layers_dir: subdirectory of the Product that contains the layers
        @param marker: the name of the (preferably) standard layer after which the new layer(s) are inserted
        @param kw: override defaults like stop_on_error attribute
        """
        self.layers_dir = layers_dir
        self.marker = marker
        for k, v in kw.items():
            setattr(self, k, v)
        return


    def doInstall(self, context):
        """Process installation of new layers
        @param context: InstallationContext object
        """
        # Get the list of installed layers
        before_layers = context.portal_skins.objectIds()

        # Process installation
        addDirectoryViews(context.portal_skins, self.layers_dir, context.product_globals)

        # Register in the skins selection
        after_layers = context.portal_skins.objectIds()
        new_layers = [l for l in after_layers if not l in before_layers]

        # FIXME: find something to reorder the various layers...
        for skin_name in context.portal_skins.getSkinSelections():
            path = [l.strip() for l in context.portal_skins.getSkinPath(skin_name).split(',')]
            for new_layer in new_layers:
                if new_layer not in path:
                    try:
                        path.insert(path.index(self.marker) + 1, new_layer)
                        context.logInfo("Added '%s' layer after '%s' in '%s' skin" %
                                        (new_layer, self.marker, skin_name))
                    except ValueError, e:
                        path.append(new_layer)
                        context.logWarning("Appended '%s' layer to '%s' skin (layer '%s' not found)" %
                                           (new_layer, skin_name, self.marker))
                else:
                    context.logWarning("Layer '%s' already in '%s' skin, skipped" %
                                       (new_layer, skin_name))
                # /if ...
            # /for ...
            path = ', '.join(path)
            context.portal_skins.addSkinSelection(skin_name, path)
        # /for ...
        return


    def doUninstall(self, context):
        """Remove layers form skins
        @param context: InstallationContext object
        """
        skinsDir = os.path.join(package_home(context.product_globals), self.layers_dir)
        new_layers = [d for d in os.listdir(skinsDir)
                     if ((os.path.isdir(os.path.join(skinsDir, d)))
                         and
                         (d not in ('CVS',)))]
        context.logInfo("Layers %s already removed by CMFQuickInstaller" %
                        ', '.join(["'" + n + "'" for n in new_layers]))
        for skin_name in context.portal_skins.getSkinSelections():
            path = [l.strip() for l in context.portal_skins.getSkinPath(skin_name).split(',')]
            for new_layer in new_layers:
                if new_layer in path:
                    path.remove(new_layer)
                    context.logInfo("Removed '%s' layer from '%s' skin" %
                                    (new_layer, skin_name))
                else:
                    context.logWarning("Didn't find '%s' layer in '%s' skin, skipped" %
                                    (new_layer, skin_name))
                # /if ...
            # /for ...
            path = ', '.join(path)
            context.portal_skins.addSkinSelection(skin_name, path)
        # /for ...
        return
