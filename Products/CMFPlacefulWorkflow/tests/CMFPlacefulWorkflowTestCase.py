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
CMFPlacefulWorkflow TestCase module
"""
__version__ = "$Revision$"
# $Source: /cvsroot/ingeniweb/CMFPlacefulWorkflow/tests/CMFPlacefulWorkflowTestCase.py,v $
# $Id$
__docformat__ = 'restructuredtext'

# Python imports
import os
import time
import Globals

# Zope imports
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base

# CMF imports
from Products.CMFCore.utils import getToolByName

# Plone imports
from Products.PloneTestCase import PloneTestCase

# Products imports
from Products.Archetypes.tests import ArchetypesTestCase
from Products.ATContentTypes.Extensions.Install import install as installATCT
from Products.ATContentTypes.Extensions.toolbox import isSwitchedToATCT


class CMFPlacefulWorkflowTestCase(PloneTestCase.PloneTestCase):

    # Globals
    portal_name = 'portal'
    portal_owner = 'portal_owner'
    user_name = PloneTestCase.default_user
    user_password = PloneTestCase.default_password

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

    def beforeTearDown(self):
        # logout
        noSecurityManager()
    
    def loginAsPortalMember(self):
        '''Use if you need to manipulate site as a member.'''
        self._setupUser()
        self.mtool.createMemberarea(self.user_name)
        member = self.mtool.getMemberById(self.user_name)
        member.setMemberProperties({'fullname': self.user_name.capitalize(), 'email': 'test@example.com',})
        self.login()

    def loginAsPortalOwner(self):
        '''Use if you need to manipulate site as a manager.'''
        uf = self.app.acl_users
        user = uf.getUserById(self.portal_owner).__of__(uf)
        newSecurityManager(None, user)

    def getPermissionsOfRole(self, role):
        perms = self.portal.permissionsOfRole(role)
        return [p['name'] for p in perms if p['selected']]

def setupCMFPlacefulWorkflow(app, id=ArchetypesTestCase.portal_name, quiet=0):
    get_transaction().begin()
    _start = time.time()
    portal = app[id]
    
    if not quiet: ZopeTestCase._print('Installing CMFPlacefulWorkflowSite ... ')

    # Login as manager
    user = app.acl_users.getUserById('portal_owner').__of__(app.acl_users)
    newSecurityManager(None, user)
    qi_tool = getToolByName(portal, 'portal_quickinstaller', None)

    ## Add ATCT
    #if hasattr(aq_base(portal), 'switchCMF2ATCT'):
        #ZopeTestCase._print('ATCT already installed ... ')
    #else:
        #qi_tool.installProduct('ATContentTypes')
        #get_transaction().commit(1)

    #if not isSwitchedToATCT(portal):
        ## Switch to ATCT
        #ZopeTestCase._print('switching to ATCT mode ... ')
        #portal.switchCMF2ATCT()
        #get_transaction().commit(1)

    # Log out
    noSecurityManager()
    get_transaction().commit()
    if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

# Install CMFPlacefulWorkflow
ZopeTestCase.installProduct('MimetypesRegistry')
ZopeTestCase.installProduct('PythonScripts')
ZopeTestCase.installProduct('PortalTransforms')
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('ATContentTypes')
ZopeTestCase.installProduct('PloneInstallation')
ZopeTestCase.installProduct('CMFPlacefulWorkflow')

# Setup Plone site
PloneTestCase.setupPloneSite(products=[
    'Archetypes',
    'ATContentTypes',
    'CMFPlacefulWorkflow',
    ])

app = ZopeTestCase.app()
setupCMFPlacefulWorkflow(app)
ZopeTestCase.close(app)
