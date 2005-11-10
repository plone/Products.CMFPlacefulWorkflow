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

def getChainFor(self, ob):
    """
    monkey-patched by CMFPlacefulWorkflow to look for placeful workflow
    configurations.
    """
    cbt = self._chains_by_type

    if type(ob) == type(''):
        pt = ob
    elif hasattr(aq_base(ob), '_getPortalTypeName'):
        pt = ob._getPortalTypeName()
    else:
        pt = None

    if pt is None:
        return ()

    if type(ob) != type('') and pt!=None:
        # Inspired by implementation in CPSWorkflowTool.py of CPSCore 3.9.0
        wfpolicyconfig = getattr(ob, WorkflowPolicyConfig_id, None)
        if wfpolicyconfig is not None:
            # Was it here or did we acquire?
            start_here = hasattr(aq_base(aq_parent(aq_inner(ob))), WorkflowPolicyConfig_id)
            chain = wfpolicyconfig.getPlacefulChainFor(pt, start_here=start_here)
            if chain is not None:
                return chain

    chain = None
    if cbt is not None:
        chain = cbt.get(pt, None)
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
