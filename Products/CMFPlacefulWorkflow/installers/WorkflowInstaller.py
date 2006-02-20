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
# *****************************************************************
# ** (Un)installation of a workflow, the workflow must have been **
# ** created with DCWorkflowDump                                 **
# *****************************************************************
#
# Get and install DCWorkflowDump from
# http://sourceforge.net/projects/collective
#
# Create the workflow installation script (called 'my_workflow.py') in your
# Product's 'Extensions' folder.
#
# Go to the ZMI "dump" tab of "my_workflow", click [Dump it!], and copy/paste
# in
# 'my_workflow.py' the generated script.
#
#     ...
#     wi = WorkflowInstaller('my_workflow', 'Document')
#
# WARNING: The new types MUST be installed prior installing the related
# workflow,
# if your new types are in the types argument.
#

__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from Products.ExternalMethod.ExternalMethod import ExternalMethod

from utils import *

__all__ = ('WorkflowInstaller',)

class WorkflowInstaller(InstallerBase):

    _installerTitle = "workflow in portal workflow"

    defaultWorkflow = False


    def __init__(self, workflow_name, portal_types, **kw):
        """
        Constructor
        @param workflow_name: should start with a lowercase
        @param portal_types: (sequence of) portal types (names) associated with this workflow
        @param kw: override defaults like stop_on_error attribute or defaultWorkflow
        """
        self.workflow_name = workflow_name
        if type(portal_types) == type(''):
            portal_types = [portal_types]
        self.portal_types = tuple(portal_types)
        
        for k, v in kw.items():
            setattr(self, k, v)
        
        module_name = getattr(self, 'module_name', None)
        if module_name is None:
            self.module_name = self.workflow_name
        function_name = getattr(self, 'function_name', None)
        if function_name is None:
            self.function_name = 'create' + self.workflow_name.capitalize()
        old_workflow = getattr(self, 'old_workflow', None)
        if old_workflow is None:
            self.old_workflow = 'plone_workflow'

        return


    def doInstall(self, context):
        """Adds the workflow and associates (existing) portal types
        @param context: InstallationContext object
        """
        if self.workflow_name not in context.portal_workflow.objectIds():
            installFunction = ExternalMethod('temp', 'temp',
                                             context.productName() + '.' + self.module_name,
                                             self.function_name)
            workflow = installFunction(self.workflow_name)
            context.portal_workflow._setObject(self.workflow_name, workflow)
            context.portal_workflow.setChainForPortalTypes(self.portal_types, self.workflow_name)
            context.logInfo("Workflow '%s' installed" % self.workflow_name)
            if self.defaultWorkflow:
                context.portal_workflow.setDefaultChain(self.workflow_name)
        else:
            context.logWarning("Workflow '%s' already installed, skipped" % self.workflow_name)
        return


    def doUninstall(self, context):
        """
        @param context: InstallationContext object
        """
        context.logInfo("Uninstall of '%s' workflow is already performed by CMFQuickInstaller" %
                        self.workflow_name)

        if not self.defaultWorkflow:
            context.portal_workflow.setChainForPortalTypes(self.portal_types, self.old_workflow)
            context.logInfo("Associated types are now associated with %s workflow" % self.old_workflow)
        else:
            context.portal_workflow.setChainForPortalTypes(self.portal_types, '(Default)')
            context.portal_workflow.setDefaultChain(self.old_workflow)
            context.logInfo("Associated types are now associated with default workflow")
        return
