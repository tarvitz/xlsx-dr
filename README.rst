XLSX dirty reader
=================

**!!!NOTE!!!*** That's dirty reader, hope you don't even try to use it. Please check other repositories and tools to get acquainted how to extract pictures from cells.

.. contents:: :local:

Installation
~~~~~~~~~~~~
For general installation you would probably need virtual environment with pip
installed:

.. code-block:: bash

   user@localhost$ virtualenv --no-site-packages venv
   user@localhost$ source venv/bin/activate
   user@localhost$ pip install -r requirements/base.txt

*optional*

.. code-block:: bash

   user@localhost$ pip install -r requirements/docs.txt


Dependencies
------------
* lxml-3.3.0+
* openpyxl-1.8.2 +
* sphinx (for docs)


Tests
~~~~~
Simply run

.. code-block:: bash

    user@localhost$ python setup.py test


Or you could run tests via `python -m unittest module` or via `run_tests.sh` script

.. code-block:: bash

   user@localhost$ ./run_tests.sh tests.XlsxReader

Using `tox <https://pypi.python.org/pypi/tox>`_ you can achieve fast and simple
test runs.

.. code-block:: bash

    user@localhost$ tox

Usage
~~~~~
You can parse Xlsx (MS Excel 2007 format) files and get data in standard python
dictionary format or json (simplejson required)

.. code-block:: python

    from xlsx.reader import XlsxReader
    reader = XlsxReader('file.xlsx')
    data = reader.get_data(sheet_name='Sheet1')
    img_data = reader.get_images()

that's all folks
