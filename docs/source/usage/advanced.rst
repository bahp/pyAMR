Advanced
==========

Building the Registries
-----------------------

A registry can be described as a centralized database or record-keeping system that stores
and manages information about a specific subject. In our scenario, we maintain a registry
of microorganisms and antimiocrobials, which includes details like their taxonomy (genus,
species), the gram stain type (posotive, or negative), the category (penicillins) and so on.

To create the scripts we have provided the following bash script

.. literalinclude:: ../../../pyamr/datasets/microbiology/registry/automated_run.sh
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

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/microorganisms/gram_stain/gram_negative.txt
        :lines: 1-5

    Then, we have combined them using ``script.py`` into ``db_gram_stain.csv``.

    .. _FGP: https://en.wikipedia.org/wiki/Category:Gram-positive_bacteria

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/microorganisms/gram_stain/db_gram_stain.csv
        :lines: 1-5


* Generating the **Taxonomy** database

    .. _FBT: https://data.gtdb.ecogenomic.org/releases/latest/

    In this script we create a daabase with the taxonomy information. For this, we have
    downloaded the information from `FBT`_ and saved the file ``bac120_taxonomy.tsv``. Then
    we have done some minor amendments, corrections and checks in ``script.py`` and the result
    has been saved into a single .csv named ``db_taxonomy.csv``.

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/microorganisms/taxonomy/db_taxonomy.csv
        :lines: 1-5

* Generating the **uuids** database

    In this script we create a database with the unique codes that want to
    assign to each microorganism species.

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/microorganisms/uuids/db_codes.csv
        :lines: 1-5

* Generating the **subspecies** database

    In this script we create a database with any additional category that we
    want to include. For example, we can see the categories subspecies, group,
    coagulase production, haemolysis and host.

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/microorganisms/subspecies/db_groups.csv
        :lines: 1-5

The final registry looks as follows:

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/microorganisms/registry_microorganisms.csv
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

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/antimicrobials/categories/db_categories.csv
        :lines: 1-5

The final registry looks as follows:

    .. literalinclude:: ../../../pyamr/datasets/microbiology/registry/antimicrobials/registry_antimicrobials.csv
        :lines: 1-5