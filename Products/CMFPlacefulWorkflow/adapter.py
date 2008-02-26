from zope.interface import Interface, implementer
from zope.component import adapter

from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Products.CMFPlacefulWorkflow.interfaces import IPlacefulMarker
from Acquisition import aq_base, aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.interfaces import IWorkflowChain
from Products.CMFPlone.workflow import ToolWorkflowChain

@adapter(Interface, IPlacefulMarker)
@implementer(IWorkflowChain)
def PlacefulWorkflowChain(ob, tool):
    """Monkey-patched by CMFPlacefulWorkflow to look for placeful workflow configurations.

    Goal: find a workflow chain in a policy

    Steps:
    1. ask the object if it contains a policy
    2. if it does, ask him for a chain
    3. if there's no chain for the type the we loop on the parent
    4. if the parent is the portal object or None we stop and ask
       portal_workflow
    """
    if isinstance(ob, basestring):
        # We are not in an object, then we can only get default from
        # portal_workflow
        return ToolWorkflowChain(ob, tool)

    elif hasattr(aq_base(ob), 'getPortalTypeName'):
        portal_type = ob.getPortalTypeName()
    else:
        portal_type = None

    if portal_type is None or ob is None:
        return ()

    # Inspired by implementation in CPSWorkflowTool.py of CPSCore 3.9.0
    # Workflow needs to be determined by true containment not context
    # so we loop over the actual containers
    chain = None
    wfpolicyconfig = None
    current_ob = aq_inner(ob)
    # start_here is used to check 'In policy': We check it only in the
    # first folder
    start_here = True
    portal = aq_base(getToolByName(tool, 'portal_url').getPortalObject())
    while chain is None and current_ob is not None:
        if base_hasattr(current_ob, WorkflowPolicyConfig_id):
            wfpolicyconfig = getattr(current_ob, WorkflowPolicyConfig_id)
            chain = wfpolicyconfig.getPlacefulChainFor(portal_type,
                                                       start_here=start_here)
            if chain is not None:
                return chain

        elif aq_base(current_ob) is portal:
            break
        start_here = False
        current_ob = aq_inner(aq_parent(current_ob))

    # fallback on the default mechanism
    return ToolWorkflowChain(ob, tool)
