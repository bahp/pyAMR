Advanced
==========

Building the Registries
-----------------------

A registry can be described as a centralized database or record-keeping system that stores
and manages information about a specific subject. In our scenario, we maintain a registry
of microorganisms and antimiocrobials, which includes details like their taxonomy (genus,
species), the gram stain type (posotive, or negative), the category (penicillins) and so on.

To create the registries we have provided the following bash script

.. literalinclude:: ../../../pyamr/datasets/registry/automated_run.sh
    :caption: ``pyamr/datasets/microbiology/registry/automated_run.sh``
    :language: bash

which can be run as follows

.. code-block::

    ./automated_run.sh

Each of the steps within the script are explained below.

Microorganisms
~~~~~~~~~~~~~~

The folder structure looks as follows. Note that each of the folder has at least the
``script.py`` and ``db_xxx.csv`` files. The former is a python script with the code
necessary to format, validate and finally create the corresponding database. This
database is named ``db_xxx.csv`` and is used at a latter stage to create the final
registry.

.. code-block::

    microorganisms
        |- gram_stain
            |- db_gram_stain.csv
            |- gram_negative.txt      // external resource
            |- gram_positive.txt      // external resource
            |- script.py
        |- subspecies
            |- db_groups.csv
            |- script.py
        |- taxonomy
            |- db_taxonomy.py
            |- bac120_taxonomy.tsv    // external resource
            |- script.py
        |- uuids
            |- db_codes.csv
            |- script.py
        |- script.py                  // generates registry_microorganisms.csv

The main ``script.py`` is used to generate the final ``registry_microorganisms.py``

* Generating the **Gram stain** database

    .. _FGP: https://en.wikipedia.org/wiki/Category:Gram-positive_bacteria
    .. _FGN: https://en.wikipedia.org/wiki/Category:Gram-negative_bacteria

    In this script we create a database with the gram stain information. For this,
    we have downloaded the list of genus and species belonging to each of the groups
    from the Wikipedia. Thus, we have created two files ``gram_negative.txt`` and
    ``gram_positive.txt`` and included all the information from `FGN`_ and `FGP`_
    respectively. These files look as follows:

    .. literalinclude:: ../../../pyamr/datasets/registry/microorganisms/gram_stain/gram_negative.txt
        :lines: 1-5

    Then, we have combined them using ``script.py`` into ``db_gram_stain.csv``.

    .. _FGP: https://en.wikipedia.org/wiki/Category:Gram-positive_bacteria

    .. literalinclude:: ../../../pyamr/datasets/registry/microorganisms/gram_stain/db_gram_stain.csv
        :lines: 1-5


* Generating the **Taxonomy** database

    .. _FBT: https://data.gtdb.ecogenomic.org/releases/latest/

    In this script we create a daabase with the taxonomy information. For this, we have
    downloaded the information from `FBT`_ and saved the file ``bac120_taxonomy.tsv``. Then
    we have done some minor amendments, corrections and checks in ``script.py`` and the result
    has been saved into a single .csv named ``db_taxonomy.csv``.

    .. literalinclude:: ../../../pyamr/datasets/registry/microorganisms/taxonomy/db_taxonomy.csv
        :lines: 1-5

* Generating the **uuids** database

    In this script we create a database with the unique codes that want to
    assign to each microorganism species.

    .. literalinclude:: ../../../pyamr/datasets/registry/microorganisms/uuids/db_codes.csv
        :lines: 1-5

* Generating the **subspecies** database

    In this script we create a database with any additional category that we
    want to include. For example, we can see the categories subspecies, group,
    coagulase production, haemolysis and host.

    .. literalinclude:: ../../../pyamr/datasets/registry/microorganisms/subspecies/db_groups.csv
        :lines: 1-5

The final registry looks as follows:

    .. literalinclude:: ../../../pyamr/datasets/registry/registry_microorganisms.csv
        :lines: 1-5

Antimicrobials
~~~~~~~~~~~~~~

The folder structure looks as follows. Note that each of the folder has at least the
``script.py`` and ``db_xxx.csv`` files. The former is a python script with the code
necessary to format, validate and finally create the corresponding database. This
database is named ``db_xxx.csv`` and is used at a latter stage to create the final
registry.

.. code-block::

    antimicrobials
        |- categories
            |- db_categories.csv
            |- category_aminoglycosides.txt      // external resource
            |- category_carbapenems.txt          // external resource
            |- category_aminoglycosides.txt      // external resource
            |- category_oxazolidinones.txt       // external resource
            |- category_penicillins.txt          // external resource
            |- category_quinolones.txt           // external resource
            |- category_tetracyclines.txt        // external resource
            |- script.py
        |- subspecies
            |- db_groups.csv
            |- script.py
        |- taxonomy
            |- db_taxonomy.py
            |- bac120_taxonomy.tsv    // external resource
            |- script.py
        |- uuids
            |- db_codes.csv
            |- script.py
        |- script.py                  // generates registry_microorganisms.csv

The main ``script.py`` is used to generate the final ``registry_antimicrobials.py``

* Generating the **categories** database

    In this script we create a database with the main categories. The database
    has been created manually and the other ``category_xxxx.txt`` files are just
    for reference.

    .. literalinclude:: ../../../pyamr/datasets/registry/antimicrobials/categories/db_categories.csv
        :lines: 1-5

The final registry looks as follows:

    .. literalinclude:: ../../../pyamr/datasets/registry/registry_antimicrobials.csv
        :lines: 1-5

What fixtures are available?
----------------------------

In the context of software testing, a fixture refers to a set of predefined data or conditions
that are used to create a known and stable starting point for tests. Fixtures provide the
necessary context for executing tests and can include data, objects, configurations, or any
other elements required for the test to run successfully.


.. list-table:: List of available fixtures
   :widths: 15 60 30
   :header-rows: 1

   * - Path
     - Description
     - Categories

   * - ``fixtures_01.csv``
     - Empty
     -

   * - ``fixtures_02.csv``
     - Does not exist
     -

   * - ``fixtures_03.csv``
     - Susceptibility test records data created manually.
     -

   * - ``fixtures_04.csv``
     - Summary table necessary to compute ASAI.
     -

   * - ``fixtures_05.csv``
     - Susceptibility test records data created manually for ACSI.
     -

   * - ``fixtures_06.csv``
     - Susceptibility test records data created manually for ACSI.
     -

   * - ``fixtures_07.csv``
     -
     -

   * - ``fixture_antibiogram.csv``
     -
     -

   * - ``fixture_spectrum.csv``
     -
     -

   * - ``fixture_surveillance``
     -
     -

   * - ``cddep/summary.csv``
       ``cddep/susceptibility.csv``
       ``cddep/prescriptions.csv``
       ``cddep/outcome.csv``
     -
     -

   * - ``lancet/mmc2_MIS.csv``
       ``lancet/mmc2_CMIS.csv``
       ``lancet/mmc2_MARKOV.csv``
     -
     -

   * - ``nhs``
     - Incomplete!
     -

   * - ``mimic``
     - Incomplete!
     -



Fixture 01
~~~~~~~~~~

Fixture 02
~~~~~~~~~~

Fixture 03
~~~~~~~~~~

    .. literalinclude:: ../../../pyamr/fixtures/fixture_03.csv
        :lines: 1-5
Fixture 04
~~~~~~~~~~

    .. literalinclude:: ../../../pyamr/fixtures/fixture_04.csv
        :lines: 1-5

Fixture 05
~~~~~~~~~~

    .. literalinclude:: ../../../pyamr/fixtures/fixture_05.csv
        :lines: 1-5

Fixture 06
~~~~~~~~~~

    .. literalinclude:: ../../../pyamr/fixtures/fixture_06.csv
        :lines: 1-5

Fixture 07
~~~~~~~~~~

    .. literalinclude:: ../../../pyamr/fixtures/fixture_07.csv
        :lines: 1-5

CDDEP - How to compute DRI?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. literalinclude:: ../../../pyamr/fixtures/summary.csv
        :lines: 1-5

    .. literalinclude:: ../../../pyamr/fixtures/outcome.csv
        :lines: 1-5

    .. literalinclude:: ../../../pyamr/fixtures/susceptibility.csv
        :lines: 1-5

    .. literalinclude:: ../../../pyamr/fixtures/prescriptions.csv
        :lines: 1-5

LANCET - How to compute ACSI?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. literalinclude:: ../../../pyamr/fixtures/mmc2_MIS.csv
        :lines: 1-5

    .. literalinclude:: ../../../pyamr/fixtures/mmc2_CMIS.csv
        :lines: 1-5

    .. literalinclude:: ../../../pyamr/fixtures/mmc2_MARKOV.csv
        :lines: 1-5

MIMIC
~~~~~


NHS
~~~
