from setuptools import find_packages
from setuptools import setup


version = "3.0.1"


setup(
    name="Products.CMFPlacefulWorkflow",
    version=version,
    description="Workflow policies for Plone",
    # Note: long_description is in setup.cfg
    # to avoid needing workarounds for UnicodeDecodeErrors.
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="CMF Plone Zope2 workflow",
    author="Encolpe DEGOUTE",
    author_email="plone-developers@lists.sourceforge.net",
    url="https://github.com/plone/Products.CMFPlacefulWorkflow",
    license="GPL",
    packages=find_packages(),
    namespace_packages=["Products"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    extras_require=dict(
        test=["plone.app.testing", "zope.testing"],
    ),
    install_requires=[
        "plone.base",
        "Products.CMFPlone",
        "setuptools",
    ],
)
