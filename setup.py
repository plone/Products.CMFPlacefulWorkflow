from setuptools import setup, find_packages

version = '1.5.15'

setup(name='Products.CMFPlacefulWorkflow',
      version=version,
      description="Workflow policies for CMF and Plone",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          ],
      keywords='CMF Plone Zope2 workflow',
      author='Encolpe DEGOUTE',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/Products.CMFPlacefulWorkflow',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      extras_require=dict(
          test=[
              'Products.PloneTestCase',
              'zope.testing',
          ]),
      install_requires=[
          'setuptools',
          'zope.component',
          'zope.interface',
          'zope.i18nmessageid',
          'Products.CMFCore',
          'Products.CMFPlone',
          'Products.GenericSetup>=1.8.1',
      ],
      )
