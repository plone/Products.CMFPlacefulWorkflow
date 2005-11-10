##parameters=
##title=add workflow policy configuration
##

context.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()

msg = "Workflow policy configuration added"

context.REQUEST.RESPONSE.redirect('placeful_workflow_configuration?portal_status_message=' + msg)
