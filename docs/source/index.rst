Welcome to pyAMR's documentation!
=================================

.. image:: ./_static/images/logo-pyamr-icon-v2.png
   :width: 100
   :align: right
   :alt: pyAMR

``PyAMR`` is a python lightweight library to facilitate the computation of common
Antimicrobial Resistance (AMR) related statistics such as the proportion
of resistance isolates, the resistance trend or the antimicrobial spectrum
of activity. In addition, it includes a number of examples to visualise
such information which relay on plotting libraries such as ``matplotlib``,
``seaborn`` or ``plotly``.

.. raw:: html

   <center>

      <a href="https://github.com/bahp/pyamr/" target="_blank">
         <button class="btn-github"> View on GitHub
            <img class="btn-icon" src="./_static/images/icon-github.svg" width=18/>
         </button>
      </a>

      <a href="https://www.mdpi.com/2079-6382/10/10/1267" target="_blank">
         <button class="btn-github">Manuscript
            <img class="btn-icon" src="./_static/images/icon-mdpi.webp" width=28/>
         </button>
      </a>

      <a href="https://youtu.be/32pTOcXszyg" target="_blank">
         <button class="btn-github"> Video on Youtube
            <img class="btn-icon" src="./_static/images/icon-youtube.svg" width=25/>
         </button>
      </a>

   </center>

   <br><br>

Antimicrobial drugs are commonly used. We have all heard of antibiotics, which fight bacteria,
but there are also antifungals, antivirals and antiparasitics that fight fungi, viruses and
parasites, respectively. The more we use these drugs, the less effective they become and this
problem is known as antimicrobial resistance (AMR). Resistant infections can be difficult, and
sometimes impossible, to treat. Thus providing accurate and up to date AMR surveillance reports
supports interventions and toolkits to improve antibiotic prescribing in the community, including
prescribing in general practices (GPs), dental and other settings and hospitals.

Let's see some reports that can be computed using ``PyAMR``.


.. list-table:: Example of AMR reports
   :widths: 15 50 35
   :header-rows: 1

   * - Name
     - Title
     - Metrics

   * - Report I
     - Surveillance on AMR resistance
     - | number of isolates,
       | resistance rate or ``SARI``
       | resistance trend or ``SART``

   * - Report II
     - Effectiveness of an antimicrobial
     - spectrum of activity or ``ASAI``




.. raw:: html

   <h6> Report I: Surveillance of AMR resistance </h6>

In order to present AMR surveillance results, the susceptibility test data is often first grouped
by three parameters: (i) the specimen or sample type (e.g. urine), (i) the infectious organism or
pathogen, and (iii) the antimicrobial. The following report provides results for all the
antimicrobials tested in ``urine`` samples in which ``Escherichia coli`` was grown and tested.

.. image:: ./_static/imgs/todo-sart-table.png
   :width: 600
   :align: center

.. raw:: html

   <br>

The table contains the following information:

 - ``R`` is the overall resistance; that is, the total proportion of resistance isolates.
 - ``TM`` is the monthly resistance trend (it would be 1 if resistance goes from 0 to 1 in a month).
 - ``TY`` is the yearly resistance trend (``TM`` x 12).
 - ``pearson`` is the correlation coefficient computed between the vector with the number of
   isolates used to compute the resistance on each time period (e.g. month or year) and the
   overall resistance obtained. It is used to assess whether the strategy used for testing
   might be affecting the resistance values. Ideally, there should not be a strong correlation
   between them (-0.5 <= ``pearson`` <= 0.5).
 - ``isolates`` is the the total number of isolates used to compute such metrics.
 - ``references`` includes manuscripts within the literate which presented similar resistance
   values to the ones displayed in the table. For more information about these, see the
   original `manuscript`_.

.. _manuscript: https://www.mdpi.com/2079-6382/10/10/1267

.. raw:: html

   <h6> Report II: Effectiveness of an Antimicrobial </h6>

The antimicrobial spectrum of activity refers to the range of microbe species that are susceptible
to these agents and therefore can be treated. In general, antimicrobial agents are classified into
broad, intermediate or narrow spectrum. Broad spectrum antimicrobials are active against both
Gram-positive and Gram-negative bacteria. In contrast, narrow spectrum antimicrobials have limited
activity and are effective only against particular species of bacteria. While these profiles appeared
in the mid-1950s, little effort has been made to define them. Furthermore, such ambiguous labels are
overused for different and even contradictory purposes.

To address this issue, the library defines the Antimicrobial Spectrum of Activity Index (``ASAI``)
which provides a way to compute a single numerical value. The following report provides results for
all the antimicrobials and microorganisms tested in ``urine`` samples.

.. image:: ./_static/imgs/todo-asai-table.png
   :width: 600
   :align: center

.. raw:: html

   <br>

The table table includes the following columns:

 - ``antimicrobial`` is the antimicrobial
 - ``ASAI_N`` is the spectrum of activity against gram negative bacteria.
 - ``ASAI_P`` is the spectrum of activity against gram positive bacteria.
 - ``N_gn`` is the number of different (unique) genus.
 - ``N_sp`` is the number of different (unique) species.

.. raw:: html

   <br>
   <br>
   <br>

When using any of this project's source code, please cite:


.. code-block::

   @article{hernandez2021resistance,
     title = {Resistance Trend Estimation Using Regression Analysis to Enhance Antimicrobial Surveillance: A Multi-Centre Study in London 2009--2016},
     author = {Hernandez, Bernard and Herrero-Vi{\~n}as, Pau and Rawson, Timothy M and Moore, Luke SP and Holmes, Alison H and Georgiou, Pantelis},
     journal = {Antibiotics},
     volume = {10},
     number = {10},
     pages = {1267},
     year = {2021},
     month = oct,
     publisher = {MDPI},
     doi = {10.3390/antibiotics10101267},
     url = {},
   }

.. .. image:: ./_static/imgs/logo-icl-square.png
   :width: 50
   :align: right
   :alt: Imperial College London

.. _Spiral: https://spiral.imperial.ac.uk/handle/10044/1/73000

.. note::

    The PhD thesis is available on `Spiral`_.


.. .. bibliography::

.. :cite:p:`espaur2017`
.. :cite:p:`ecdc2016`
.. :cite:p:`world2017global`
.. :cite:t:`2018:hernandez`.
.. :cite:p:`2018:hernandez`.
.. :footcite:t:`2018:hernandez`
.. :footcite:t:`rawson2021real`
.. :cite:p:`o2014antimicrobial`



.. toctree::
   :maxdepth: 2
   :caption: Contents:

.. toctree::
   :maxdepth: 2
   :caption: Tutorial
   :hidden:

   usage/introduction
   usage/installation
   usage/quickstart
   usage/advanced
   usage/todo

.. toctree::
   :maxdepth: 2
   :caption: Example Galleries
   :hidden:

   _examples/tutorial/index
   _examples/indexes/index
   _examples/forecasting/index
   _examples/visualization/index

.. usage/quickstart
   _examples/reports/index

.. toctree::
   :maxdepth: 4
   :caption: API
   :hidden:

   _apidoc/pyamr.rst

.. toctree::

.. currentmodule:: pyamr


aaaa

.. automodule:: pyamr
   :no-members:
   :no-inherited-members:

bbbb

.. autosummary::
   :toctree: source/
   :template: module.rst

cccc

.. autosummary::
   :toctree: _autosummary
   :recursive:

ddd

.. autosummary::
   :toctree: source/
   :template: module.rst

   utils
   core

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


