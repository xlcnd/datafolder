``datafolder`` is a small python library that makes it very easy to **install**
the `data files` of your package and **access** them later.

If you want to install some data files (conf, sqlite, csv, ...) to a place like
the user's home directory and find it difficult with ``setuptools``, then here
is some help.


   **WARNING**: this is pre-alpha software!!!


First, let's make life easier and use some 'configuration by convention'.

I assume that (1) you have layout your project like::

    MANIFEST.in
    README.rst
    setup.py
    mypkg
        |_ __init__.py
        |_ mypkg.conf
        |_ mypkg.db
        |_ ...


And that (2) you want to put a folder, in the home directory of the user
(in Windows will be in %APPDATA%), with your data files (conf, csv, ...) inside.
This folder will have the name of your package (preceded with a '.' in UNIX
systems), let's say '.mypkg' and, of course, with the right permissions
(it will work with ``sudo pip install mypkg``). For virtual environements the
data folder will be put at the root of the environement.


**How to do it?**



Use the following template for your ``setup.py``
(**just enter at a terminal** ``datafolder_mktpl`` if you already installed ``datafolder``):

.. code-block:: python

    import sys
    import pkg_resources
    from setuptools import setup
    from datafolder import Installer
    from datafolder import DataFolderException


    # write the name of the package (in this case 'mypkg'!)
    MYPKG = 'mypkg'                                             #<-- ADAPT THIS

    # mypkg supports these python versions
    SUPPORT = ((2, 6), (2, 7), (3, 1), (3, 2), (3, 3), (3, 4))  #<-- ADAPT THIS

    # list of data files in mypkg (just the names)
    MYDATAFILES = ['mypkg.conf', 'mypkg.db']                    #<-- ADAPT THIS


    # (many people get confused with the next step...)


    # tell setup were these files are in your package
    # (I assume that they are together with the first __init__.py)
    MYRESOURCES = [pkg_resources.resource_filename(MYPKG, datafile)
                   for datafile in MYDATAFILES]

    # now, create the installer
    installer = Installer(sys.argv)

    # use the installer to check supported python versions
    installer.support(SUPPORT)

    # create the data folder and tell setup to put the data files there
    try:
        DATAPATH = installer.data_path(MYPKG)
    except DataFolderException:
        # here you can handle any exception raised with the creation
        # of the data folder... e.g. abort installation
        print('Abort installation')
        raise
    data_files = [(DATAPATH, MYRESOURCES)]

    # now, setup can do his thing...
    setup(
        name=MYPKG,
        data_files=data_files,
        install_requires=["datafolder>=0.0.6"],                 # <-- IMPORTANT
        ...                                                     # <-- ADAPT THIS
    )

    # but we are NOT READY, in some cases the data files
    # don't have the appropriate permissions,
    # let us fix that...
    installer.pos_setup(MYDATAFILES)



**And that is all!**

"But, **I have the reverse problem**, how can I access these files in my code?"
I heard you say.

Very easy, in your code:

.. code-block:: python


    from datafolder import DataFolder

    data = DataFolder('mypkg')

    # now you can get the full path of each data file, e.g.
    conffile = data.files['mypkg.conf']

    # do your thing... (read, write, ...)


For your convinience, the `DataFolder` class *discovers* the location
of the data folder for you and provides attributes and methods
that make it easy to handle the files presente in the data folder.


Feedback_, please!


.. _Feedback: https://github.com/xlcnd/datafolder/issues
