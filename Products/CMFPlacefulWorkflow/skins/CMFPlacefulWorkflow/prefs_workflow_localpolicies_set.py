##parameters=delete=None, add=None
##title=set local workflow policies prefs
##

from Products.CMFCore.utils import getToolByInterfaceName
from Products.CMFPlacefulWorkflow import CMFPlacefulWorkflowMessageFactory as _

request = context.REQUEST

policy_ids = request.get('policy_ids',[])
policy_id = request.get('policy_id', None)
policy_duplicate_id = request.get('policy_duplicate_id', 'empty')

pwtool = getToolByInterfaceName('Products.CMFPlacefulWorkflow.interfaces.IPlacefulWorflowTool')

if delete and policy_ids:
    for policy_id in policy_ids:
        if policy_id in pw_tool.objectIds():
            pwtool.manage_delObjects([policy_id,])
    context.plone_utils.addPortalMessage(_(u'Deleted Local Workflow Policy.'))
    context.REQUEST.RESPONSE.redirect('prefs_workflow_localpolicies_form')

elif add and policy_id:
    pwtool.manage_addWorkflowPolicy(id=policy_id, duplicate_id=policy_duplicate_id)
    context.plone_utils.addPortalMessage(_(u'Local Workflow Policy added.'))
    context.REQUEST.RESPONSE.redirect('prefs_workflow_policy_mapping?wfpid='+policy_id)
