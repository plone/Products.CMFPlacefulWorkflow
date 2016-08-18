Changelog
=========

1.7.1 (2016-08-18)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


1.7.0 (2016-05-26)
------------------

New:

- Added ``uninstall`` profile instead of old external method.  [maurits]

- Removed ``actionicons.xml`` because this is handled in ``controlpanel.xml``.  [maurits]

- Replaced ``placeful_marker`` import step with a ``post_handler``.  [maurits]


1.6.5 (2015-11-28)
------------------

Fixes:

- Updated Site Setup link in all control panels.
  Fixes https://github.com/plone/Products.CMFPlone/issues/1255
  [davilima6]


1.6.4 (2015-09-27)
------------------

- Fix test after new default dependecy-strategy for GenericSetup.
  [pbauer]


1.6.3 (2015-09-20)
------------------

- Allow unicode as workflow-policy-name
  [pbauer]


1.6.2 (2015-09-07)
------------------

- Added upgrade step to apply our full profile.  This is meant mostly
  for upgrades from ancient versions that had no profile yet or had a
  profile without a metadata.xml.  In that case the quick installer
  would complain that the old profile version was unknown and there
  was no upgrade.
  [maurits]


1.6.1 (2015-03-13)
------------------

- Ported tests to plone.app.testing
  [tomgross]

- PEP8 and frosted cleanup
  [tomgross]

- Major cleanup of old stuff
  [tomgross]


1.6.0 (2014-04-16)
------------------

- Plone 5 fixes
  [vangheem]


1.5.10 (2013-12-07)
-------------------

- Move dependency on Products.PloneTestCase to test extra and thus removing
  implicit hard dependency on Products.ATContentTypes.
  [thet]

- Fix policy_form test failures for Plone 5.
  [timo]


1.5.9 (2012-12-15)
------------------

- Fixed handling of "update security" option.
  [ericof]


1.5.8 (2012-10-16)
------------------

- Fixed updating Role Mappings only in current folder.
  [kroman0]

- Added 'CMFPlacefulWorkflow: Manage workflow policies' permission.
  ManageWorkflowPolicies is no longer 'Manage portal', it's now assigned to
  'CMFPlacefulWorkflow: Manage workflow policies'.
  [alecghica]

- Fixed add workflow policy template (via ZMI).
  [alecghica]

- Fixed descriptions under placeful_workflow_configuration.pt for sections
  "For this folder" and "Below this folder".
  [alecghica]

- Added "update security" as an option field on local configuration management
  form, as in most cases updating catalog role mappings can be a very long
  operation and is better to be made as a separate upgrade step.
  [alecghica]

1.5.7 (2012-05-25)
------------------

- Fixed a few test failures in combination with five.pt.
  [maurits]

1.5.6 (2011-11-24)
------------------

- Fix profiles description to be translated.
  [vincentfretin]

- Fix failing test.
  [davisagli]

1.5.5 - 2011-06-15
------------------

- Fix required value untested #9833
  [encolpe]

1.5.4 - 2011-03-31
------------------

- Fix test to work with both 4.0 and 4.1.
  [elro]

- Create base profile with no dependencies on the default Plone types to allow use in an
  archetype free dexterity environment
  [anthonyg]

1.5.3 - 2011-02-04
------------------

- Fix failing test. The 'comment_review_workflow' from plone.app.discussion is
  now part of the core.
  [timo]


1.5.2 - 2011-01-03
------------------

- Depend on ``Products.CMFPlone`` instead of ``Plone``.
  [elro]

- Updated the placeful_workflow import step to depends on typeinfo,
  as we need to make sure all types are available when importing the
  local policies.
  [deo]


1.5.1 - 2010-10-27
------------------

- Fixed chameleon incompatibility in `manage_workflow_policy_config.zpt`.
  Renamed `select_workflows.zpt` to `select_workflows.dtml` and
  `select_workflows.zpt` to `select_workflows.dtml`.
  [swampmonkey]

1.5 - 2010-07-18
----------------

- No changes.

1.5b5 - 2010-06-13
------------------

- Avoid deprecation warnings under Zope 2.13.
  [hannosch]

- Avoid using the deprecated five:implements directive.
  [hannosch]

1.5b4 - 2010-06-03
------------------

- Remove references to Large Plone Folder from the included workflow policies.
  [davisagli]

1.5b3 - 2010-05-01
------------------

- Use i18n_domain=cmfplacefulworkflow in profiles.zcml to be able to
  translate the title and description of the profile. This refs
  http://dev.plone.org/plone/ticket/9864
  [vincentfretin]

1.5b1 - 2009-12-27
------------------

- Avoid showing the content type icons in the workflow mapping screens.
  [hannosch]

- Small code cleanup and removal of unused imports.
  [hannosch]

1.5a2 - 2009-11-18
------------------

- Make CMFPlacefulWorkflow tool an ImmutableId object, but not a UniqueObject.
  The UniqueObject base class specifies that it is impossible to have any
  other object with the same id (portal_placeful_workflow). This was breaking
  in-ZODB GenericSetup snapshots, because the GenericSetup sub-folder for
  placeful workflow policies happens to also be called
  portal_placeful_workflow. Plone has a checkId script which disallows
  shadowing tools anyway, so the UniqueObject base class is a nicety rather
  than a necessity.
  [optilude]

1.5a1 - 2009-11-18
------------------

- Removed createSnapshot() call from exportimport.txt test. It wasn't doing
  anything useful, and caused a distracting test failure not related to
  CMFPlacefulWorkflow.

- Fix #9359: CMFPlacefulWorkflow defines __implements__ with zope3 interface.
  [encolpe]

- Remove use of the deprecated document_byline macro in the placeful
  workflow configuration template.
  [davisagli]

- Register configlet icon using icon_expr for forwards-compatibility
  with Plone 4.
  [davisagli]

- Copied safeEditProperty function from CMFPlone's migrations package,
  as that is being removed.
  [davisagli]

- Change imports from Globals to use canonical locations, for compatibility
  with Zope 2.12.
  [davisagli]

- Define wtool inside the prefs_workflow_policy_mapping template.
  [hannosch]

- Removed settings of the portal_skins tool itself from skins.xml.
  Specifically, allow_any was set to False, which bit me.
  [maurits]

- Made worflow policies translatable in prefs_workflow_localpolicies_form.
  [vincentfretin]

1.4.2 - 2009-03-05
------------------

- The `Cancel` button on the local workflow configuration screen was saving
  data as much as the `Save` button. Now it actually cancels the operation.
  [hannosch]

- Made sure you cannot set a workflow configuration on a non-folderish item
  in the site root. The actual configuration would end up on the site root.
  [hannosch]

- Change the local workflow configuration screen to not be shown for the
  site root, even if you accidentally type in the wrong URL.
  [hannosch]

1.4.1 (2009-01-17)
------------------

- Declare package dependencies and fixed deprecation warnings for use
  of Globals.
  [hannosch]

- Copied safeEditProperty from CMFPlone.migration_util to avoid a dependency.
  [hannosch]


1.4.0 (2008-11-05)
------------------

- Port evolutions from the 1.3 maintenance branch (old style product).
  [encolpe]

- Fixed bad version in metadata.xml (again)
  [encolpe]

- Removed Favorite content type.
  [hannosch]

- Fixed "ValueError: 'acquisition' is not a workflow ID" in
  prefs_workflow_policy_mapping.  Fix prepared by jhackel.  Fixes
  http://dev.plone.org/plone/ticket/8101
  [maurits]


1.3.2 (2008-06-30)
------------------

- Fixed bad metadata.xml.
  [encolpe]

- Fixed incorrect variable name in exception message.
  [davisagli]
