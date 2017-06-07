Ingress Report GPS Spoof User Server
================================================================================

*WIP*

Requirements
--------------------------------------------------------------------------------

System package
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

We need `python3`
and `nginx` or other similar static http server.

Python package
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You may use virtualenv.
Most of required packages listed in ``requirements.txt``.
Use the following command to install.

::

    $ pip3 install -r requirements.txt
    $ python3 manage.py migrate

Config
--------------------------------------------------------------------------------

set your nginx server with

::

    listen 7890 default_server;
    root <repo_path>/reports/static/files;

Start Server
--------------------------------------------------------------------------------

Start server
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

::

    python3 manage.py runserver 8000
