Future Actions
==============

.. warning:: This list of things to do could be also logged using github issues.

.. warning:: Reformat names in all the ``.csv`` files. Also create a sample dataset
    with microbiology data to be loaded automatically using the ``pyamr`` module. The
    file must contain the following columns:

    .. note: We are ignoring the ``OrgPieceCounter``

    ======================= =============================================================
    Column Name             Description
    ======================= =============================================================
    ``date_sample``         The date the sample was taken (datetime64[ns])
    ``date_outcome``        The date the outcome was available (or last edited)
    ``patient_id``          The anonymised patient id
    ``lab_number``          The laboratory number associated to the test.
    ``order_name``          The order type (e.g. sputum, urine, ...)
    ``order_code``          The order code
    ``order_description``   The order description (at the moment is called specimen type)
    ``microorganism_name``
    ``microorganism_code``
    ``antimicrobial_name``
    ``antimicrobial_code``
    ``sensitivity_method``
    ``sensitivity``
    ``mic``                 The Minimum Inhibitory Concentration
    ``reported``            The result was reported to clinicians (selective reporting)
    ``genus_name``
    ``specie_name``
    ``gram_type``           Microorganism classification based on cell wall.
    ``antimicrobial_class``
    ======================= =============================================================

    Also note that it would be very useful to find open source databases with all
    this information already available. In addition, they might contain other relevant
    information: (i) organisms grouped by shape, (ii) organisms group by ....
    (iii) antimicrobials grouped by ...

    .. note:: We are ignoring the OrgPieceCounter.



.. LINK1: https://www.statsmodels.org/stable/examples/notebooks/generated/robust_models_0.html

.. warning:: Computing ``SART`` using Robust Regression. `[1] <https://www.statsmodels.org/stable/examples/notebooks/generated/robust_models_0.html>`_


.. warning:: ``CSV``

    Generate big csv files with the main outcomes (freq, sari, sart, asai, ...)

.. warning:: ``HTML``

    Create HTML files that based on the information contained in the CSV file,
    allows to dynamically explore different organism and antimicrobial pairs,
    different order codes, ...

.. warning:: ``ANIMATION``

    Create animations that based on the information contained in the CSV file,
    displays the evolution of the aforementioned AMR statistics in time. Similar
    examples seen in.... d3.js?

.. warning:: ``LATEX``

    Generate automatically from the data the latex/html tables and graphs describing
    the Antimicrobial Spectrum of Activity Index - ``ASAI`` - (see example below). For
    more information check out the PhD thesis (Chapter 4).

    .. image:: ../_static/imgs/todo-asai-table.png
       :align: center
       :alt: ASAI

.. warning:: ``LATEX``

    Generate automatically from the data the latex/html tables and graphs describing
    the Single Antimicrobial Resistance Trend - ``SART`` - (see example below). For
    more information check out the PhD thesis (Chapter 4).

    .. image:: ../_static/imgs/todo-sart-table.png
       :align: center
       :alt: SART