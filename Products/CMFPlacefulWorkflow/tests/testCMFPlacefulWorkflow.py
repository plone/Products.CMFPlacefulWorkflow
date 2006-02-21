# -*- coding: utf-8 -*-
## CMFPlacefulWorkflow
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
CMFPlacefulWorkflow Unittest
"""
__version__ = "$Revision$"
# $Source: /cvsroot/ingeniweb/CMFPlacefulWorkflow/tests/testCMFPlacefulWorkflow.py,v $
# $Id$
__docformat__ = 'restructuredtext'


from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from CMFPlacefulWorkflowTestCase import CMFPlacefulWorkflowTestCase

try:
   _standard_permissions = ZopeTestCase._standard_permissions
except AttributeError:
   _standard_permissions = ZopeTestCase.standard_permissions
_edit_permissions     = [] # [PlacefulWorkflowPolicy_editPermission,]
_all_permissions      = _edit_permissions

#Install our product 
PloneTestCase.installProduct('CMFPlacefulWorkflow')
PloneTestCase.setupPloneSite()

# Other imports
from Products.CMFCore.utils import getToolByName

# Set log options if Log module is available
# This is done to set LOG_PROCESSORs to file logs instead of Zope logs
try:
    import Log
    import os

    Log.LOG_LEVEL = Log.LOG_DEBUG

    Log.LOG_PROCESSOR = {
        Log.LOG_NONE: Log.logFile,
        Log.LOG_CRITICAL: Log.logFile,
        Log.LOG_ERROR: Log.logFile,
        Log.LOG_WARNING: Log.logFile,
        Log.LOG_NOTICE: Log.logFile,
        Log.LOG_DEBUG: Log.logFile,
        }

    Log.Log(Log.LOG_NOTICE, "Starting %s at %d debug level" % (os.path.dirname(__file__), Log.LOG_LEVEL, ))

except:
    print "Log module not available"
    LOG_DEBUG = None
    LOG_NOTICE = None
    LOG_WARNING = None
    LOG_ERROR = None
    LOG_CRITICAL = None
    def Log(*args, **kw):
        pass
    raise

class TestPlacefulWorkflow(CMFPlacefulWorkflowTestCase):
    """ Testing all add-on and modified method for workflow stuff """

    def createMember(self, id, pw, email, roles=('Member',)):
        pr = self.portal.portal_registration
        member = pr.addMember(id, pw, roles, properties={ 'username': id, 'email' : email })
        #self.failUnless(id in self.portal.Members.objectIds())
        return member
    
    def installation(self, productName):
        self.qi = self.portal.portal_quickinstaller
        self.qi.installProduct(productName)
        
    def setupSecurityContext(self,):
        self.logout()
        self.loginAsPortalOwner()
        # Create a few members
        self.user1 = self.createMember('user1', 'abcd4', 'abc@domain.tld')
        self.user2 = self.createMember('user2', 'abcd4', 'abc@domain.tld')
        self.user3 = self.createMember('user3', 'abcd4', 'abc@domain.tld')
        
        self.folder = self.portal.portal_membership.getHomeFolder('user1')
        self.installation('CMFPlacefulWorkflow')
        self.logout()
    
    def afterSetUp(self,):
        """
        afterSetUp(self) => This method is called to create an empty PloneArticle.
        It also joins three users called 'user1', 'user2' and 'user3'.
        """
        #some usefull properties/tool
        self.catalog = getToolByName(self.portal, 'portal_catalog')
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.membershipTool = getToolByName(self.portal, 'portal_membership')
        self.memberdataTool = getToolByName(self.portal, 'portal_memberdata')

        self.placefulworkflowTool = getToolByName(self.portal, 'portal_placeful_workflow')
        
        self.setupSecurityContext()
        
        self.login('user1')
        #self.createPolicy()
        
    def createArticle(self, ):
        """
        Create new policy
        """
        # Content creation
        self.contentId = 'myPolicy'

        # XXX

    def test_01_addWorkflowPolicyConfig(self,):
        """
        Add workflow policy config
        """
        # No policy config should exist before
        self.failIf(WorkflowPolicyConfig_id in self.portal.objectIds() )
        # Add a policy config
        self.portal.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        # Make sure the policy config is there
        self.failUnless( WorkflowPolicyConfig_id in self.portal.objectIds() )

    def test_02_checkWorkflowPolicyConfig(self,):
        """
        Add workflow policy config
        """
        self.portal.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        pc = getattr(self.portal, WorkflowPolicyConfig_id)
        self.failUnless(pc.getPolicyBelow()==None)
        self.failUnless(pc.getPolicyIn()==None)

    def test_03_addWorkflowPolicy(self,):
        """
        Add workflow policy
        """
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')
        gsp = getattr(pwt, 'foo_bar_policy', None)
        self.failUnless(gsp!=None)

    def test_04_addWorkflowPolicyAndConfigForIt(self,):
        """
        Add workflow policy
        """
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')
        self.portal.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        pc = getattr(self.portal, WorkflowPolicyConfig_id)
        pc.setPolicyIn('foo_bar_policy')
        pc.setPolicyBelow('foo_bar_policy')
        self.failUnless(pc.getPolicyInId()=='foo_bar_policy')
        self.failUnless(pc.getPolicyBelowId()=='foo_bar_policy')

    def test_05_editWorkflowPolicy(self,):
        """
        Add workflow policy
        """
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')
        gsp = pwt.getWorkflowPolicyById('foo_bar_policy')
        gsp.setChainForPortalTypes(['Document','Folder'], ['plone_workflow','folder_workflow'])
        self.failUnless(gsp.getChainFor('Document')==('plone_workflow','folder_workflow',))
        self.failUnless(gsp.getChainFor('Folder')==('plone_workflow','folder_workflow',))

    def test_06_getWorkflowPolicyIds(self,):
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy_2' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')
        wp_ids=pwt.getWorkflowPolicyIds()
        self.failUnless('foo_bar_policy' in wp_ids)
        self.failUnless('foo_bar_policy_2' in wp_ids)
        self.failUnless(len(wp_ids)==2)

    def test_07_getChainFor(self,):
        # Let's see what the chain is before
        self.logout()
        self.loginAsPortalOwner()

        pw = self.portal.portal_workflow
        self.failUnless(pw.getChainFor('Document')==('plone_workflow',) )

        self.portal.invokeFactory('Document', id='doc_before', text='foo bar baz')

        # The chain should be different now
        # Workflow tool should look for policy definition and return
        # the chain of the correct policy
        self.failUnless(pw.getChainFor(self.portal.doc_before)==('plone_workflow',) )

        # Let's define another policy
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')

        # And redefine the chain for Document
        gsp = pwt.getWorkflowPolicyById('foo_bar_policy')

        gsp.setChainForPortalTypes(['Document'], ['folder_workflow'])

        # Try getting the new chain directly
        self.assertEqual(gsp.getChainFor('Document'), ('folder_workflow',) )

        # Add a config at the root that will use the new policy
        self.portal.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        self.failUnless('.wf_policy_config' in self.portal.objectIds())

        # Let's set the policy to the config
        pc = getattr(self.portal, WorkflowPolicyConfig_id)
        pc.setPolicyIn('foo_bar_policy')
        pc.setPolicyBelow('foo_bar_policy')

        self.assertEqual(pc.getPlacefulChainFor('Document', start_here=1), ('folder_workflow',))

        self.portal.invokeFactory('Document', id='doc', text='foo bar baz')

        # The chain should be different now
        # Workflow tool should look for policy definition and return
        # the chain of the correct policy
        self.assertEqual(pw.getChainFor(self.portal.doc), ('folder_workflow',) )
        # The chain for the first document should have changed now
        self.assertEqual(pw.getChainFor(self.portal.doc_before), ('folder_workflow',) )

    def test_08_getChainFor(self,):
        # Let's see what the chain is before
        pwt = self.portal.portal_placeful_workflow
        self.failUnless(pwt.getMaxChainLength()==1)
        pwt.setMaxChainLength(2)
        self.failUnless(pwt.getMaxChainLength()==2)

    def test_09_wft_getChainFor(self,):
        self.logout()
        self.loginAsPortalOwner()
        self.portal.invokeFactory('Folder', id='folder')
        self.portal.folder.invokeFactory('Document', id='document', text='foo')

        # Check default
        wft = self.portal.portal_workflow
        chain = wft.getChainFor('Document')
        self.assertEqual(tuple(chain), ('plone_workflow',))

        # Check global chain
        wft.setChainForPortalTypes(('Document',), ('wf',))
        chain = wft.getChainFor('Document')
        self.assertEqual(tuple(chain), ('wf',))

        # Check global chain, using object
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ('wf',))

        # Remove global chain
        wft.setChainForPortalTypes(('Document',), ())
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ())

    def test_10_wft_getChainFor_placeful(self):
        self.logout()
        self.loginAsPortalOwner()
        wft = self.portal.portal_workflow
        self.portal.invokeFactory('Folder', id='folder')
        self.portal.folder.invokeFactory('Document', id='document')
        self.portal.folder.invokeFactory('Folder', id='folder2')
        self.portal.folder.folder2.invokeFactory('Document', id='document2')

        # Create a policy
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById('foo_bar_policy')
        gsp1.setChainForPortalTypes(['Document'], ['folder_workflow'])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)
        pc.setPolicyIn('foo_bar_policy')
        pc.setPolicyBelow('foo_bar_policy')

        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ('folder_workflow',))

        # Create a different policy
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy2' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')

        # And redefine the chain for Document
        gsp2 = pwt.getWorkflowPolicyById('foo_bar_policy2')
        gsp2.setChainForPortalTypes(['Document'], ['plone_workflow'])

        # Add a different config in the second folder
        self.portal.folder.folder2.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        pc = getattr(self.portal.folder.folder2, WorkflowPolicyConfig_id)
        pc.setPolicyIn('foo_bar_policy2')
        pc.setPolicyBelow('foo_bar_policy2')

        # Check inheritance order
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ('plone_workflow',))

        # Check empty chain
        gsp2.setChain('Document', ())
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ())

        # Check default
        wft.setDefaultChain('folder_workflow')
        gsp2.setChainForPortalTypes(('Document',), ('(Default)',))
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ('folder_workflow',))

    def test_11_In_and_Below(self):
        self.logout()
        self.loginAsPortalOwner()
        wft = self.portal.portal_workflow
        self.portal.invokeFactory('Folder', id='folder')
        self.portal.folder.invokeFactory('Document', id='document')
        self.portal.folder.invokeFactory('Folder', id='folder2')
        self.portal.folder.folder2.invokeFactory('Document', id='document2')

        # Create a policy
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById('foo_bar_policy')
        gsp1.setChainForPortalTypes(['Document'], ['plone_workflow'])

        # Create a policy
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy2' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById('foo_bar_policy2')
        gsp1.setChainForPortalTypes(['Document'], ['folder_workflow'])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)

        # In folder 1, we want to have plone_workflow
        # We set PolicyIn to the first policy in folder 1
        pc.setPolicyIn('foo_bar_policy')

        # In folder 2, we want to have folder_workflow
        # We set PolicyBelow to the second policy in folder 2
        pc.setPolicyBelow('foo_bar_policy2')

        # A document in folder 2 should have folder_workflow
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ('folder_workflow',))

        # A document in folder 1 should have plone_workflow
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ('plone_workflow',))

    def test_11_getWorkflowPolicyById_edge_cases(self):
        pwt = self.portal.portal_placeful_workflow
        self.assertEqual(pwt.getWorkflowPolicyById('dummy'), None)

    def test_12_getWorkflowPolicyById_edge_cases(self):
        pwt = self.portal.portal_placeful_workflow
        self.assertEqual(pwt.getWorkflowPolicyById(None), None)


    def test_13_getWorkflowPolicyConfig(self):
        pwt = self.portal.portal_placeful_workflow
        config = pwt.getWorkflowPolicyConfig(self.portal)
        self.assertEqual(config, None)

    def test_14_getWorkflowPolicyConfig(self):
        self.logout()
        self.loginAsPortalOwner()
        wft = self.portal.portal_workflow
        self.portal.invokeFactory('Folder', id='folder')
        self.portal.folder.invokeFactory('Document', id='document')
        self.portal.folder.invokeFactory('Folder', id='folder2')
        self.portal.folder.folder2.invokeFactory('Document', id='document2')

        # Create a policy
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')
        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById('foo_bar_policy')
        gsp1.setChainForPortalTypes(['Document'], ['folder_workflow'])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)
        pc.setPolicyIn('foo_bar_policy')
        pc.setPolicyBelow('foo_bar_policy')

        # You should only be able to get a config in the folder itself
        config = pwt.getWorkflowPolicyConfig(self.portal.folder)
        self.failUnless(config!=None)

        # Not in the folder above
        config = pwt.getWorkflowPolicyConfig(self.portal)
        self.assertEqual(config, None)

        # Not in a document in the folder
        config = pwt.getWorkflowPolicyConfig(self.portal.folder.document)
        self.assertEqual(config, None)

        # Not in a folder below
        config = pwt.getWorkflowPolicyConfig(self.portal.folder.folder2)
        self.assertEqual(config, None)

        # Not in a document in a folder below
        config = pwt.getWorkflowPolicyConfig(self.portal.folder.folder2.document2)
        self.assertEqual(config, None)

    def test_15_wft_getChainFor_placeful_with_strange_wrapper(self):
        self.logout()
        self.loginAsPortalOwner()
        wft = self.portal.portal_workflow
        self.portal.invokeFactory('Folder', id='folder')
        self.portal.folder.invokeFactory('Document', id='document')
        self.portal.invokeFactory('Folder', id='folder2')
        self.portal.folder2.invokeFactory('Document', id='document2')

        # Create a policy
        pwt = self.portal.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(id = 'foo_bar_policy' \
                                    , workflow_policy_type = 'default_workflow_policy'+\
                                    ' (Simple Policy)')

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById('foo_bar_policy')
        gsp1.setChainForPortalTypes(['Document'], ['folder_workflow'])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)
        pc.setPolicyIn('foo_bar_policy')
        pc.setPolicyBelow('foo_bar_policy')

        chain = wft.getChainFor(self.portal.folder2.document2)
        self.assertEqual(tuple(chain), ('plone_workflow',))

        # What if we acquired the doc from the wrong place
        wrapped_doc = self.portal.folder2.document2.__of__(self.portal.folder)
        chain = wft.getChainFor(wrapped_doc)
        self.assertEqual(tuple(chain), ('plone_workflow',))

        # What if we acquired the container from the wrong place
        wrapped_doc = self.portal.folder2.__of__(self.portal.folder).document2
        chain = wft.getChainFor(wrapped_doc)
        self.assertEqual(tuple(chain), ('plone_workflow',))

# What if the "in" and/or the "below" policy of a .config is empty?

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPlacefulWorkflow))
    return suite
