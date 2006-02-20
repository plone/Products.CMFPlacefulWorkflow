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

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

import os
from cStringIO import StringIO
from traceback import print_exc

import zLOG
from Globals import package_home

from Products.CMFCore.utils import getToolByName

__all__ = [
    'InstallationError', 'InstallationContext', 'InstallationRunner',
    'InstallerBase', 'InstallerQISupportBase'
    ]

#
# Exception raised if something fails
#

class InstallationError(Exception):
    pass

#
# *********************************************
# ** Provides information on Plone resources **
# ** and installation environment            **
# *********************************************
#
# Your install and uninstall functions must start with the creation of an
# InstallationContext object.
#
# Example:
#
# ...
# from Products.MyProduct import product_globals
# ...
# def install(self):
#     ic = InstallationContext(self, product_globals)
#     ...
#
class InstallationContext:
    """Provides the various information on the Plone on which the installation is
    performed (Plone version, installed products...)
    """

    def __init__(self, context, product_globals, verbose_report=True):
        """Constructor
        @param context: is the object passed to the external method
        @param product_globals: should be provided from your Produc's __init__.py
            like this: product_globals = globals()
        @param verbose_report: 1 = shows all progress, 0 = shows only errors and warnings
        """
        # Find the tools for quicker access later
        all_tool_names = (
            'portal_actions', 'portal_catalog', 'portal_controlpanel', 'portal_properties', 'portal_quickinstaller',
            'portal_skins', 'portal_types', 'portal_url', 'portal_workflow')

        for tool_name in all_tool_names:
            setattr(self, tool_name, getToolByName(context, tool_name))
        self.portal = self.portal_url.getPortalObject()
        self.report = StringIO()
        self.product_globals = product_globals
        self.verbose_report = verbose_report
        return


    def productName(self):
        """The directory name in Products dir
        """
        return os.path.basename(package_home(self.product_globals))


    def log(self, text, level=zLOG.INFO):
        """Shows what's happening
        @param text: to be printed
        @param level: type of log event (see zLOG)
        """
        self.report.write(text + '\n')
        zLOG.LOG('PloneInstallation', level, text)
        return


    def logInfo(self, text):
        """Logs a normal (success) message
        @param text: to be printed
        """
        if self.verbose_report:
            self.log('/i\\ ' + text)
        return


    def logWarning(self, text):
        """Logs something strange the user should be aware of
        @param text: to be printed
        """
        self.log('/?\\ ' + text, level=zLOG.WARNING)
        return


    def logError(self, text):
        """Logs not recoverable error (can't proceed more install)
        @param text: to be printed
        """
        self.log('/!\\ ' + text, level=zLOG.ERROR)
        raise InstallationError(text)
        return


    def logTitle(self, text):
        """Logs an emphasized text
        @param text: to be printed
        """
        l = len(text)
        underline = ('*' * (len(text) + 6)) + '\n'
        title = '** ' + text + ' **\n'
        self.report.write(underline)
        self.report.write(title)
        self.report.write(underline)
        zLOG.LOG('PloneInstallation', zLOG.INFO, text)
        return


    def requiresProduct(self, productName):
        """Finds if the Zope instance has this product available.
        Usefull for dependancies checking
        @param productName: name of Zope Product as appearing in the ZMI
        """
        root = self.portal.getPhysicalRoot()
        products = root.Control_Panel.Products
        if productName not in products.objectIds():
            self.logError("Product '%s' is required. Please check the documentation" % productName)
        return


    def requiresInstalledProduct(self, productName):
        """Finds if the Plone instance has this product available and installed.
        Usefull for dependancies checking.
        @param productName: name of Zope Product as appearing in the ZMI
        """
        if not self.portal_quickinstaller.isProductInstalled(productName):
            self.logError("You should install '%s' Product in this Plone instance first" % productName)
        return

#
# *******************************************************
# ** Executes and controls the execution of Installers **
# *******************************************************
#
# Example:
#     ...
#     runner = InstallationRunner(
#         TypeInstaller(...),
#         ToolInstaller(...),
#         ...)
#     ...
#     runner.addInstallers(
#         WrokflowInstaller(...),
#         ...)
#     ...
#

class InstallationRunner:
    """Handles the installers
    """


    def __init__(self, *installers):
        """Constructor
        @param *installers: objects built with subclasses of InstallerBase
        """
        self._checkInstallers(installers)
        self.installers = list(installers)
        return


    def addInstallers(self, *installers):
        """For making the installers programmaticaly rather than declaratively
        @param *installers: objects built with subclasses of InstallerBase
        """
        self._checkInstallers(installers)
        self.installers += installers
        return


    def install(self, context, auto_reorder=False, autoReorder=False):
        """Processes installation based on all xxInstaller objects
        @param context: InstallationContext object
        @param auto_reorder: need to reorder installers in a safe way
        @param autoReorder: backward compatibility
        """
        context.logTitle("Installing %s Product" % context.productName())
        if auto_reorder or autoReorder:
            self._reorder()
        for installer in self.installers:
            installer.install(context)
        return '<pre>\n' + context.report.getvalue() +'\n</pre>'


    def uninstall(self, context, auto_reorder=False, autoReorder=False):
        """Processes uninstallation based on all xxInstaller objects
        @param context: InstallationContext object
        @param auto_reorder: need to reorder installers in a safe way
        @param autoReorder: backward compatibility
        """
        context.logTitle("Uninstalling %s Product" % context.productName())
        if auto_reorder or autoReorder:
            self._reorder()
        self.installers.reverse()
        for installer in self.installers:
            installer.uninstall(context)
        return '<pre>\n' + context.report.getvalue() +'\n</pre>'


    def _reorder(self):
        """Reorders the installers in a safe way
        """
        best_class_order = (
            'TypeInstaller', 'ATTypesInstaller', 'ToolInstaller', 'SkinLayersInstaller',
            # __others__ is a marker for other installer classes which position doesnt care
            '__others__', 
            'SkinInstaller', 'WorkflowInstaller', 'ActionInstaller', 'ZexpInstaller'
            )
        installers_by_class = {}
        ordered_installers = []
        for installer in self.installers:
            class_name = installer.__class__.__name__
            if class_name not in best_class_order:
                class_name = '__others__'
            try:
                installers_by_class[class_name].append(installer)
            except KeyError, e:
                installers_by_class[class_name] = [installer]
        for class_name in best_class_order:
            ordered_installers += installers_by_class.get(class_name, [])
        self.installers = ordered_installers
        return


    def _checkInstallers(self, installers):
        """Checks the types of installers"""

        for installer in installers:
            if not issubclass(installer.__class__, InstallerBase):
                raise InstallationError("%s object is not an installer" %
                                        installer.__class__.__name__)
        return


#
# ***************************************
# ** The base class for all installers **
# ***************************************
#
# All subclasses must provide "doInstall" and "doUninstall" methods,
# otherwise: BANG !
#

class InstallerBase:
    """Base class for all installers
    """

    # Can be overriden by subclasses passing stop_on_error=1 in the constructor
    stop_on_error = True

    # *Must* be overriden by subclasses
    _installerTitle = '**undefined stuff**'


    def install(self, context):
        """Install controller
        @param context: InstallationContext object
        """
        context.logTitle("Installing " + self._installerTitle)
        try:
            self.doInstall(context)
        except:
            print_exc(None, context.report)
            if self.stop_on_error:
                raise
        return


    def doInstall(self, context):
        """Processes the installation (Defered to a subclass)
        @param context: InstallationContext object
        """
        raise NotImplementedError


    def uninstall(self, context):
        """Uninstall controller
        @param context: InstallationContext object
        """
        context.logTitle("Uninstalling " + self._installerTitle)
        try:
            self.doUninstall(context)
        except:
            print_exc(None, context.report)
            if self.stop_on_error:
                raise
        return


    def doUninstall(self, context):
        """Processes the installation (Defered to a subclass)
        @param context: InstallationContext object
        """
        raise NotImplementedError


#
# ************************************************************
# ** Use this base class for features correctly uninstalled **
# ** by the CMFQuickInstaller                               **
# ************************************************************
#

class InstallerQISupportBase(InstallerBase):
    """Base class for installers with uninstall supported by the CMFQuickInstaller
    """


    def doUninstall(self, context):
        """Just does nothing :)
        @param context: InstallationContext object
        """
        context.logInfo("Uninstall already performed by CMFQuickInstaller")
        return
