##parameters=
##title=add workflow policy configuration
##

context.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()

msg = context.translate('Workflow policy configuration added', domain='cmfplacefulworkflow')

context.REQUEST.RESPONSE.redirect('placeful_workflow_configuration?portal_status_message=' + msg)
