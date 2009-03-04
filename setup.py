from setuptools import setup, find_packages

version = '1.4.1'

setup(name='Products.CMFPlacefulWorkflow',
      version=version,
      description="Workflow policies for CMF and Plone",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES").read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='CMF Plone Zope2 workflow',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='http://svn.plone.org/svn/collective/Products.CMFPlacefulWorkflow',
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
