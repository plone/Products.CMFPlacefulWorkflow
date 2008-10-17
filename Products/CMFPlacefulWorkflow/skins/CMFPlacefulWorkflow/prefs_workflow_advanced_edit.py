## Script (Python) "prefs_workflow_advanced_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=wf
##title=
##

for w in wf.keys():
    context.portal_workflow.setChainForPortalTypes((w,), wf[w], REQUEST=context.REQUEST)
return context.prefs_workflow_advanced()
