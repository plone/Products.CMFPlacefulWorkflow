from setuptools import setup, find_packages

version = '1.7.4'

setup(
    name='Products.CMFPlacefulWorkflow',
    version=version,
    description="Workflow policies for Plone",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 5.1",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='CMF Plone Zope2 workflow',
    author='Encolpe DEGOUTE',
    author_email='plone-developers@lists.sourceforge.net',
    url='https://pypi.python.org/pypi/Products.CMFPlacefulWorkflow',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        test=[
            'plone.app.testing',
            'zope.testing',
        ],
    ),
    install_requires=[
        'setuptools',
        'six',
        'zope.component',
        'zope.interface',
        'zope.i18nmessageid',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Products.GenericSetup>=1.8.3',
    ],
)
