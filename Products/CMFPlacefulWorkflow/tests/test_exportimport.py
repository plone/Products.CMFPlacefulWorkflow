# -*- coding: utf-8 -*-
## CMFPlacefulWorflow
## Copyright (C)2006 Ingeniweb

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
Contributed by Jazkarta
"""
__docformat__ = 'restructuredtext'

import doctest

from Products.CMFCore.interfaces import ISiteRoot
from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry

from CMFPlacefulWorkflowTestCase import CMFPlacefulWorkflowTestCase
from plone.testing import layererd

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_UDIFF)

class ExportImportLayer(PloneTestCaseFixture):

    def setUpZope(self, app, configurationContext):
        super(ExportImportLayer, self).setUpZope()
        profile_registry.registerProfile(
            name='exportimport', title='Test Placeful Workflow Profile',
            description=(
                "Tests the placeful workflow policy handler."),
            path='profiles/exportimport',
            product='Products.CMFPlacefulWorkflow.tests',
            profile_type=EXTENSION, for_=ISiteRoot)

EXPORT_IMPORT_FIXTURE = ExportImportLayer()
EXPORT_IMPORT_LAYER = FunctionalTesting(bases=(EXPORT_IMPORT_FIXTURE,),
        name='WorkflowTestCase:Functional')

def test_suite():
    suite = layererd(doctest.DocFileSuite(
        'exportimport.txt',
        optionflags=OPTIONFLAGS,
        ), layer=EXPORT_IMPORT_LAYER)
    return suite
