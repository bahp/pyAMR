Registries
----------

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

The table below shows some relevant characteristics that can be used to describe various
microorganisms. Therefore, these can also be used to categorise or group microorganisms
that have similar properties

==================== ============================================================= ==========
Definition           Categories                                                    Status
==================== ============================================================= ==========
taxonomy             domain, kingdom, phylum, class, order, family, genus, species ``Ok``
gram_stain           positive, negative                                            ``Ok``
shape/morphology     cocci, bacilli, vibrio, spirochete
growth               aerobic, anaerobic
hemolysis            alpha, beta, gamma, no-hemolysis
coagulase_production positive, negative
group                A, B, C, D, ...
arrangement
endospores
mobility?
salinity
oxygen_requirements
habitat
temp_range
temp_optima
disease
host                 human, animals, swine, cattle, ...
fermenting           lactose, non-lactose
acid_fastness_stain
ziehl_nealson_tain
==================== ============================================================= ==========

.. note:: Most of these categories have not been used within the library.


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

[REF]: https://www.sciencedirect.com/topics/medicine-and-dentistry/microbial-morphology

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
--------------

An antimicrobial is an agent that kills microorganisms or stops their growth. Antimicrobial
medicines can be grouped according to the microorganisms they act primarily against in for main
categories: (i) **anibiotics** which are used against bacteria, (ii) **antifungals** which are used
against fungi, (iii) **antivirals** which are used against viruses and (iv) **antiparasitics** which
are used against parasites.

.. image:: https://antibioticguardian.com/assets/Antimicrobials_AMR-infographic_UKHSA.png

An antibiotic is a type of antimicrobial substance active against bacteria. It is the most important type
of antibacterial agent for fighting bacterial infections, and antibiotic medications are widely used in the
treatment and prevention of such infections.

[REF]: https://en.wikipedia.org/wiki/Antibiotic

.. image:: https://girlymicrobiologist.files.wordpress.com/2020/10/antibiotic-classes.png

