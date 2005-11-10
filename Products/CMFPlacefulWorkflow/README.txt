Dependencies
============

Required Products
------------------

* Plone 2.0.5 or more

* Plone 2.1 is supported.

Installation
============
  
Installing CMFPlacefulWorkflow
------------------------------
    
* Unpack it into your Zope Products Folder
* Restart Zope
* Use portal_quickinstaller to install the CMFPlacefulworkflow in ZMI (or use plone_setup in pmi)
* Now you can define and apply a workflow policies through the Plone Interface.
    (Adding a workflow policies through the ZMI works as well).

Overview
========

  CMFPlacefulWorkflow: A Plone product that allows you to define workflow
  policies that define content type to workflow mappings that can be applied
  in any sub-folder of your Plone site.

  When you access the root of your site, you will see a new action in
  the workflow state drop-down menu called "policy". Click on the 
  "policy" link. 

  The next page will let you add a policy to your folder by clicking
  on the "Add Workflow policy" link. Click on "Add Workflow policy".

  Now you have a workflow policy in your site, and you can set the
  workflow policies for this folder and below.

  We didn't add workflow policies yet, so you don't have the choice
  between different workflow policies, but the default workflow
  policy will be taken both for the folder and below.

  Let's define a new workflow policy. Access the "Plone Setup" and
  click on "Placeful Workflow" in the "Add-on Product Configuration"
  section.

  Enter the name "my_policy" in the "New policy" field, and click on
  "add".

  Now you have a new policy for which you can enter the title "My policy"
  and the description "This is my policy". Change the workflow for the
  content type "Folder" from "folder_workflow" to plone_workflow", and click
  on "Save". Now all your content types should use the "plone_workflow".

  Now we want to test the new workflow policy for "Folders" at the root
  of our site. At the root of our site, select the "policy" link in the
  workflow state drop-down menu.

  Select "My policy" for "In this Folder" and "Below this Folder" and
  click on "save". 

  Let's add a Folder to see whether the new workflow policy is taken 
  into account. Go to the root of your site and select "Folder" from 
  the "add new item" drop-down list. Enter the id "myfolder", the title
  "My folder" and the description "This is my folder", and click on
  "save". 

  Now, when you access the "state" drop-down list, you will see that
  you have the possibility to "submit" the folder. The submit transition
  only exists in the "plone_workflow", and is absent from the "folder_workflow",
  which proves that the workflow policy we have chosen is used for
  the "Folder" content type.

  Let's go one step further and add a new folder inside of "My folder".
  After having added the new folder, you should also find the "submit"
  transition at your disposition.

  Now it would be interesting to change the workflow policy setting in
  the Plone site. Let's first change the workflow policy for "Below this
  Folder" to "Default Policy". You will find that the second folder does
  not more have the "submit" transition.

  You can add an additional workflow policy in the first folder, which
  assigns the "My policy" for "In this Folder", so the second folder
  will once again have the "submit" transition.

Additional tools
----------------

  Placeful Workflow tool

    The Placeful Workflow tool (portal_placeful_workflow) is installed by
    the installer. It provides a few configuration options so that you use
    to create you workflow policies through the ZMI.

PLIP
----

  http://plone.org/Members/maikroeder/52

  Our goal is to be able to say that in a given folder, a different
  workflow (or workflow chain) should be used for certain content types. 

  The mapping of content type to workflow chain can be managed in 
  the workflow tool, but there is no way to associate a document
  dynamically to a workflow chain in a given folder.

  Have a look at the INSTALL.txt for information on how to 
  install the product.
