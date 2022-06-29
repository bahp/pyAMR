Welcome to pyAMR's documentation!
=================================

.. image:: ./_static/images/logo-pyamr-v1.png
   :width: 100
   :align: right
   :alt: pyAMR

PyAMR is a lightweight library to facilitate the computation and visualisation
of various Antimicrobial Resistance (AMR) statistics. It includes a number of
visualisation examples that depend on matplotlib, seaborn and plotly. In addition,
an app to browse AMR statistics easily is under construction.


.. raw:: html

   <center>

      <a href="https://github.com/bahp/pyamr/" target="_blank">
         <button class="btn-github"> View on GitHub
            <img class="btn-icon" src="./_static/images/icon-github.svg" width=18/>
         </button>
      </a>

      <a href="" target="_blank">
         <button class="btn-heroku"> Demo on Heroku
            <img class="btn-icon" src="./_static/images/icon-heroku.svg" width=18/>
         </button>
      </a>

   </center>

   <br><br>

.. .. image:: ./_static/imgs/logo-icl-square.png
   :width: 50
   :align: right
   :alt: Imperial College London

.. _PhD: https://spiral.imperial.ac.uk/handle/10044/1/73000

The PhD thesis is on Spiral: `PhD`_


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


.. warning:: Some of the interactive examples included below might take considerable time
             to load, specially when created using the whole datasets (either ``NHS`` or
             ``MIMIC``) was used. For a quick pre-visualization, we recommend to click on
             ``Sample`` dataset examples (for now).

.. list-table:: List of interactive examples
   :header-rows: 1
   :align: center

   * - Name
     - ``Sample``
     - ``NHS``
     - ``MIMIC``
   * - Treemap + Images - SART (outdated)
     -
       .. raw:: html

         <a href="./_static/htmls/treemap-graph-simplified-sample/treemap-visualizer.html"
            target="_blank"> LINK </a>
     -
     -
   * - Treemap [culture, microorganism, antimicrobial] - SARI
     -
        .. raw:: html

           <a href="./_static/htmls/plot_pyplot_treemap.html" target="_blank"> LINK </a>
     -
        .. raw:: html

           <a href="./_static/htmls/plot_nhs_treemap.html" target="_blank"> LINK </a>
     -
        .. raw:: html

           <a href="./_static/htmls/plot_mimic_treemap.html" target="_blank"> LINK </a>




Examples visualisations (to implement):

   - https://ig.ft.com/coronavirus-lockdowns/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


