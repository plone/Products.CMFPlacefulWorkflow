from setuptools import setup, find_packages

version = '1.5b5'

setup(name='Products.CMFPlacefulWorkflow',
      version=version,
      description="Workflow policies for CMF and Plone",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
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
      install_requires=[
          'setuptools',
          'zope.component',
          'zope.interface',
          'zope.i18nmessageid',
          'Products.CMFCore',
          'Plone',
          'Products.GenericSetup',
          'zope.testing',
          'Products.PloneTestCase',
      ],
      )
