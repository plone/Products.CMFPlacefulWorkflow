# CMFPlacefulWorflow
# Copyright (C)2006 Ingeniweb

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
Contributed by Jazkarta
"""

from plone.testing import layered
from Products.CMFPlacefulWorkflow.testing import (
    PRODUCTS_CMFPLACEFULWORKFLOW_FUNCTIONAL_TESTING,
)

import doctest
import unittest


OPTIONFLAGS = (
    doctest.ELLIPSIS
    | doctest.NORMALIZE_WHITESPACE
    | doctest.REPORT_UDIFF
    | doctest.REPORT_ONLY_FIRST_FAILURE
)


def test_suite():
    suite = unittest.TestSuite()
    for testfile in ["exportimport.txt", "policy_form.txt"]:
        suite.addTest(
            layered(
                doctest.DocFileSuite(testfile, optionflags=OPTIONFLAGS),
                layer=PRODUCTS_CMFPLACEFULWORKFLOW_FUNCTIONAL_TESTING,
            )
        )
    return suite
