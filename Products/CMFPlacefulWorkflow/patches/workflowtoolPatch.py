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
Patch for Plone workflow tool getChainFor method

This code stay here for historical reasons: ** DO NOT REMOVE IT **
"""
__version__ = "$Revision$"
# $Source: /cvsroot/ingeniweb/CMFPlacefulWorkflow/patches/workflowtoolPatch.py,v $
# $Id$
__docformat__ = 'restructuredtext'

from Products.CMFPlone.WorkflowTool import WorkflowTool
from Products.CMFPlacefulWorkflow.adapter import PlacefulWorkflowChain

def getPlacefulChainFor(self, ob):
    """Just use the adapter directly"""
    return PlacefulWorkflowChain(ob, self)

# don't lose the docstrings
getPlacefulChainFor.__doc__ = '\n'.join((WorkflowTool.getChainFor.__doc__,
                                         PlacefulWorkflowChain.__doc__))
WorkflowTool.getChainFor = getPlacefulChainFor
