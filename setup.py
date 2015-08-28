from setuptools import setup, find_packages

version = '1.5.11.dev0'

setup(name='Products.CMFPlacefulWorkflow',
      version=version,
      description="Workflow policies for CMF and Plone",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
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
          'Products.GenericSetup',
      ],
      )
