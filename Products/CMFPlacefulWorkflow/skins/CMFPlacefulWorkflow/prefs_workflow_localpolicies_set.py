##parameters=delete=None, add=None
##title=set local workflow policies prefs
##
request = context.REQUEST

policy_ids = request.get('policy_ids',[])
policy_id = request.get('policy_id', None)

pwt = context.portal_placeful_workflow

msg="No action"

if delete and policy_ids:
    msg = 'Deleting Local Workflow Policy'
    for policy_id in policy_ids:
        if policy_id in pwt.objectIds():
            pwt.manage_delObjects([policy_id,])
    context.REQUEST.RESPONSE.redirect('prefs_workflow_localpolicies_form?portal_status_message=' + msg)
elif add and policy_id:
    msg = 'Local Workflow Policy added'
    pwt.manage_addWorkflowPolicy(id = policy_id)
    context.REQUEST.RESPONSE.redirect('prefs_workflow_policy_mapping?wfpid='+policy_id+'&portal_status_message=' + msg)
