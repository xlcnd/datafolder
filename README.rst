'configuration by convention'

MANIFEST.in
README.rst
setup.py
mypkg
    |_ __init__.py
    |_ mypkg.conf
    |_ mypkg.db
    |_ ...

    

.. code-block:: python

    ...
    import sys
    import pkg_resources
    from setuptools import setup
    from installtools import Installer
    ...

    # write the name of the package (in this case 'mypkg'!)
    MYPKG = 'mypkg'

    # mypkg supports these python versions
    SUPPORT = ((2, 6), (2, 7), (3, 3), (3, 4))

    # list of data files in mypkg (just the names)
    MYDATAFILES = ['mypkg.conf', 'mypkg.db']


    # (many people get confused with the next step...)


    # now, tell were these files are in your package
    MYRESOURCES = []
    for datafile in MYDAFILES:
        MYRESOURCES.append(pkg_resources.resource_filename(MYPKG, datafile))
    
    # now, create the installer
    installer = Installer(sys.argv)

    # use installer to check supported python versions
    installer.support(SUPPORT)

    # create the data folder and tell setup to put there the data files
    DATAPATH = installer.data_path(MYPKG)
    data_files = [(DATAPATH, MYRESOURCES)]

    # setup can now do his thing...
    setup(
        name=MYPKG',
        ...
        data_files=data_files,
        install_requires=["installtools>=0.0.1"],  # <-- IMPORTANT
        ...
    )

    # but we are NOT READY, in some cases the data files 
    # don't have the appropriate permissions,
    # let us fix that...  
    installer.pos_setup(MYDATAFILES)

