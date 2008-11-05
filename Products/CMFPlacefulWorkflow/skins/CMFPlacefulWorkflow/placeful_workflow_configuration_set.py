##parameters=policy_in='', policy_below=''
##title=set placeful workflow configuration
##
from Products.CMFCore.utils import getToolByName
from Products.CMFPlacefulWorkflow import CMFPlacefulWorkflowMessageFactory as _

request = context.REQUEST
config = getToolByName(context, 'portal_placeful_workflow').getWorkflowPolicyConfig(context)

if not config:
    message = _(u'No config in this folder.')
else:
    if not context.portal_placeful_workflow.isValidPolicyName(policy_in) \
       and not policy_in == '':
        raise AttributeError("%s is not a valid policy id" % policy_in)

    if not context.portal_placeful_workflow.isValidPolicyName(policy_below) \
       and not policy_below == '':
        raise AttributeError("%s is not a valid policy id" % policy_below)

    config.setPolicyIn(policy=policy_in)
    config.setPolicyBelow(policy=policy_below, update_security=True)
    message = _('Changed policies.')

context.plone_utils.addPortalMessage(message)
request.RESPONSE.redirect('placeful_workflow_configuration')
