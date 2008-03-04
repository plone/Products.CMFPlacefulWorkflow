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
from Products.CMFPlacefulWorkflow.global_symbols import Log, LOG_DEBUG

_marker = []

class PlacefulWorkflowXMLAdapter(FolderXMLAdapter):

    _LOGGER_ID = 'placeful_workflow'

    body = property(XMLAdapterBase._exportBody,
                    XMLAdapterBase._importBody)

class WorkflowPoliciesXMLAdapter(WorkflowToolXMLAdapter):

    _LOGGER_ID = 'placeful_workflow'

    @property
    def name(self):
        Log(LOG_DEBUG, self.context.id)
        return self.context.id

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
            typestool = getToolByName(self.context, 'portal_types')
            typeinfos = sorted(typestool.listTypeInfo(),
                               key=lambda type: type.getId())
            for ti in typeinfos:
                type_id = ti.getId()
                chain = self.context._chains_by_type.get(type_id, _marker)
                child = self._doc.createElement('type')
                if chain is _marker or len(chain) == 0:
                    #child.setAttribute('acquire', 'True')
                    # Types omited from the policy must acquire.
                    # XXX: question is: do we need to explicit export them?
                    # it doesnt hurt, but makes the file a bit more confusing.
                    # chains that arent exported also arent imported and if
                    # no chain is found it falls back to acquire anyway
                    # chains with acquire are also ignored on import.
                    # -- jensens
                    continue
                child.setAttribute('type_id', type_id)
                for workflow_id in chain:
                    sub = self._doc.createElement('bound-workflow')
                    sub.setAttribute('workflow_id', workflow_id)
                    child.appendChild(sub)
                node.appendChild(child)
        fragment.appendChild(node)
        return fragment

    def _initChains(self, node):
        """ Import policies from XML

        Types specified are in two cases:

        - no workflow is present then the type take the default worklfow

        - one or more workflows are presents then type take the chain in the
          same order

        For any types not specified, we do nothing and they will acquire their
        chain from another policy or from portal_workfow.
        """
        seen = set()
        for child in node.childNodes:
            if child.nodeName != 'bindings':
                continue
            for sub in child.childNodes:
                Log(LOG_DEBUG, sub)
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

        #for ti in getToolByName(self.context,
        #                        'portal_types').listTypeInfo():
        #    type_id = ti.getId()
        #    if type_id not in seen:
        #        self.context.setChainForPortalTypes((type_id,),
        #                                            DEFAULT_CHAIN)

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
