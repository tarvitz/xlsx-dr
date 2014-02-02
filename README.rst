XLSX dirty reader
=================
.. contents:: :local:

Installation
~~~~~~~~~~~~
For general installation you would probably need virtual environment with pip
installed:

.. code-block:: bash

   user@localhost$ virtualenv --no-site-packagmes venv
   user@localhost$ source ve/bin/activate
   user@localhost$ pip install -r requirements/base.html

Dependencies
------------
* lxml-3.3.0
* openpyxl-1.8.2 +
* sphinx (for docs)


Tests
~~~~~
You could run tests via `python -m unittest module` or via `run_tests.sh` script

.. code-block:: bash

   user@localhost$ ./run_tests.sh tests.XlsxReader


Usage
~~~~~
You can parse Xlsx (MS Excel 2007 format) files and get data in standard python
dictionary format or json (simplejson required)

.. code-block:: python

    from xlsx import XlsxReader
    reader = XlsxReader('file.xlsx')
    data = reader.get_data(sheet_name='Sheet1')
    img_data = reader.get_images()

that's all folks
