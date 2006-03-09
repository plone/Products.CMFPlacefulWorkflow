##parameters=delete=None, add=None
##title=set local workflow policies prefs
##

from Products.CMFPlacefulWorkflow import CMFPlacefulWorkflowMessageFactory as _

request = context.REQUEST

policy_ids = request.get('policy_ids',[])
policy_id = request.get('policy_id', None)

pwt = context.portal_placeful_workflow

if delete and policy_ids:
    for policy_id in policy_ids:
        if policy_id in pwt.objectIds():
            pwt.manage_delObjects([policy_id,])
    context.plone_utils.addPortalMessage(_(u'Deleted Local Workflow Policy.'))
    context.REQUEST.RESPONSE.redirect('prefs_workflow_localpolicies_form')
elif add and policy_id:
    pwt.manage_addWorkflowPolicy(id = policy_id)
    context.plone_utils.addPortalMessage(_(u'Local Workflow Policy added.'))
    context.REQUEST.RESPONSE.redirect('prefs_workflow_policy_mapping?wfpid='+policy_id)
