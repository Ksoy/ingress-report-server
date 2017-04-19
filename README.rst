Ingress Report GPS Spoof User Server
================================================================================

*WIP*

Requirements
--------------------------------------------------------------------------------

System package
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

We need `python3`, `nodejs`, `npm`, `webpack`

Python package
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You may use virtualenv.
Most of required packages listed in ``requirements.txt``.
Use the following command to install.

::

    $ pip3 install -r requirements.txt
    $ python3 manage.py migrate

NPM package
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

::

    $ cd reports
    $ npm install
    $ npm install -g webpack
    $ webpack


Config
--------------------------------------------------------------------------------

Todo

Start Server
--------------------------------------------------------------------------------

Start server
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

::

    python3 manage.py runserver 8000
