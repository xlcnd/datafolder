``datafolder`` is a small python library that makes it very easy to **install**
the `data files` of your package and **access** them later.

If you want to install some data files (conf, sqlite, csv, ...) to a place like
the user's home directory and find it difficult with ``setuptools``, then here
is some help.


   **WARNING**: this is alpha software!


First, let's make life easier and use some 'configuration by convention'.

I assume that (1) you have layout your project like::

    MANIFEST.in
    README.rst
    setup.py
    mypkg
        │
        ├── __init__.py
        ├── mypkg.conf
        ├── mypkg.db
        └── ...


And that (2) you want to put a folder, in the home directory of the user
(in Windows will be in %APPDATA%), with your data files (conf, csv, ...) inside.
This folder will have the name of your package (preceded with a '.' in UNIX
systems), let's say '.mypkg' and, of course, with the right permissions
(it will work with ``sudo pip install mypkg``). For virtual environements the
data folder will be put at the root of the environement.


**How to do it?**


(1) First, install the ``datafolder`` package::

    $ pip install -U datafolder


(2) Then, enter::

    $ datafolder_mkboot

It will make a file called `bootdf.py` that you **must** put in your `mypkg` directory.


(3) Then, enter::

    $ datafolder_mktpl

it will create a new file called `setup_TPL.py` that you **must** put at the root of your project.


(4) That file is a template that you have to adapt to your case:

.. code-block:: python

    import sys
    import pkg_resources

    from setuptools import setup
 
    from mypkg.bootdf import Installer                         # <-- ADAPT THIS


    # write the name of the package (in this case 'mypkg'!)
    MYPKG = 'mypkg'                                            # <-- ADAPT THIS

    # list of data files in mypkg (just the names)
    # [don't forget to include these files in MANIFEST.in!]
    MYDATAFILES = ['mypkg.conf', 'mypkg.db']                   # <-- ADAPT THIS

    # tell setup were these files are in your package
    # (I assume that they are together with the first __init__.py)
    MYRESOURCES = [pkg_resources.resource_filename(MYPKG, datafile)
                   for datafile in MYDATAFILES]

    # now, create the installer
    installer = Installer(sys.argv)

    # create the data folder and tell setup to put the data files there
    DATAPATH = installer.data_path(MYPKG)
    data_files = [(DATAPATH, MYRESOURCES)]

    # now, setup can do his thing...
    setup(
        name=MYPKG,
        packages=[MYPKG,'other_packg1','other_packg2'],        # <-- ADAPT THIS
        data_files=data_files,
        install_requires=["datafolder>=0.1.1"],
        ...                                                    # <-- ADAPT THIS
    )

    # but we are NOT READY, in some cases the data files
    # don't have the appropriate permissions,
    # let us fix that...
    installer.pos_setup(MYDATAFILES)


(5) Now, rename the file to 'setup.py'.

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
of the data folder for you and provides attributes and methods,
that make it easy to handle the files presente in the data folder.


Feedback_, please!


   **REMARK**: as you can see above, this only works if the
   install method uses ``setup.py``. Is **not** the case
   of *python wheels*!


.. _Feedback: https://github.com/xlcnd/datafolder/issues
