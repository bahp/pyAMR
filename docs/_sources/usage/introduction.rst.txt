Introduction
============

.. _phe: https://www.gov.uk/government/organisations/uk-health-security-agency/

The growing threat of antimicrobial resistance (AMR) is a leading patient health and
safety issue, with estimates that AMR will be responsible for more than 10 million deaths
by 2050. A major driver of AMR has been the misuse of antimicrobials
in humans. Whilst reasons for the misuse of antimicrobials are complex and multifaceted, a number
of factors have been described and investigated. At the individual level, physicians often prioritise
the management of the patient being treated, paying little regard to the long-term consequences of overusing
antimicrobials. Moreover, the majority of antimicrobials are prescribed by individuals who are
not experts in infection management and may have limited understanding of antimicrobials and the
potential consequences of AMR.

For such reason, numerous health organizations have promoted antimicrobial surveillance to regulate
prescriptions within clinical practice. At national level, Public Health England implemented the
English surveillance program for antimicrobial utilisation and resistance (ESPAUR) which
provides annual reports as a benchmark to determine appropriate local action.
At international level, the European Centre for Disease Prevention and Control through
the European antimicrobial resistance surveillance network (EARS-Net) has created the
largest publicly funded system for antimicrobial surveillance in Europe. Furthermore,
the World Health Organization has recently implemented the global antimicrobial resistance surveillance
system (GLASS) to strengthen the evidence base on AMR and inform decision-making.

With increasing electronic recording of data, there is a growing interest in the potential secondary
use of microbiology records to provide the necessary information to support antimicrobial stewardship
programs [20]. These programs are crucial to guide health care organizations designing evidence-based
policies to combat AMR [21, 22]. In particular, susceptibility reporting has shown to be a determinant
data source to inform empiric antimicrobial therapy selection.

.. image:: ../_static/imgs/susceptibility-test-record.png
   :width: 200
   :align: right
   :alt: ASAI

Susceptibility test records (see Figure 4.1) are composed by laboratory identification
number (LID), patient identification number (PID), date, sample type or culture (e.g.
blood or urine), pathogen, antimicrobial, reported status and outcome (resistant, sensitive
or intermediate). In research, the susceptibility test data is usually first grouped by
specimen or culture type, and further grouped by pairs (pathogen, antimicrobial)
since it is widely accepted by clinicians as detailed in the UK five year strategy in AMR [21].



Basics of susceptibility testing
------------------------------------

Antimicrobial susceptibility testing or ``AST`` is a laboratory method used to determine the
effectiveness of antimicrobial agents against specific microorganisms. It helps in guiding
appropriate antimicrobial therapy by providing valuable information about the susceptibility
or resistance of bacteria, fungi, or other pathogens to different drugs. Several key concepts
are involved in this process:

- **Minimum Inhibitory Concentration (MIC):** MIC is the lowest concentration of an antimicrobial
  agent that inhibits the visible growth of a microorganism. It provides a quantitative measure
  of the susceptibility of the organism to the drug.

- **Zone of Inhibition:** This concept is specific to disc diffusion tests, where antimicrobial agents
  are applied to a culture plate and diffuse outward. The zone of inhibition is the area around the
  disc where microbial growth is inhibited due to the effectiveness of the drug.

- **Breakpoints:** Breakpoints are predefined thresholds that categorize organisms as susceptible,
  intermediate, or resistant based on their MIC or zone of inhibition values. These breakpoints
  serve as guidelines for determining appropriate treatment options.

- **Quality Control:** Quality control measures are essential to ensure the accuracy and reliability
  of antimicrobial susceptibility testing. It involves testing reference strains with known
  susceptibility patterns to verify that the testing process is performing as expected.

- **Interpretive Criteria:** Interpretive criteria are guidelines provided by regulatory bodies,
  such as the Clinical and Laboratory Standards Institute (CLSI) or the European Committee on
  Antimicrobial Susceptibility Testing (EUCAST). These criteria help interpret the test results
  and provide recommendations for appropriate antimicrobial therapy.

Overall, antimicrobial susceptibility testing plays a vital role in guiding the selection of
appropriate antimicrobial agents, optimizing treatment outcomes, and combating antimicrobial resistance.

Microorganisms
~~~~~~~~~~~~~~

A microorganism, or microbe, is an organism of microscopic size, which may exist in its
single-celled form or as a colony of cells. Microbes are important in human culture and health
in many ways, serving to ferment foods and treat sewage, and to produce fuel, enzymes, and
other bioactive compounds. Microbes are essential tools in biology as model organisms and have
been put to use in biological warfare and bioterrorism. Microbes are a vital component of
fertile soil. In the human body, microorganisms make up the human microbiota, including the
essential gut flora. The pathogens responsible for many infectious diseases are microbes and,
as such, are the target of hygiene measures.

There are several approaches to categorizing infectious microorganisms. It's important to note
that these approaches are not mutually exclusive, and often multiple methods are used in
combination to fully understand and categorize infectious microorganisms. Furthermore, advances
in molecular techniques and genomics have provided new insights into the classification and
identification of microorganisms, allowing for more precise categorization based on genetic
characteristics.

.. list-table:: Example of categories
   :widths: 15 60 30
   :header-rows: 1

   * - Name
     - Description
     - Categories

   * - ``taxonomy``
     - Taxonomic characteristics, such as their genetic makeup, morphology, and
       evolutionary relationships
     - domain, kingdom, phylum, class, order, family, genus, species

   * - ``shape/morphology``
     - Refers to the shape and arrangement of bacterial cells including cocci (spherical),
       bacilli (rod-shaped), spirilla (spiral-shaped), and vibrios (comma-shaped)
     - cocci, bacilli, vibrio, spirochete

   * - ``gram_stain``
     - Helps identify the differences in the structure of the bacterial cell wall.
     - positive, negative

   * - ``coagulase_production``
     - It plays a role in the clotting of plasma proteins. Coagulase-positive bacteria can
       cause the formation of fibrin clots, while coagulase-negative bacteria do not produce
       this enzyme.
     - positive, negative

   * - ``oxygen_requirements``
     - Wehther require oxygen for growth and metabolism
     - aerobic, anaerobic

   * - ``fermenting``
     - Whether they can derive energy through fermentation in the absence of oxygen, or
       oxidative, meaning they require oxygen for energy production.
     - lactose, non-lactose

   * - ``hemolysis``
     - Refers to the ability of bacteria to lyse red blood cells
     - alpha, beta, gamma, no-hemolysis

   * - ``group``
     -
     - A, B, C, D, ...

   * - ``arrangement``
     -
     -

   * - ``endospores``
     -
     -

   * - ``mobility``
     -
     -

   * - ``temp_range``
     -
     -

   * - ``temp_optima``
     -
     -

   * - ``temp_range``
     -
     -

   * - ``acid_fastness_stain``
     -
     -

   * - ``ziehl_nealson_stain``
     -
     -

   * - ``transmission``
     - How they spread from one host to another
     -

   * - ``habitat``
     - Whether their are found in the environment (soil bacteria or waterborne bacteria),
       whether they coexist with the host without causing harm (commensal) or cause a
       disease (pathogenic)
     - environmental, commensal, pathogenic

   * - ``host``
     -
     - human, animal, swine, cattle, ...

   * - ``disease``
     -
     -

.. note:: These categories are for reference, most have not been used within the library.


Taxonomy
********

.. image:: https://textimgs.s3.amazonaws.com/boundless-microbiology/assification-l-pengo-vflip.svg#fixme
   :width: 130
   :align: right
   :alt: pyAMR

Bacterial taxonomy is a rank-based classification, of bacteria. In the scientific classification
established by Carl Linnaeus, each species has to be assigned to a genus (binary nomenclature),
which in turn is a lower level of a hierarchy of ranks (family, suborder, order, subclass, class,
division/phyla, kingdom and domain). In the currently accepted classification of life, there are
three domains (Eukaryotes, Bacteria and Archaea), which, in terms of taxonomy, despite following
the same principles have several different conventions between them and between their subdivisions.
See an example below.

  - life:
  - domain: Bacteria
  - kingdom:
  - phylum: Proteobacteria
  - class: Gamma Proteobacteria
  - order: Enterobacteriales
  - family: Enterobacteriaceae
  - genus: Escherichia
  - species: Escherichia coli
  - subspecies (missing in dataset)


Gram Stain
**********

Gram stain or Gram staining, also called Gram's method, is a method of staining used to
distinguish and classify bacterial species into two large groups according to the chemical
and physical properties of their cell walls: gram-positive bacteria and gram-negative
bacteria. The name comes from the Danish bacteriologist Hans Christian
Gram, who developed the technique.

- **Gram positive** bacteria take up the crystal violet stain used in the test, and then
  appear to be purple-coloured when seen through an optical microscope. This is because the
  thick peptidoglycan layer in the bacterial cell wall retains the stain after it is washed
  away from the rest of the sample, in the decolorization stage of the test.

- **Gram-negative** bacteria cannot retain the violet stain after the decolorization step;
  alcohol used in this stage degrades the outer membrane of gram-negative cells, making the
  cell wall more porous and incapable of retaining the crystal violet stain. Their peptidoglycan
  layer is much thinner and sandwiched between an inner cell membrane and a bacterial outer
  membrane, causing them to take up the counterstain (safranin or fuchsine) and appear red or
  pink.

.. note:: Despite their thicker peptidoglycan layer, gram-positive bacteria are more
    receptive to certain cell wall–targeting antibiotics than gram-negative bacteria,
    due to the absence of the outer membrane.


Shape or morphology
*******************

`ROS1`_: Microbial morphology.

.. _ROS1: https://www.sciencedirect.com/topics/medicine-and-dentistry/microbial-morphology

Different types of microbes have different, but characteristic, shapes. Under suitable
conditions, the shape and size of microbes are relatively stable. It is important to know
the morphological structure of microbes, as it provides us with a better understanding of
microbial physiology, pathogenic mechanisms, antigenic features, and allows us to identify
them by species. In addition, knowledge of microbial morphology can be helpful in diagnosing
disease and in preventing microbial infections.

Bacteria are complex and highly variable microbes. They come in four basic shapes: **spherical**
(cocci), **rod-shaped** (bacilli), **arc-shaped** (vibrio), and **spiral** (spirochete). See some
examples included in the figure below.


.. image:: https://upload.wikimedia.org/wikipedia/commons/1/1b/Bacterial_morphology_diagram-ro.svg
   :width: 600
   :align: center
   :alt: pyAMR

.. raw:: html

    <!--
    <img src="https://microbenotes.com/wp-content/uploads/2020/05/Bacterial-Shapes-and-Arrangement.jpeg"/>
    <img src="https://ars.els-cdn.com/content/image/3-s2.0-B978012802234400001X-f01-03-9780128022344.jpg"/>
    <img src="https://upload.wikimedia.org/wikipedia/commons/1/1b/Bacterial_morphology_diagram-ro.svg"/>
    -->


Growth Type
***********

The two main types of bacterial growth are **aerobic** and **anaerobic**. The basic difference
between the two, is that the former thrives in oxygenated environment and latter in an environment
marked by the absence of oxygen, there also exist other differences which cannot be ignored.

- **Aerobic:** These are the species of bacteria which require oxygen for their basic survival,
  growth, and the process of reproduction. It is very easy to isolate these bacteria by culturing
  a mass of bacterial strains in some liquid medium. As they require oxygen for survival, they
  tend to come to the surface in a bid to derive maximum oxygen available. Examples are Bacillus
  or Nocardia.

- **Anaerobic**: these are the species of bacteria which don’t require oxygen for growth. There are
  different types of anaerobic species, including the aerotolerant anaerobes, which can survive in the
  presence of oxygen, and obligate anaerobes, which can’t survive in the presence of oxygen. Examples
  are Escherichia coli or Bacteroides.



Haemolysis
**********

Hemolysis (from Greek αιμόλυση, meaning 'blood breakdown') is the breakdown of red blood cells. The
ability of bacterial colonies to induce hemolysis when grown on blood agar is used to classify certain
microorganisms. This is particularly useful in classifying streptococcal species. A substance that causes
hemolysis is a hemolysin.

- **Alpha-hemolysis:** When alpha-hemolysis (α-hemolysis) is present, the agar under the colony is
  light and greenish. Streptococcus pneumoniae and a group of oral streptococci (Streptococcus viridans
  or viridans streptococci) display alpha hemolysis.

- **Beta-hemolysis:** Sometimes called complete hemolysis, is a complete lysis of red cells in the media
  around and under the colonies: the area appears lightened (yellow) and transparent. Streptolysin, an
  exotoxin, is the enzyme produced by the bacteria which causes the complete lysis of red blood cells. There
  are two types of streptolysin: Streptolysin O (SLO) and streptolysin S (SLS).

- **Gamma-hemolysis:** If an organism does not induce hemolysis, the agar under and around the colony
  is unchanged, and the organism is called non-hemolytic or said to display gamma-hemolysis (γ-hemolysis).
  Enterococcus faecalis (formerly called "Group D Strep"), Staphylococcus saprophyticus, and Staphylococcus
  epidermidis display gamma hemolysis.


Coagulase Production
********************

Coagulase is a protein enzyme produced by several microorganisms that enables the conversion of fibrinogen
to fibrin. In the laboratory, it is used to distinguish between different types of Staphylococcus isolates.
Importantly, S. aureus is generally coagulase-positive, meaning that a positive coagulase test would indicate
the presence of S. aureus or any of the other 11 coagulase-positive Staphylococci. A negative coagulase
test would instead show the presence of coagulase-negative organisms such as S. epidermidis or S. saprophyticus.
However, it is now known that not all S. aureus are coagulase-positive. Whereas coagulase-positive
Staphylococci are usually pathogenic, coagulase-negative Staphylococci are more often associated with
opportunistic infection.

Antimicrobials
~~~~~~~~~~~~~~

An antimicrobial is an agent that kills microorganisms or stops their growth. Antimicrobial
medicines can be grouped according to the microorganisms they act primarily against in for main
categories: (i) **anibiotics** which are used against bacteria, (ii) **antifungals** which are used
against fungi, (iii) **antivirals** which are used against viruses and (iv) **antiparasitics** which
are used against parasites.

.. image:: https://antibioticguardian.com/assets/Antimicrobials_AMR-infographic_UKHSA.png

Antibiotics are powerful medications that are used to treat bacterial infections. They work by either killing
the bacteria or inhibiting their growth, thereby helping the body's immune system to overcome the infection.
There are various types of antibiotics, each with its own mechanism of action and spectrum of activity. Here's
an brief introduction to some of the different types of antibiotics:

- **Penicillins:** Penicillins were the first antibiotics discovered and are still widely used today.
  They work by interfering with the synthesis of bacterial cell walls, leading to their destruction.
  Examples of penicillins include amoxicillin and ampicillin.

- **Cephalosporins:** Cephalosporins are similar to penicillins in their mechanism of action. They also
  disrupt bacterial cell wall synthesis, but they have a broader spectrum of activity and are often
  used as an alternative to penicillins. Examples of cephalosporins include cephalexin and ceftriaxone.

- **Macrolides:** Macrolides are a class of antibiotics that inhibit bacterial protein synthesis. They bind
  to the bacterial ribosome, preventing the synthesis of new proteins. Macrolides are effective against
  many different types of bacteria and are often used to treat respiratory tract infections. Examples of
  macrolides include erythromycin and azithromycin.

- **Tetracyclines:** Tetracyclines are broad-spectrum antibiotics that inhibit protein synthesis in bacteria.
  They are often used to treat acne and respiratory tract infections. Tetracycline and doxycycline are
  examples of tetracycline antibiotics.

- **Fluoroquinolones:** Fluoroquinolones work by interfering with bacterial DNA replication and repair. They
  are effective against a wide range of bacteria and are commonly used to treat urinary tract infections
  and respiratory infections. Ciprofloxacin and levofloxacin are examples of fluoroquinolones.

- **Sulfonamides:** Sulfonamides, also known as sulfa drugs, inhibit the synthesis of folic acid in bacteria,
  which is essential for their growth. They are used to treat urinary tract infections, respiratory infections,
  and other bacterial infections. Examples of sulfonamides include sulfamethoxazole and trimethoprim.

- **Aminoglycosides:** Aminoglycosides are bactericidal antibiotics that inhibit bacterial protein synthesis.
  They are particularly effective against aerobic gram-negative bacteria. Aminoglycosides are often used in
  combination with other antibiotics to treat severe infections. Gentamicin and streptomycin are examples of
  aminoglycosides.

.. image:: https://girlymicrobiologist.files.wordpress.com/2020/10/antibiotic-classes.png

These are just a few examples of the different types of antibiotics available. It's important to note that
the choice of antibiotic depends on the specific infection being treated, as well as factors such as the type
of bacteria involved, the site of infection, and the patient's individual circumstances. Antibiotics should
always be used judiciously and under the guidance of a healthcare professional to ensure their appropriate
and effective use.

  - `RA1`_: Entry in wikipedia for Antibiotic.

.. _RA1: https://en.wikipedia.org/wiki/Antibiotic











Description of metrics for AMR
------------------------------

Establishing quantifiable metrics is essential to gain a standardized and objective framework to
monitor the emergence and spread of resistant strains, assess the effectiveness of antimicrobial
interventions, and evaluate the impact of various interventions and policies. Such metrics enable
us to quantify resistance levels, track trends over time, and compare data across different regions
and healthcare settings, facilitating evidence-based decision making. Furthermore, these metrics
provide a foundation for the development of sophisticated algorithms that can analyze vast amounts
of data, identify patterns, predict resistance patterns, and assist clinicians in making informed
treatment choices. By integrating these metrics into clinical decision support systems, healthcare
providers can access real-time, data-driven insights to optimize antimicrobial therapy, improve patient
outcomes, and mitigate the further development and dissemination of antimicrobial resistance.

.. list-table:: Summary of AMR metrics
   :widths: 4 49 13 43
   :header-rows: 1

   * -
     - Name
     - Range
     - Description
   * - ``SARI``
     - Single Antimicrobial Resistance Index
     - [0, 1]
     - Ratio of resistant isolates
   * - ``MARI``
     - Multiple Antimicrobial Resistance Index
     - [0, 1]
     - Ratio of agents tested to which a pathogen is resistant
   * - ``SART``
     - Single Antimicrobial Resistance Trend
     - [0, 1]
     - Ratio of change of resistance rates per time unit
   * - ``ASAI``
     - Antimicrobial Spectrum of Activity Index
     - [-1, 1]
     - Range of microbe species that are susceptible to an agent
   * - ``ACSI``
     - Antimicrobial Collateral Sensitivity Index
     - [-.7, .7]
     - Degree of dependence between two agents
   * - ``DRI``
     - Drug Resistance Index
     - [0, 1]
     - Ratio of pathogens resistant to the antimicrobials used to treat them

- **Single Antimicrobial Resistance Index (SARI)**

    The single antimicrobial resistance index describes the proportion of resistant isolates for a
    given set of susceptibility tests. It provides a value within the range [0,1] where values close
    to one indicate high resistance. It is agnostic to pathogen, antibiotic and time. The variables *R*,
    *I* and *S* represent the number of susceptibility tests with Resistant, Intermediate and Susceptible
    outcomes respectively. The definition might vary slightly since the intermediate category is not
    always considered.

    See: :py:mod:`pyamr.core.sari.SARI`

    Example: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_a_sari.py`

- **Multiple Antimicrobial Resistance Index (MARI)**

    The multiple antimicrobial resistance describes the ratio of antimicrobials tested (*T*) to which a
    pathogen is resistant (*R*). It provides a value within the range [0,1] where values close to
    one indicate high multi-drug resistance. It highly depends on the antimicrobials to which the
    pathogen is tested. Since tested antimicrobials vary among health care centres and time, comparison
    and analysis of its evolution in time is not straight forward. In addition, antibiotics which are
    intrinsically resistant should not be considered.

    See: :py:mod:`pyamr.core.mari.MARI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_c_mari.py`

- **Single Antimicrobial Resistance Trend (SART)**

    The single antimicrobial resistance trend measures the ratio of change per time unit
    (e.g. monthly or yearly). To compute this metric, it is necessary to generate a
    resistance time series from the susceptibility test data. This is often achieved by
    computing the SARI consecutive or overlapping partitions of the data. Then, the trend
    can be extracted using for example a linear model where the slope, which is a value
    within the range [-1, 1] indicates the ratio of change.

    See: :py:mod:`pyamr.core.sart.SART`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_d_sart.py`

- **Antimicrobial Spectrum of Activity Index (ASAI)**

    The antimicrobial spectrum of activity index refers to the range of microbe species that are
    susceptible to these agents and therefore can be treated. In general, antimicrobial agents are
    classified into broad, intermediate or narrow spectrum. Broad spectrum antimicrobials are active
    against both Gram-positive and Gram-negative bacteria. In contrast, narrow spectrum antimicrobials
    have limited activity and are effective only against particular species of bacteria.

    See: :py:mod:`pyamr.core.asai.ASAI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_b_asai.py`

- **Antimicrobial Collateral Sensitivity Index (ACSI)**

    The antimicrobial collateral sensitivity index is based on the mutual information score
    and is useful to identify antibiotic pairs displaying concurrent resistance, independence, or
    disjoint resistance. Mutual information quantifies the degree of dependence between two antibiotic
    susceptibility test results (X and Y) by measuring the amount of information gained about one test
    result (X) by knowing that of the other (Y). Susceptibility test results for pairs of antibiotics
    (X/Y) belong to one of four possible states: susceptible/susceptible, susceptible/resistant,
    resistant/susceptible, or resistant/resistant. Concurrent resistance manifests as an X/Y bias toward
    susceptible/susceptible and resistant/resistant states, resulting in a positive MIS. Conversely, an
    X/Y bias toward susceptible/resistant and resistant/susceptible due to disjoint resistance would result
    in a negative MIS. The MIS is maximised (0·7) when susceptibility to one antibiotic always predicts
    susceptibility to another antibiotic and similarly for non-susceptibility. The MIS is minimised
    (−0·7) when resistance to one antibiotic always predicts susceptibility to another and vice versa.

    See: :py:mod:`pyamr.core.acsi.ACSI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_f_acri.py`

- **Drug Resistance Index (DRI)**

    The drug resistance index measures the proportion of pathogens that are resistant to the
    antimicrobials used to treat them. It provides a value within the range [0,1] where values
    close to one indicate high resistant for frequent antimicrobials. The variable *ρik* is the
    proportion of resistance among organism *i* to antimicrobial *k* and *qik* is the
    frequency of drug *k* used to treat organism *i*.

    See: :py:mod:`pyamr.core.dri.DRI`

    Examples: :ref:`sphx_glr__examples_tutorial_indexes_plot_core_e_dri.py`



Essentials of time series analysis
----------------------------------

Time series analysis is a specific way of analyzing a sequence of data points collected over
an interval of time. In time series analysis, analysts record data points at consistent intervals
over a set period of time. Time series analysis typically requires a large number of data points
to ensure consistency and reliability. An extensive data set ensures you have a representative
sample size and that analysis can cut through noisy data. It also ensures that any trends or patterns
discovered are not outliers and can account for seasonal variance. Additionally, time series data
can be used for forecasting—predicting future data based on historical data.

Examples using time-series analysis in ``pyAMR``.

    - :ref:`sphx_glr__examples_tutorial_guide_plot_step_03.py`
    - :ref:`sphx_glr__examples_tutorial_guide_plot_step_04.py`

..
    - :ref:`examples-with-tsa`


..
    Time-series analysis is a method of analyzing data to extract useful statistical information and
    characteristics. One of the study's main goals is to predict future value. When forecasting with
    time series analysis, which is extremely complex, extrapolation is required. However, the forecasted
    value and the associated uncertainty estimation can make the result extremely valuable.

In time-series analysis, it is necessary to understand various statistical properties/tests
in order to assess which method to use and to better understand the behaviour of the
produced models. A summary of these statistical properties/tests is presented below.


Statistical properties
~~~~~~~~~~~~~~~~~~~~~~

A statistic (singular) or sample statistic is any quantity computed from values in a sample which
is considered for a statistical purpose. Some of the most commonly used descriptive statistics are
central tendency, dispersion, skewness, and tailednes.


.. list-table:: Summary of statistical properties
   :widths: 10 70 15 5
   :header-rows: 1

   * - Name
     - Description
     - Range
     - Choose
   * - ``pearson``
     - Measures linear correlation between variables
     - [-1, 1]
     - ≈0
   * - ``kurtosis``
     - Measure of tailedness of a probability distribution
     - [1, ∞)
     - ≈0
   * - ``skewness``
     - Measure of asymmetry of a probability distribution
     -
     - ≈0
   * - ``R2``
     - Measures goodness-of-fit or linear regression models
     - [0, 100]
     - ↑
   * - ``aic``
     - Measures goodness-of-fit among models
     -
     - ↓
   * - ``bic``
     - Measures goodness-of-fit among models
     -
     - ↓
   * - ``hqic``
     - Measures goodness-of-fit among models
     -
     -
   * - ``llf``
     -
     -
     -



Pearson
*******

.. _R1: https://cdn.scribbr.com/wp-content/uploads/2022/05/Strong-positive-correlation-and-strong-negative-correlation.webp
.. _R2: https://upload.wikimedia.org/wikipedia/commons/3/34/Correlation_coefficient.png

.. image:: https://www.simplilearn.com/ice9/free_resources_article_thumb/Pearson_Correlation_1.jpg
   :width: 320
   :align: right
   :alt: pearson

In statistics, the Pearson correlation coefficient is a measure of linear correlation
between two sets of data. It is the ratio between the covariance of two variables and
the product of their standard deviations; thus, it is essentially a normalized measurement
of the covariance, such that the result always has a value between −1 and 1. The measure
can only reflect a linear correlation of variables, and ignores many other types of
relationships or correlations.


R2
**

.. _R3: https://statisticsbyjim.com/regression/interpret-r-squared-regression/

R-squared is a goodness-of-fit measure for linear regression models. This
statistic indicates the percentage of the variance in the dependent variable
that the independent variables explain collectively. R-squared measures the
strength of the relationship between your model and the dependent variable
on a convenient 0 – 100% scale. R-squared is always between 0 and 100% where
(i) **0%** represents a model that does not explain any of the variation in the
response variable around its mean. The mean of the dependent variable predicts
the dependent variable as well as the regression model and (ii) **100%** represents
a model that explains all the variation in the response variable around its mean.


Skewness
********

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Negative_and_positive_skew_diagrams_%28English%29.svg/446px-Negative_and_positive_skew_diagrams_%28English%29.svg.png
   :width: 320
   :align: right
   :alt: skewness

Skewness is a measure of the asymmetry of the probability distribution of a
real-valued random variable about its mean. The skewness value can be positive,
zero, negative, or undefined.

For a unimodal distribution, negative skew commonly indicates that the tail is
on the left side of the distribution, and positive skew indicates that the tail
is on the right. In cases where one tail is long but the other tail is fat,
skewness does not obey a simple rule. For example, a zero value means that the
tails on both sides of the mean balance out overall; this is the case for a
symmetric distribution, but can also be true for an asymmetric distribution
where one tail is long and thin, and the other is short but fat.


Kurtosis
********

.. image:: https://surferhelp.goldensoftware.com/Resources/image/kurtosis.png
   :width: 320
   :align: right
   :alt: kurtosis

Kurtosis describes the extent to which the tails (or extremes) of a set of data
differ from those of a normal distribution. A bell curve distribution would exhibit
kurtosis of 3, so only numbers above or below 3 can be described as “excess” Kurtosis.

It is common to compare the excess kurtosis (defined below) of a distribution to 0,
which is the excess kurtosis of any univariate normal distribution. Distributions
with negative excess kurtosis are said to be platykurtic, although this does not
imply the distribution is "flat-topped" as is sometimes stated. Rather, it means the
distribution produces fewer and/or less extreme outliers than the normal distribution.
An example of a platykurtic distribution is the uniform distribution, which does not
produce outliers. Distributions with a positive excess kurtosis are said to be leptokurt.


Akaike information criterion
******************************

The Akaike information criterion (AIC) is an estimator of prediction error and thereby
relative quality of statistical models for a given set of data.[1][2][3] Given a collection
of models for the data, AIC estimates the quality of each model, relative to each of the
other models. Thus, AIC provides a means for model selection.

Bayesian information criterion
******************************

In statistics, the Bayesian information criterion (BIC) or Schwarz information criterion
(also SIC, SBC, SBIC) is a criterion for model selection among a finite set of models; models
with lower BIC are generally preferred. It is based, in part, on the likelihood function and
it is closely related to the Akaike information criterion (AIC).


Hannan-Quinn information criterion
**********************************

The Hannan-Quinn information criterion (HQC) is a measure of the goodness of fit of a statistical
model, and is often used as a criterion for model selection among a finite set of models. It is not
based on log-likelihood function (LLF), and but related to Akaike's information criterion.


Stationarity
************

.. warning:: Pending!

Statistical tests
~~~~~~~~~~~~~~~~~

A statistical test provides a mechanism for making quantitative decisions about a process or
processes. The intent is to determine whether there is enough evidence to "reject" a conjecture
or hypothesis about the process. The conjecture is called the null hypothesis.


.. list-table:: Summary of statistical tests
   :widths: 25 60 10 5
   :header-rows: 1

   * - Name
     - Description
     - Range
     - Choose
   * - ``jarque-bera``
     - Goodness-of-fit measure data matches normal dist
     -
     - ↓?
   * - ``durbin-watson``
     - Measure correlation of residuals in regression
     - [0, 4]
     - ≈2
   * - ``omnibus``
     -
     -
     - ↓?
   * - ``adfuller``
     -
     -
     -
   * - ``kendall``
     -
     -
     -
   * - ``kpss``
     -
     -
     -
   * - ``normal``
     -
     -
     -
   * - ``Kolmogorov-smirnov``
     -
     -
     -
   * - ``Shapiro-wilkinson``
     -
     -
     -
   * - ``Anderson-darling``
     -
     -
     -



Augmented Dicker-Fuller
***********************

.. warning:: Pending!

Kendal
************

.. warning:: Pending!

Kwiatkowski–Phillips–Schmidt–Shin
*********************************

.. warning:: Pending!

Jarque Bera
************

In statistics, the Jarque–Bera test is a goodness-of-fit test of whether sample data
have the skewness and kurtosis matching a normal distribution.

Durbin Watson
*************

The Durbin Watson (DW) statistic is a test for autocorrelation in the residuals
from a statistical model or regression analysis. The Durbin-Watson statistic will
always have a value ranging between 0 and 4. A value of 2.0 indicates there is
no autocorrelation detected in the sample.

Normal
******

.. warning:: Pending!

Kolmogorov-smirnov
******************

.. warning:: Pending!

Shapiro-wilkinson
*****************

.. warning:: Pending!

Anderson-darling
****************

.. warning:: Pending!

Omnibus
*******

Omnibus tests are a kind of statistical test. They test whether the explained variance
in a set of data is significantly greater than the unexplained ...

.. warning:: Pending!



