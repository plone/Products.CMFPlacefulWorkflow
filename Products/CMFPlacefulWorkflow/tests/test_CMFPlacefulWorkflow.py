# CMFPlacefulWorkflow
# Copyright (C)2005 Ingeniweb

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
CMFPlacefulWorkflow Unittest
"""

from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_PASSWORD
from plone.base.utils import get_installer
from Products.CMFCore.utils import getToolByName
from Products.CMFPlacefulWorkflow.interfaces import IPlacefulMarker
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import (  # noqa: E501
    WorkflowPolicyConfig_id,
)
from Products.CMFPlacefulWorkflow.tests.CMFPlacefulWorkflowTestCase import (  # noqa: E501
    CMFPlacefulWorkflowTestCase,
)


_edit_permissions = []
_all_permissions = _edit_permissions


class TestPlacefulWorkflow(CMFPlacefulWorkflowTestCase):
    """Testing all add-on and modified method for workflow stuff"""

    def createMember(self, id, pw, email, roles=("Member",)):
        pr = self.portal.portal_registration
        member = pr.addMember(
            id, pw, roles, properties={"username": id, "email": email}
        )
        return member

    def setupSecurityContext(
        self,
    ):
        # Create a few members
        self.user1 = self.createMember("user1", TEST_USER_PASSWORD, "abc@domain.tld")
        self.user2 = self.createMember("user2", TEST_USER_PASSWORD, "abc@domain.tld")
        self.user3 = self.createMember("user3", TEST_USER_PASSWORD, "abc@domain.tld")

        self.folder = self.portal.portal_membership.getHomeFolder("user1")
        self.qi = get_installer(self.portal)
        self.qi.install_product("CMFPlacefulWorkflow")

    def setUp(
        self,
    ):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.catalog = getToolByName(self.portal, "portal_catalog")
        self.workflow = getToolByName(self.portal, "portal_workflow")
        self.membershipTool = getToolByName(self.portal, "portal_membership")
        self.memberdataTool = getToolByName(self.portal, "portal_memberdata")

        self.portal_placeful_workflow = getToolByName(
            self.portal, "portal_placeful_workflow"
        )

        self.setupSecurityContext()

        # login(self.portal, 'user1')
        # self.createPolicy()

    def createArticle(
        self,
    ):
        """
        Create new policy
        """
        # Content creation
        self.contentId = "myPolicy"
        # XXX

    def test_marker_applied_and_unapplied(self):
        """
        Check that the IPlacefulMarker is applied to the workflow tool by
        the install, and removed by the uninstall.
        """
        self.assertTrue(IPlacefulMarker.providedBy(self.workflow))
        self.qi.uninstall_product("CMFPlacefulWorkflow")
        self.assertFalse(IPlacefulMarker.providedBy(self.workflow))

        self.qi.install_product("CMFPlacefulWorkflow")
        self.assertTrue(IPlacefulMarker.providedBy(self.workflow))

    def test_reinstall(self):
        """
        Test if upgrade is going the good way
        """
        self.qi.uninstall_product("CMFPlacefulWorkflow")
        self.qi.install_product("CMFPlacefulWorkflow")
        self.assertTrue("portal_placeful_workflow" in self.portal.objectIds())

    def test_activation_reactivation(self):
        """Test multiple installs and uninstalls."""
        self.qi.uninstall_product("CMFPlacefulWorkflow")
        self.assertFalse("portal_placeful_workflow" in self.portal)
        self.qi.install_product("CMFPlacefulWorkflow")
        self.assertTrue("portal_placeful_workflow" in self.portal)
        self.qi.uninstall_product("CMFPlacefulWorkflow")
        self.assertFalse("portal_placeful_workflow" in self.portal)

    def test_01_addWorkflowPolicyConfig(
        self,
    ):
        """
        Add workflow policy config
        """
        # No policy config should exist before
        self.assertFalse(WorkflowPolicyConfig_id in self.portal.objectIds())
        # Add a policy config
        self.portal.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()
        # Make sure the policy config is there
        self.assertTrue(WorkflowPolicyConfig_id in self.portal.objectIds())

    def test_02_checkWorkflowPolicyConfig(
        self,
    ):
        """
        Add workflow policy config
        """
        self.portal.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()
        pc = getattr(self.portal, WorkflowPolicyConfig_id)
        self.assertEqual(pc.getPolicyBelow(), None)
        self.assertEqual(pc.getPolicyIn(), None)

    def test_03_addWorkflowPolicy(
        self,
    ):
        """
        Add workflow policy
        """
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )
        gsp = getattr(pwt, "foo_bar_policy", None)
        self.assertTrue(gsp is not None)

    def test_04_addWorkflowPolicyAndConfigForIt(
        self,
    ):
        """
        Add workflow policy
        """
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )
        self.portal.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()
        pc = getattr(self.portal, WorkflowPolicyConfig_id)
        pc.setPolicyIn("foo_bar_policy")
        pc.setPolicyBelow("foo_bar_policy")
        self.assertEqual(pc.getPolicyInId(), "foo_bar_policy")
        self.assertEqual(pc.getPolicyBelowId(), "foo_bar_policy")

        logout()

    def test_04_addWorkflowPolicyAndDuplicateConfiguration(
        self,
    ):
        """Add a workflow policy and duplicate another one

        Use a python script that can duplicate another policy or portal_workflow configuration
        """
        pw_tool = self.portal_placeful_workflow
        wf_tool = self.portal.portal_workflow
        ptypes = self.portal.portal_types.objectIds()

        # Part One: duplicate portal_workflow
        pw_tool.manage_addWorkflowPolicy(
            id="foo_bar_policy",
            duplicate_id="portal_workflow",
        )

        policy = pw_tool.getWorkflowPolicyById("foo_bar_policy")

        self.assertEqual(policy.getDefaultChain("XXX"), wf_tool._default_chain)
        for ptype in ptypes:
            chain = policy.getChainFor(ptype)
            if chain is None:
                # Default empty chain is None in a policy and () in
                # portal_workflow
                chain = ()
            self.assertEqual(chain, wf_tool.getChainFor(ptype))

        # Part Two: duplicate another policy
        policy.setDefaultChain(["plone_workflow", "folder_workflow"])
        policy.setChainForPortalTypes(
            ["Document", "Folder"], ["plone_workflow", "folder_workflow"]
        )
        pw_tool.manage_addWorkflowPolicy(
            id="foo_bar_policy2",
            duplicate_id="foo_bar_policy",
        )

        policy2 = pw_tool.getWorkflowPolicyById("foo_bar_policy2")

        self.assertEqual(
            policy.getDefaultChain("XXX"), ("plone_workflow", "folder_workflow")
        )
        for ptype in ptypes:
            if ptype not in ("Document", "Folder"):
                self.assertEqual(policy2.getChainFor(ptype), policy.getChainFor(ptype))
            else:
                self.assertEqual(
                    policy2.getChainFor(ptype), ("plone_workflow", "folder_workflow")
                )

        logout()

    def test_05_editWorkflowPolicy(
        self,
    ):
        """Edit workflow policy"""
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )
        gsp = pwt.getWorkflowPolicyById("foo_bar_policy")
        gsp.setChainForPortalTypes(
            ["Document", "Folder"], ["plone_workflow", "folder_workflow"]
        )
        self.assertEqual(
            gsp.getChainFor("Document"),
            (
                "plone_workflow",
                "folder_workflow",
            ),
        )
        self.assertEqual(
            gsp.getChainFor("Folder"),
            (
                "plone_workflow",
                "folder_workflow",
            ),
        )

    def test_06_getWorkflowPolicyIds(
        self,
    ):
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy_2", "default_workflow_policy (Simple Policy)"
        )
        wp_ids = sorted(pwt.getWorkflowPolicyIds())
        # There are 4 base policies
        self.assertEqual(
            tuple(wp_ids),
            (
                "foo_bar_policy",
                "foo_bar_policy_2",
                "intranet",
                "old-plone",
                "one-state",
                "simple-publication",
            ),
        )

    def test_07_getChainFor(
        self,
    ):
        # Let's see what the chain is before
        pw = self.portal.portal_workflow
        self.assertEqual(pw.getChainFor("Document"), ("simple_publication_workflow",))

        self.portal.invokeFactory("Document", id="doc_before", text="foo bar baz")

        # The chain should be different now
        # Workflow tool should look for policy definition and return
        # the chain of the correct policy
        self.assertEqual(
            pw.getChainFor(self.portal.doc_before), ("simple_publication_workflow",)
        )

        # Let's define another policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )

        # And redefine the chain for Document
        gsp = pwt.getWorkflowPolicyById("foo_bar_policy")

        gsp.setChainForPortalTypes(["Document"], ["folder_workflow"])

        # Try getting the new chain directly
        self.assertEqual(gsp.getChainFor("Document"), ("folder_workflow",))

        # Add a config at the root that will use the new policy
        self.portal.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()
        self.assertTrue(".wf_policy_config" in self.portal.objectIds())

        # Let's set the policy to the config
        pc = getattr(self.portal, WorkflowPolicyConfig_id)
        pc.setPolicyIn("foo_bar_policy")
        pc.setPolicyBelow("foo_bar_policy")

        self.assertEqual(
            pc.getPlacefulChainFor("Document", start_here=1), ("folder_workflow",)
        )

        self.portal.invokeFactory("Document", id="doc", text="foo bar baz")

        # The chain should be different now
        # Workflow tool should look for policy definition and return
        # the chain of the correct policy
        self.assertEqual(pw.getChainFor(self.portal.doc), ("folder_workflow",))
        # The chain for the first document should have changed now
        self.assertEqual(pw.getChainFor(self.portal.doc_before), ("folder_workflow",))

    def test_08_getChainFor(
        self,
    ):
        # Let's see what the chain is before
        pwt = self.portal_placeful_workflow
        self.assertEqual(pwt.getMaxChainLength(), 1)
        pwt.setMaxChainLength(2)
        self.assertEqual(pwt.getMaxChainLength(), 2)

    def test_09_wft_getChainFor(
        self,
    ):
        self.portal.invokeFactory("Folder", id="folder")
        self.portal.folder.invokeFactory("Document", id="document", text="foo")

        # Check default
        wft = self.portal.portal_workflow
        chain = wft.getChainFor("Document")
        self.assertEqual(tuple(chain), ("simple_publication_workflow",))

        # Check global chain
        wft.setChainForPortalTypes(("Document",), ("wf",))
        chain = wft.getChainFor("Document")
        self.assertEqual(tuple(chain), ("wf",))

        # Check global chain, using object
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ("wf",))

        # Remove global chain
        wft.setChainForPortalTypes(("Document",), ())
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ())

    def test_10_wft_getChainFor_placeful(self):
        wft = self.portal.portal_workflow
        self.portal.invokeFactory("Folder", id="folder")
        self.portal.folder.invokeFactory("Document", id="document")
        self.portal.folder.invokeFactory("Folder", id="folder2")
        self.portal.folder.folder2.invokeFactory("Document", id="document2")

        # Create a policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById("foo_bar_policy")
        gsp1.setChainForPortalTypes(["Document"], ["folder_workflow"])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)
        pc.setPolicyIn("foo_bar_policy")
        pc.setPolicyBelow("foo_bar_policy")

        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ("folder_workflow",))

        # Create a different policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy2", "default_workflow_policy (Simple Policy)"
        )

        # And redefine the chain for Document
        gsp2 = pwt.getWorkflowPolicyById("foo_bar_policy2")
        gsp2.setChainForPortalTypes(["Document"], ["plone_workflow"])

        # Add a different config in the second folder
        self.portal.folder.folder2.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()
        pc = getattr(self.portal.folder.folder2, WorkflowPolicyConfig_id)
        pc.setPolicyIn("foo_bar_policy2")
        pc.setPolicyBelow("foo_bar_policy2")

        # Check inheritance order
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ("plone_workflow",))

        # Check empty chain
        gsp2.setChain("Document", ())
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ())

        # Check default
        wft.setDefaultChain("folder_workflow")
        gsp2.setChainForPortalTypes(("Document",), ("(Default)",))
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ("folder_workflow",))

    def test_11_In_and_Below(self):
        """In and below"""
        wft = self.portal.portal_workflow
        self.portal.invokeFactory("Folder", id="folder")
        self.portal.folder.invokeFactory("Document", id="document")
        self.portal.folder.invokeFactory("Folder", id="folder2")
        self.portal.folder.folder2.invokeFactory("Document", id="document2")
        self.portal.folder.invokeFactory("Folder", id="folder3")
        self.portal.folder.folder3.invokeFactory("Document", id="document3")

        # Create a policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById("foo_bar_policy")
        gsp1.setChainForPortalTypes(["Document"], ["plone_workflow"])
        gsp1.setChainForPortalTypes(["Folder"], ["plone_workflow"])

        # Create a policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy2", "default_workflow_policy (Simple Policy)"
        )

        # And redefine the chain for Document
        gsp2 = pwt.getWorkflowPolicyById("foo_bar_policy2")
        gsp2.setChainForPortalTypes(["Document"], ["folder_workflow"])
        gsp2.setChainForPortalTypes(["Folder"], ["folder_workflow"])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)

        # In folder 1, we want to have plone_workflow
        # We set PolicyIn to the first policy in folder 1
        pc.setPolicyIn("foo_bar_policy")

        # In folder 2, we want to have folder_workflow
        # We set PolicyBelow to the second policy in folder 2
        pc.setPolicyBelow("foo_bar_policy2")

        # A document in folder 2 should have folder_workflow
        chain = wft.getChainFor(self.portal.folder.folder2.document2)
        self.assertEqual(tuple(chain), ("folder_workflow",))

        # Folder 2 should have folder_workflow
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ("folder_workflow",))

        # A document in folder 1 should have folder_workflow
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ("folder_workflow",))

        # Folder 1 should have plone_workflow
        chain = wft.getChainFor(self.portal.folder)
        self.assertEqual(tuple(chain), ("plone_workflow",))

    def test_11_copy_paste(self):
        """Test security after a copy/paste"""
        wft = self.portal.portal_workflow
        self.portal.invokeFactory("Document", id="document")
        self.portal.invokeFactory("Folder", id="folder")

        # Create a policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById("foo_bar_policy")
        gsp1.setChainForPortalTypes(["Document"], ["folder_workflow"])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)

        # In folder, we want to have folder_workflow
        # We set PolicyIn to the first policy in folder
        pc.setPolicyIn("foo_bar_policy")

        cb = self.portal.manage_copyObjects(["document"])
        self.portal.folder.manage_pasteObjects(cb_copy_data=cb)

        # A document in plone root should have simple_publication_workflow
        chain = wft.getChainFor(self.portal.document)
        self.assertEqual(tuple(chain), ("simple_publication_workflow",))

        # Folder should have simple_publication_workflow
        chain = wft.getChainFor(self.portal.folder)
        self.assertEqual(tuple(chain), ("simple_publication_workflow",))

        # A document in folder should have folder_workflow
        chain = wft.getChainFor(self.portal.folder.document)
        self.assertEqual(tuple(chain), ("folder_workflow",))

    def test_11_getWorkflowPolicyById_edge_cases(self):
        pwt = self.portal_placeful_workflow
        self.assertEqual(pwt.getWorkflowPolicyById("dummy"), None)

    def test_12_getWorkflowPolicyById_edge_cases(self):
        pwt = self.portal_placeful_workflow
        self.assertEqual(pwt.getWorkflowPolicyById(None), None)

    def test_13_getWorkflowPolicyConfig(self):
        pwt = self.portal_placeful_workflow
        config = pwt.getWorkflowPolicyConfig(self.portal)
        self.assertEqual(config, None)

    def test_14_getWorkflowPolicyConfig(self):
        self.portal.invokeFactory("Folder", id="folder")
        self.portal.folder.invokeFactory("Document", id="document")
        self.portal.folder.invokeFactory("Folder", id="folder2")
        self.portal.folder.folder2.invokeFactory("Document", id="document2")

        # Create a policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )
        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById("foo_bar_policy")
        gsp1.setChainForPortalTypes(["Document"], ["folder_workflow"])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)
        pc.setPolicyIn("foo_bar_policy")
        pc.setPolicyBelow("foo_bar_policy")

        # You should only be able to get a config in the folder itself
        config = pwt.getWorkflowPolicyConfig(self.portal.folder)
        self.assertTrue(config is not None)

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
        wft = self.portal.portal_workflow
        self.portal.invokeFactory("Folder", id="folder")
        self.portal.folder.invokeFactory("Document", id="document")
        self.portal.invokeFactory("Folder", id="folder2")
        self.portal.folder2.invokeFactory("Document", id="document2")

        # Create a policy
        pwt = self.portal_placeful_workflow
        pwt.manage_addWorkflowPolicy(
            "foo_bar_policy", "default_workflow_policy (Simple Policy)"
        )

        # And redefine the chain for Document
        gsp1 = pwt.getWorkflowPolicyById("foo_bar_policy")
        gsp1.setChainForPortalTypes(["Document"], ["folder_workflow"])

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        pc = getattr(self.portal.folder, WorkflowPolicyConfig_id)
        pc.setPolicyIn("foo_bar_policy")
        pc.setPolicyBelow("foo_bar_policy")

        chain = wft.getChainFor(self.portal.folder2.document2)
        self.assertEqual(tuple(chain), ("simple_publication_workflow",))

        # What if we acquired the doc from the wrong place
        wrapped_doc = self.portal.folder2.document2.__of__(self.portal.folder)
        chain = wft.getChainFor(wrapped_doc)
        self.assertEqual(tuple(chain), ("simple_publication_workflow",))

        # What if we acquired the container from the wrong place
        wrapped_doc = self.portal.folder2.__of__(self.portal.folder).document2
        chain = wft.getChainFor(wrapped_doc)
        self.assertEqual(tuple(chain), ("simple_publication_workflow",))

    def test_16_getWorklists(self):
        """Verify if worklists are always accessible with a policy"""
        wf_tool = self.portal.portal_workflow
        placeful_tool = self.portal_placeful_workflow

        self.portal.invokeFactory("Folder", id="folder")
        self.portal.folder.invokeFactory("Document", id="document")

        # Create a policy
        placeful_tool.manage_addWorkflowPolicy(
            "foo_bar_policy",
            "default_workflow_policy (Simple Policy)",
            "portal_workflow",
        )
        # And redefine the chain for Document in portal_workflow
        wf_tool.setChainForPortalTypes(["Document"], ())

        # Add a config to the folder using the policy
        self.portal.folder.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()

        # Set the policy for the config
        config = getattr(self.portal.folder, WorkflowPolicyConfig_id)
        config.setPolicyBelow("foo_bar_policy")

        # we make the document pending
        document = self.portal.folder.document
        wf_tool.doActionFor(document, "submit", comment="unittest transition")

        keys = list(wf_tool.getWorklists().keys())
        if "comment_review_workflow" in keys:
            # This test needs to work on both 4.0 and 4.1
            keys.remove("comment_review_workflow")
        expected = (
            "folder_workflow",
            "intranet_folder_workflow",
            "intranet_workflow",
            "one_state_workflow",
            "plone_workflow",
            "simple_publication_workflow",
        )
        installer = get_installer(self.portal)
        if installer.is_product_installed("plone.app.discussion"):
            expected += ("comment_one_state_workflow",)
        self.assertEqual(
            sorted(tuple(keys)),
            sorted(expected),
        )
        self.assertEqual(tuple(wf_tool.getWorklistsResults()), (document,))

        logout()
