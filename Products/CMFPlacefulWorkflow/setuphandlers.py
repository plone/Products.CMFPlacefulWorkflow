from zope.interface import alsoProvides
from Products.CMFCore.utils import getToolByName
from Products.CMFPlacefulWorkflow.interfaces import IPlacefulMarker

def installMarker(context):
    """
    Apply a marker interface to the workflow tool to indicate that the
    product is installed.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('placeful_marker.txt') is None:
        return
    site = context.getSite()
    wf = getToolByName(site, 'portal_workflow', None)
    if wf is not None:
        alsoProvides(wf, IPlacefulMarker)
