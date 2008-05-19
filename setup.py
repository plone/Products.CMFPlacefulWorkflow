from setuptools import setup, find_packages
import os

version = '1.3.1'

setup(name='Products.CMFPlacefulWorkflow',
      version=version,
      description="Workflow policies for CMF and Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
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
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
