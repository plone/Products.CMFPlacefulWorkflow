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
Patch for Plone workflow tool getChainFor method
"""
__version__ = "$Revision$"
# $Source: /cvsroot/ingeniweb/CMFPlacefulWorkflow/patches/workflowtoolPatch.py,v $
# $Id$
__docformat__ = 'restructuredtext'

from Products.CMFPlone.WorkflowTool import WorkflowTool
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Acquisition import aq_base, aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr

def getChainFor(self, ob):
    """
    monkey-patched by CMFPlacefulWorkflow to look for placeful workflow
    configurations.
    """
    cbt = self._chains_by_type

    if type(ob) == type(''):
        portal_type = ob
    elif hasattr(aq_base(ob), '_getPortalTypeName'):
        portal_type = ob._getPortalTypeName()
    else:
        portal_type = None

    if portal_type is None:
        return ()

    # Take some extra care when ob is a string
    is_policy_container=0
    objectids=[]
    try:
       objectids = ob.objectIds()
    except AttributeError, TypeError:
       pass
    if WorkflowPolicyConfig_id in objectids:
        is_policy_container=1

    if type(ob) != type('') and portal_type != None and not is_policy_container:
        # Inspired by implementation in CPSWorkflowTool.py of CPSCore 3.9.0
        # Workflow needs to be determined by true containment not context
        # so we loop over the actual containers
        wfpolicyconfig = None
        current_ob = aq_inner(ob)
        portal = aq_base(getToolByName(self, 'portal_url').getPortalObject())
        while wfpolicyconfig is None and current_ob is not None:
            if base_hasattr(current_ob, WorkflowPolicyConfig_id):
                wfpolicyconfig = getattr(current_ob, WorkflowPolicyConfig_id)
            elif aq_base(current_ob) is portal:
                break
            current_ob = aq_inner(aq_parent(current_ob))

        if wfpolicyconfig is not None:
            # Was it here or did we acquire?
            start_here = base_hasattr(aq_parent(aq_inner(ob)), WorkflowPolicyConfig_id)
            chain = wfpolicyconfig.getPlacefulChainFor(portal_type, start_here=start_here)
            if chain is not None:
                return chain

    chain = None
    if cbt is not None:
        chain = cbt.get(portal_type, None)
        # Note that if chain is not in cbt or has a value of
        # None, we use a default chain.
    if chain is None:
        chain = self.getDefaultChainFor(ob)
        if chain is None:
            return ()
    return chain

# don't lose the docstrings
getChainFor.__doc__ = '\n'.join((WorkflowTool.getChainFor.__doc__, getChainFor.__doc__))
WorkflowTool.getChainFor = getChainFor
