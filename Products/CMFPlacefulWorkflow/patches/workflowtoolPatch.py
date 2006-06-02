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

from AccessControl import getSecurityManager
from Acquisition import aq_base, aq_parent, aq_inner

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr

from Products.CMFPlone.WorkflowTool import WorkflowTool
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id

def getChainFor(self, ob):
    """Monkey-patched by CMFPlacefulWorkflow to look for placeful workflow configurations.

    Goal: find a workflow chain in a policy

    Steps:
    1. ask the object if it contains a policy
    2. if it does, ask him for a chain
    3. if there's no chain for the type the we loop on the parent
    4. if the parent is the portal object or None we stop and we ask to portal_workflow

    Hint:
    If ob was a string, ask directly portal_worlfow\n\n"""

    cbt = self._chains_by_type

    if type(ob) == type(''):
        # We are not in an object, then we can only get default from portal_workflow
        portal_type = ob
        if cbt is not None:
            chain = cbt.get(portal_type, None)
            # Note that if chain is not in cbt or has a value of None, we use a default chain.
        if chain is None:
            chain = self.getDefaultChainFor(ob)
            if chain is None:
                # CMFCore default
                return ()

    elif hasattr(aq_base(ob), '_getPortalTypeName'):
        portal_type = ob._getPortalTypeName()
    else:
        portal_type = None

    if portal_type is None or ob is None:
        return ()

    # Take some extra care when ob is a string
    is_policy_container = False
    objectids = []
    try:
       objectids = ob.objectIds()
    except AttributeError, TypeError:
       pass
    if WorkflowPolicyConfig_id in objectids:
        is_policy_container = True

    # Inspired by implementation in CPSWorkflowTool.py of CPSCore 3.9.0
    # Workflow needs to be determined by true containment not context
    # so we loop over the actual containers
    chain = None
    wfpolicyconfig = None
    current_ob = aq_inner(ob)
    start_here = True
    portal = aq_base(getToolByName(self, 'portal_url').getPortalObject())
    while chain is None and current_ob is not None:
        if shasattr(current_ob, WorkflowPolicyConfig_id):
            wfpolicyconfig = getattr(current_ob, WorkflowPolicyConfig_id)
            chain = wfpolicyconfig.getPlacefulChainFor(portal_type, start_here=start_here)
            if chain is not None:
                return chain

        elif aq_base(current_ob) is portal:
            break
        start_here = False
        current_ob = aq_inner(aq_parent(current_ob))

    # Note that if chain is not in cbt or has a value of None, we use a default chain.
    if cbt is not None:
        chain = cbt.get(portal_type, None)

    if chain is None:
        chain = self.getDefaultChainFor(ob)
        if chain is None:
            # CMFCore default
            return ()

    return chain

# don't loose the docstrings
getChainFor.__doc__ = '\n'.join((WorkflowTool.getChainFor.__doc__, getChainFor.__doc__))
WorkflowTool.getChainFor = getChainFor



def getWorklists(self):
    """ This method is ugly.

    Worklists are deprecated and must be replaced by catalog search.
    """
    # We want to know which types use the workflows with worklists
    # This for example avoids displaying 'pending' of multiple workflows in the same worklist
    types_tool = getToolByName(self, 'portal_types')
    list_ptypes = types_tool.listContentTypes()
    types_by_wf = {} # wf:[list,of,types]
    for t in list_ptypes:
        for wf in self.getChainFor(t):
            types_by_wf[wf] = types_by_wf.get(wf,[]) + [t]

    # Placeful stuff
    placeful_tool = getToolByName(self, 'portal_placeful_workflow')
    for policy in placeful_tool.getWorkflowPolicies():
        for t in list_ptypes:
            chain = policy.getChainFor(t) or ()
            for wf in chain:
                types_by_wf[wf] = types_by_wf.get(wf,[]) + [t]

    wf_with_wlists = {}
    for id in self.getWorkflowIds():
        # the above list incomprehension merely _flattens_ nested sequences into 1 sequence

        wf=self.getWorkflowById(id)
        if hasattr(wf, 'worklists'):
            wlists = []
            for worklist in wf.worklists._objects:
                wlist_def=wf.worklists._mapping[worklist['id']]
                # Make the var_matches a dict instead of PersistentMapping to enable access from scripts
                var_matches = {}
                for key in wlist_def.var_matches.keys(): var_matches[key] = wlist_def.var_matches[key]
                a_wlist = {
                    'id':worklist['id'],
                    'guard' : wlist_def.getGuard(),
                    'guard_permissions' : wlist_def.getGuard().permissions,
                    'guard_roles' : wlist_def.getGuard().roles,
                    'catalog_vars' : var_matches,
                    'name' : getattr(wlist_def, 'actbox_name', None),
                    'url' : getattr(wlist_def, 'actbox_url', None),
                    'types' : types_by_wf.get(id,[])
                }
                wlists.append(a_wlist)
            # yes, we can duplicates, we filter duplicates out on the calling PyhtonScript client
            wf_with_wlists[id]=wlists

    return wf_with_wlists

getWorklists.__doc__ = WorkflowTool.getWorklists.__doc__
WorkflowTool.getWorklists = getWorklists



def getWorklistsResults(self):
    """Return all the objects concerned by one or more worklists

    An object is returned only once, even if is return by several worklists.
    Make the whole stuff as expensive it is.
    """
    sm = getSecurityManager()
    # We want to know which types use the workflows with worklists
    # This for example avoids displaying 'pending' of multiple workflows in the same worklist
    types_tool = getToolByName(self, 'portal_types')
    catalog = getToolByName(self, 'portal_catalog')

    list_ptypes = types_tool.listContentTypes()
    types_by_wf = {} # wf:[list,of,types]
    for t in list_ptypes:
        for wf in self.getChainFor(t):
            types_by_wf[wf] = types_by_wf.get(wf, []) + [t]

    # Placeful stuff
    placeful_tool = getToolByName(self, 'portal_placeful_workflow')
    for policy in placeful_tool.getWorkflowPolicies():
        for t in list_ptypes:
            chain = policy.getChainFor(t) or ()
            for wf in chain:
                types_by_wf[wf] = types_by_wf.get(wf, []) + [t]

    objects_by_path = {}
    for id in self.getWorkflowIds():

        wf=self.getWorkflowById(id)
        if hasattr(wf, 'worklists'):
            wlists = []
            for worklist in wf.worklists._objects:
                wlist_def=wf.worklists._mapping[worklist['id']]
                # Make the var_matches a dict instead of PersistentMapping to enable access from scripts
                catalog_vars = {}
                for key in wlist_def.var_matches.keys():
                    catalog_vars[key] = wlist_def.var_matches[key]
                for result in catalog.searchResults(catalog_vars, portal_type=types_by_wf.get(id, [])):
                    o = result.getObject()
                    if o \
                       and id in self.getChainFor(o) \
                       and wlist_def.getGuard().check(sm, wf, o):
                        absurl = o.absolute_url()
                        if absurl:
                            objects_by_path[absurl] = (o.modified(), o)

    results = objects_by_path.values()
    results.sort()
    return tuple([ obj[1] for obj in results ])

WorkflowTool.getWorklistsResults = getWorklistsResults
