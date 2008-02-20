# -*- coding: utf-8 -*-
## CMFPlacefulWorflow
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
Contributed by Jazkarta
"""
__version__ = "$Revision:  $"
# $Source:  $
# $Id:  $
__docformat__ = 'restructuredtext'
from Products.GenericSetup.utils import exportObjects, importObjects
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.OFSP.exportimport import FolderXMLAdapter

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.exportimport.workflow import WorkflowToolXMLAdapter

from Products.CMFPlacefulWorkflow.DefaultWorkflowPolicy import DEFAULT_CHAIN

_marker = []

class PlacefulWorkflowXMLAdapter(FolderXMLAdapter):

    _LOGGER_ID = 'placeful_workflow'

    body = property(XMLAdapterBase._exportBody,
                    XMLAdapterBase._importBody)

class WorkflowPoliciesXMLAdapter(WorkflowToolXMLAdapter):

    _LOGGER_ID = 'placeful_workflow'

    name = 'workflow_policies'

    def _extractChains(self):
        fragment = self._doc.createDocumentFragment()
        node = self._doc.createElement('bindings')
        child = self._doc.createElement('default')
        for workflow_id in self.context._default_chain or ():
            sub = self._doc.createElement('bound-workflow')
            sub.setAttribute('workflow_id', workflow_id)
            child.appendChild(sub)
        node.appendChild(child)
        if self.context._chains_by_type:
            for ti in sorted(
                getToolByName(self.context,
                              'portal_types').listTypeInfo(),
                key=lambda type: type.getId()):
                type_id = ti.getId()
                chain = self.context._chains_by_type.get(type_id,
                                                         _marker)
            
                if chain == [DEFAULT_CHAIN]:
                    # types using the policy default are ommitted
                    continue
            
                child = self._doc.createElement('type')
                child.setAttribute('type_id', type_id)
                if chain is _marker:
                    # Types omited from the policy must acquire
                    child.setAttribute('acquire', 'True')
            
                for workflow_id in chain:
                    sub = self._doc.createElement('bound-workflow')
                    sub.setAttribute('workflow_id', workflow_id)
                    child.appendChild(sub)
                node.appendChild(child)
        fragment.appendChild(node)
        return fragment

    def _initChains(self, node):
        seen = set()
        for child in node.childNodes:
            if child.nodeName != 'bindings':
                continue
            for sub in child.childNodes:
                if sub.nodeName == 'default':
                    self.context.setDefaultChain(self._getChain(sub))
                if sub.nodeName == 'type':
                    type_id = str(sub.getAttribute('type_id'))
                    assert type_id not in seen, (
                        'Type %s listed more than once' % type_id)
                    seen.add(type_id)

                    acquire = sub.getAttribute('acquire')
                    chain = self._getChain(sub)
                    assert not (acquire and chain), (
                        'Type %s is marked to acquire but also '
                        'included a chain: %s' % (type_id, chain))
                    if acquire:
                        # omit from the policy to acquire
                        continue
                    self.context.setChainForPortalTypes((type_id,),
                                                        chain)

        # For any types not specified, we use the policy default
        for ti in getToolByName(self.context,
                                'portal_types').listTypeInfo():
            type_id = ti.getId()
            if type_id not in seen:
                self.context.setChainForPortalTypes((type_id,),
                                                    DEFAULT_CHAIN)

    def _getChain(self, node):
        result = super(WorkflowPoliciesXMLAdapter,
                       self)._getChain(node)
        if result == '':
            return []
        return result.split(',')

def importWorkflowPolicies(context):
    """Import workflow policies from the XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_placeful_workflow')
    importObjects(tool, '', context)
    

def exportWorkflowPolicies(context):
    """Export workflow policies as an XML file.
    """
    site = context.getSite()
    tool = getToolByName(site, 'portal_placeful_workflow')
    if tool is None:
        logger = context.getLogger('workflow_policies')
        logger.info('Nothing to export.')
        return

    exportObjects(tool, '', context)
