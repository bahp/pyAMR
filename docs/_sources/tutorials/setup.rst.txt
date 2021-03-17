Tutorial
========

Creating the virtual environment
--------------------------------

A virtual environment is a tool that helps to keep dependencies required by
different projects separate by creating isolated python virtual environments
for them. This is one of the most important tools that Python developers use.

In recent versions of python (>3) we can use venv. If you have various
versions of python you might need to use python3 or py instead.

.. code::

  python -m pip install venv           # Install venv
  python -m venv <environment-name>    # Create environment

Otherwise, using standard virtualenv (linux-based systems)

.. code::

  which python                                    # where is python
  pip install virtualenv                          # Install virtualenv
  virtualenv -p <python-path> <environment-name>  # create virtualenv

Let's activate the environment

.. code::

  source <environment-name>/bin/activate          # activate environment

To deactivate the environment just type

.. code::

  deactivate                                      # deactivate environment


.. warning:: Ths is slightly different on Windows systems. It is also possible
   to configure the virtual environment using the python IDE PyCharm. Students
   can get a free licence.

Creating repository from template
----------------------------------

Repository template: https://github.com/bahp/fyp-pypkg-template

Open the previous url and create your own repository using it as
a template. For this, click on the green "Use as a template" button.
Please use the following conventions:

    - name: ``fyp<year>-<imperial_username>`` # eg. fyp2020-bahp
    - include a brief description of the project
    - keep it ``public`` to be able to use github pages.
    - tick ``include all branches``.

Once you have created the repository, it should appear on your repository list.
Note that the url to clone the repository is under the green "code" button and
it should look like https://github.com/bahp/fyp2020-bahp.git but replacing bahp
with your github username and fyp2020-bahp with your repository name.

Let's double check that Github Pages is enabled. For this, click 'Settings',
scroll down to the GitHub Pages section and select: (i) gh-pages as source branch
and (ii) docs as a source folder.

Set up the repository locally
-----------------------------

On your computer, open the terminal and create your repository folder:

.. code-block:: console

    $ mkdir fyp2020-bahp # fyp<yyyy>-<imperial-username>

Move inside the folder:

.. code-block:: console

    $ cd fyp2020-bahp

Clone each branch in a different folder:

.. code-block:: console

    $ git clone -b main https://github.com/bahp/fyp2020-bahp.git
    $ mv <repository_name> main
    $ git clone -b gh-pages https://github.com/bahp/fyp2020-bahp.gi
    $ mv <repository_name> gh-pages

Your repository is now ready!

The main branch contains all the source files and the gh-pages will be just used
to host the documentation in html. Brief summary of the contents below:

.. code-block:: console

    gh-pages
        |- docs
            - documentation
    main
        |- docs
            |- build
            |- source
                |- conf.py    # config - sphinx documentation
                |- index.rst  # index - sphinx documentation
            make.bat
            Makefile          # run to create documentation
        |- examples
        |- pkgname            # your library
            |- core           # contains your pkg core classes
            |- tests          # contains your pkg tests - pytest
            |- utils          # contains your pkg utils


Installing your pkg in editable mode
------------------------------------

During your project you will find that some behaviour can be encapsulated in
either classes or methods. This will save you repeating code in every single
script you write. These classes and/or methods will be part of your library.
You can find an example in ``pkgname``.

It is recommended to install the package in editable (develop) mode. It puts a link
(actually \*.pth files) into the python installation to your code,
so that your package is installed, but any changes will immediately take effect.
This way all your can import your package the usual way.

First, ensure that the repository is in your local machine (we just did it
on the previous section)

.. code::

  git clone https://github.com/<username>/<reponame>.git

Let's install the requirements. Move to the folder where requirements.txt is
and install all the required libraries as shown in the statements below. In
the scenario of missing libraries, just install them using pip.

.. code::

  python -m pip install -r requirements.txt   # Install al the requirements

.. note:: Note that you will need to add required libraries so other people
   can start using your package quickly. For example, if you use use
   scikit-learn then include scikit-learn in ``requirements.txt``.

Move to the directory where the setup.py is. Please note that although ``setup.py`` is
a python script, it is not recommended to install it executing that file with python
directly. Instead lets use the package manager pip.

.. warning:: Feel free to change your package name if you want. However, note that
   to make things work you will need to make the appropriate changes in existing
   files: ``setup.cfg`` and ``plot_greetings_01.py``.

.. code::

  python -m pip install --editable  .         # Install in editable mode

Read more about `packages <https://python-packaging-tutorial.readthedocs.io/en/latest/setup_py.html>`_


Generating documentation
------------------------

.. note:: To generate autodocs automatically look at sphinx-napoleon and sphinx-autodocs.
   In general the numpy documentation style is used thorough the code.

Let's use Sphinx to generate the documentation. First, you will need to install sphinx,
sphinx-gallery, sphinx-std-theme and matplotlib. Note that they might have been already
installed through the ``requirements.txt``.

Let's install the required libraries.

.. code-block:: console

  python -m pip install sphinx            # Install sphinx
  python -m pip install sphinx-gallery    # Install sphinx-gallery for examples
  python -m pip install sphinx-std-theme  # Install sphinx-std-theme CSS
  python -m pip install matplotlib        # Install matplotlib for plot examples

Then go to the docs folder within main and run:

.. code-block:: console

  make github

Note that make github is defined within the Makefile and it is equivalent to:

.. code-block:: console

  make clean html
  cp -a _build/html/. ../../gh-pages/docs

These commands first generate the sphinx documentation in html and then copies
the html folder into the gh-pages branch. You can see how the documentation
looks like locally by opening the gh-pages/docs/index.html file. If you move to
the gh-pages branch and push all the changes the documentation will be also
available online thanks to GitHub Pages. You can access it through your
repository page (see Environments / GitHub Pages / Active)

Note that in order to edit the documentation you need to create .rst files and
include these newly created files in the index.rst document. An example is shown
in docs/source/tutorials/setup.rst.

In addition, you can create and document python scripts that will be automatically
included in the documentation (gallery examples) using sphinx-gallery. Remember
to include the folder(s) containing the scripts in the variable ``sphinx_gallery_conf``
in the conf.py file as shown below for tutorial.

.. code-block:: console
    :emphasize-lines: 4, 6

    # Configuration for sphinx_gallery
    sphinx_gallery_conf = {
        # path to your example scripts
        'examples_dirs': ['../../examples/tutorial'],
        # path to where to save gallery generated output
        'gallery_dirs': ['../source/_examples/tutorial'],
        # Other
        'line_numbers': True,
        'download_all_examples': False,
        'within_subsection_order': FileNameSortKey
    }

Also remember to include the .rst file automatically generated
the ``docs/index.rst`` file.

.. code-block:: console
    :emphasize-lines: 6

    .. toctree::
        :maxdepth: 2
        :caption: Example Galleries
        :hidden:

        _examples/tutorial/index



To include the output of the script (e.g. graph or console output) in the documentation
remember to prefix the script file name with ``plot`` (e.g. plot_sample_01.py). You can
find the following examples in examples/tutorial:

    - ``plot_greetings_01.py`` script using your pkgname package.
    - ``plot_sample_01.py`` script just including all the code.
    - ``plot_sample_02.py`` script documenting steps within the code.



| Read more about `sphinx <https://www.sphinx-doc.org/en/master/>`_
| Read more about `sphinx-gallery <https://sphinx-gallery.github.io/stable/index.html>`_



Running tests
-------------

Just go to the main folder and run:

.. code::

  pytest


Read more about `pytest <https://docs.pytest.org/en/stable/>`_

Now it is time to start coding!
-------------------------------

I would recommend to start with dirty ``scripts`` in the scripts folder.

After some time coding, you might identify that part of your implementation
could be encapsulated in a number of classes and methods. Or that some
methods are being called very often. In such case, include those methods
in your ``pkgname`` so you can import them easily and therefore don't end up
copy/paste code all the time.

Once you have some results, create an example, document it and keep it clean.
For example, if you have trained a model and plotted some graphs to
evaluate its performance, create a file in gallery, document it properly
within the code and include the folder in sphinx-gallery. This will facilitate
to review the code and results and you will have everything ready to include
it later in your report!

Where to store the data?

**Option I:** When the datasets used in the examples are completely different,
we can include the datasets directly within the example folder as shown in
the folder structure below.

.. code-block::

    examples
    |- tutorial
    |- yourexample
        |- datasets  # put here any data
            |- pathology.csv
        |- outputs   # put here any outcomes
            |- datasets
                |- pathology_fmt.csv
        format_pathology.py
        do_something.py
        do_something_else.py

**Option II:** If your examples use always the same data (which is probably the
case) you could include the data in the main folder so it looks something
like this.

.. code-block::

    datasets
        |- microbiology.csv
        |- pathology.csv
    examples
    |- tutorial
    |- yourexample
        |- outputs   # put here any outcomes
            |- datasets
                |- pathology_fmt.csv
                |- microbiology_fmt.csv
        format_pathology.py     # loads datasets/pathology.csv saves in outputs
        format_microbiology.py  # loads datasets/microbiology.csv saves in outputs
        plot_roc_and_cfmatrix.py   # loads outputs/datasets/....
        plot_temporal_analysis.py  # loads outputs/datasets/...


Also, if you create various examples, the portion of the code that
loads and saves data might become a bit repetitive. However, this
is usually not included in the package. Thus you could use the
code below so the paths are not absolute but to the file you are
running:


.. code-block::

    # Libraries
    import pathlib

    # -------------------------------
    # Create configuration from data
    # -------------------------------
    # Current path
    curr_path = pathlib.Path(__file__).parent.absolute()

    # Folder with the raw data
    path_data = '{0}/../../datasets/'

    # Path with fixed data
    path_micro = '{0}/outputs/datasets/{1}'.format(
        curr_path, 'microbiology_fmt.csv')


These are just suggestions, if you feel more comfortable following other
folder structure and/or approaches feel free to do so!

Happy coding!

