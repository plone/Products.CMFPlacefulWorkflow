##parameters=submit, wfpid, title, description, wf, default_workflow_id
##title=set local workflow policy mapping
#-*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

request = context.REQUEST
policy = getToolByName(context, 'portal_placeful_workflow').getWorkflowPolicyById(wfpid)

policy.setTitle(title)
policy.setDescription(description)

for pt, wf in wf.items():
    policy.setChain(portal_type=pt, chain=(wf,))

policy.setDefaultChain(default_chain=(default_workflow_id,))

wf_tool = getToolByName(context, 'portal_workflow')
wf_tool.updateRoleMappings()

psm = "Changes to criteria saved."
if request:
    request.RESPONSE.redirect('prefs_workflow_policy_mapping?wfpid=%s&portal_status_message=%s' % (wfpid, psm))

return request
