##parameters=submit, wfpid, title, description, wf, default_workflow_id
##title=set local workflow policy mapping
#-*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByInterfaceName
from Products.CMFPlacefulWorkflow import CMFPlacefulWorkflowMessageFactory as _

request = context.REQUEST
pwtool_iface = 'Products.CMFPlacefulWorkflow.interfaces.IPlacefulWorflowTool'
pwtool = getToolByInterfaceName(pwtool_iface)
policy = pwtool.getWorkflowPolicyById(wfpid)

policy.setTitle(title)
policy.setDescription(description)

policy.setDefaultChain(default_chain=(default_workflow_id,))

for pt, wf in wf.items():
    policy.setChain(portal_type=pt, chain=(wf,))

wftool = getToolByInterfaceName('Products.CMFCore.interfaces.IConfigurableWorkflowTool')
wftool.updateRoleMappings()

context.plone_utils.addPortalMessage(_(u'Changes to criteria saved.'))
if request:
    request.RESPONSE.redirect('prefs_workflow_policy_mapping?wfpid=%s' % wfpid)

return request
