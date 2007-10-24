from zope.testing import doctest
from Testing.ZopeTestCase import ZopeDocFileSuite

from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

from Products.CMFPlone.interfaces import IPloneSiteRoot

from CMFPlacefulWorkflowTestCase import CMFPlacefulWorkflowTestCase

class ExportImportLayer(
    CMFPlacefulWorkflowTestCase.layer):

    @classmethod
    def setUp(cls):
        profile_registry.registerProfile(
            name='exportimport', title='Test Placeful Workflow Profile',
            description=(
                "Tests the placeful workflow policy handler."),
            path='profiles/exportimport',
            product='Products.CMFPlacefulWorkflow.tests',
            profile_type=EXTENSION, for_=IPloneSiteRoot)

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass

def test_suite():
    suite = ZopeDocFileSuite(
        '../exportimport.txt',
        optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        test_class=CMFPlacefulWorkflowTestCase)
    suite.layer = ExportImportLayer
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
