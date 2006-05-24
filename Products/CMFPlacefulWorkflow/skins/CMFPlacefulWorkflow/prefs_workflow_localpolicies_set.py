##parameters=delete=None, add=None
##title=set local workflow policies prefs
##

from Products.CMFCore.utils import getToolByName
request = context.REQUEST

policy_ids = request.get('policy_ids',[])
policy_id = request.get('policy_id', None)
policy_duplicate_id = request.get('policy_duplicate_id', 'empty')

pw_tool = getToolByName(context, 'portal_placeful_workflow')
types_tool = getToolByName(context, 'portal_types')

msg="No action"

if delete and policy_ids:
    msg = "Deleting Workflow Policy."
    for policy_id in policy_ids:
        if policy_id in pw_tool.objectIds():
            pw_tool.manage_delObjects([policy_id,])
    context.REQUEST.RESPONSE.redirect('prefs_workflow_localpolicies_form?portal_status_message=%s' % msg)

elif add and policy_id:

    msg = "Local Workflow Policy added."
    pw_tool.manage_addWorkflowPolicy(id=policy_id, duplicate_id=policy_duplicate_id)

    context.REQUEST.RESPONSE.redirect('prefs_workflow_policy_mapping?wfpid=%s&portal_status_message=%s' % (policy_id, msg))
