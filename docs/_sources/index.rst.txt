Welcome to pyAMR's documentation!
=================================

.. image:: ./_static/images/logo-pyamr-v1.png
   :width: 100
   :align: right
   :alt: pyAMR

PyAMR is a python lightweight library to facilitate the computation of common
Antimicrobial Resistance (AMR) related statistics such as the proportion
of resistance isolates, the resistance trend or the antimicrobial spectrum
of activity. In addition, it includes a number of examples to visualise
such information which relay on plotting libraries such as ``matplotlib``,
``seaborn`` or ``plotly``.

For a video demonstration visit the EPiC IMPOC Microbiology app!

.. raw:: html

   <center>

      <a href="https://github.com/bahp/pyamr/" target="_blank">
         <button class="btn-github"> View on GitHub
            <img class="btn-icon" src="./_static/images/icon-github.svg" width=18/>
         </button>
      </a>

      <a href="https://github.com/bahp/django-epicimpoc-microbiology.git" target="_blank">
         <button class="btn-heroku"> Demo on Github
            <img class="btn-icon" src="./_static/images/logo-epicimpoc-micro.png" width=18/>
         </button>
      </a>

   </center>

   <br><br>

Below there are a couple of examples which some of the statistics that can be computed
using the library. The first figure shows the overall resistance (``R``), the monthly (``TM``)
and yearly (``TY``) resistance trend, the pearson correlation coefficient and the amount of
isolates used to compute such metrics. The metrics are also displayed visually on the
graphs below.

.. image:: ./_static/imgs/todo-sart-table.png

The second figure shows the antimicrobial spectrum of activity for all the antibiotics
tested on urine samples. The table includes the antimicrobial, and the spectrum of activity
for gram negative (``ASAI_N``) and gram positive (``ASAI_P``) bacteria. For each category it
includes the number of genus (``N_gn``) and species (``N_sp``).

.. image:: ./_static/imgs/todo-asai-table.png


.. .. image:: ./_static/imgs/logo-icl-square.png
   :width: 50
   :align: right
   :alt: Imperial College London

.. note::

    The PhD thesis is available on Spiral: https://spiral.imperial.ac.uk/handle/10044/1/73000



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
   usage/registries
   usage/todo

.. toctree::
   :maxdepth: 2
   :caption: Example Galleries
   :hidden:

   _examples/tutorial/index
   _examples/indexes/index
   _examples/forecasting/index
   _examples/reports/index
   _examples/visualization/index

.. toctree::
   :maxdepth: 2
   :caption: API
   :hidden:

   _apidoc/pyamr


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


