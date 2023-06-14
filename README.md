# pyamr

<img src="docs/source/_static/images/logo-pyamr-icon-v2.png" align="right" width="90">

[url-epicimpoc]: https://bahp.github.io/portfolio-academic/projects/epicimpoc/
[url-documentation]: https://bahp.github.io/pyAMR/index.html
[url-installation]: https://bahp.github.io/pyAMR/usage/installation.html
[url-development]: https://bahp.github.io/pyAMR/usage/development.html

[url-py39]: https://www.python.org/downloads/release/python-390/
[url-license]: https://www.gnu.org/licenses/gpl-3.0
[url-codecov]: https://codecov.io/gh/bahp/pyAMR
[url-readthedocs]: https://readthedocs.org/projects/docs/badge/?version=latest
[url-gh-package]: https://github.com/bahp/pyAMR/actions/workflows/package.yml
[url-gh-package]: https://github.com/bahp/pyAMR/actions/workflows/release.yml

[badge-py39]: https://img.shields.io/badge/python-3.9-blue.svg
[badge-codecov]: https://codecov.io/gh/bahp/pyAMR/branch/main/graph/badge.svg?token=GLL7GYY5TE
[badge-license]: https://img.shields.io/badge/license-GPLv3-orange.svg
[badge-gh-package]: https://github.com/bahp/pyAMR/actions/workflows/package.yml/badge.svg
[badge-gh-release]: https://github.com/bahp/pyAMR/actions/workflows/release.yml/badge.svg

[![Python 3.6][badge-py39]][url-py39]
[![readthedocs][url-readthedocs]][url-documentation]
[![codecov][badge-codecov]][url-codecov]
[![License][badge-license]][url-license]

[![.github/workflows/package.yml][badge-gh-package]][url-gh-package]
[![.github/workflows/release.yml][badge-gh-release]][url-gh-package]



Community | [Documentation][url-documentation] | Resources | Contributors | Release Notes

PyAMR is a python lightweight library to facilitate the computation of common Antimicrobial 
Resistance (AMR) related statistics such as the proportion of resistance isolates, the 
resistance trend or the antimicrobial spectrum of activity. In addition, it includes a number 
of examples to visualise such information which relay on plotting libraries such as 
``matplotlib``, ``seaborn`` or ``plotly``.

Antimicrobial drugs are commonly used. We have all heard of antibiotics, which fight bacteria, 
but there are also antifungals, antivirals and antiparasitics that fight fungi, viruses and 
parasites, respectively. The more we use these drugs, the less effective they become and this 
problem is known as antimicrobial resistance (AMR). Resistant infections can be difficult, and 
sometimes impossible, to treat. Thus providing accurate and up to date AMR surveillance reports 
supports interventions and toolkits to improve antibiotic prescribing in the community, including 
prescribing in general practices (GPs), dental and other settings and hospitals.

<div>
    <img src="docs/source/_static/imgs/todo-sart-table.png" width=700 align="right">  
</div>
<br>

<!-- ----------------------- -->
<!--    ABOUT THE PROJECT    -->
<!-- ----------------------- -->
## About the project

**[EPIC IMPOC][url-epicimpoc]** is an NIHR i4i funded project which aims to develop an intelligent 
clinical  decision support system to help doctors prescribe the most appropriate antibiotics. 
EPIC IMPOC is a collaborative project between medics and other health-care professionals from 
the National Institute for Health Research Health Protection Research Unit (NIHR HPRU) and 
engineers from the Centre for Bio-Inspire Technology (CBIT) at Imperial College London.

Please, acknowledge and/or cite the following article(s) when using this source code.

```console
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
```


<!-- ----------------------- -->
<!--     Installation        -->
<!-- ----------------------- -->
## Installation

Please see the [Installation Guide][url-installation].

<!-- ----------------------- -->
<!--      CONTRIBUTING       -->
<!-- ----------------------- -->
## Contributing

We welcome contributions including bug reports, bug fixes, documentation improvements, 
enhances and ideas from new contributors of all experience levels. The goals are to be 
helpful, welcoming, and effective. The [Development Guide][url-development] has detailed 
information about contributing code, documentation, tests, and more. We've included some 
basic information in this `README` and `CHANGELOG` file.

<!--For more information read <a href="#">CONTRIBUTING.md</a> for details on our 
code of conduct and the process for submitting pull requests to us.-->

#### Basic steps

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/FeatureName`)
3. Commit your Changes (`git commit -m 'Add some FeatureName'`)
4. Push to the Branch (`git push origin feature/FeatureName`)
5. Open a Pull Request
$ python -m build --sdist --wheel
$ twine upload -r testpypi dist/*

#### Testing

You can launch the test suite running

```
python manage.py test
```

#### Releasing

<!-- https://jacobtomlinson.dev/posts/2021/automating-releases-of-python-packages-with-github-actions/ -->

Releases are published automatically when a tag is pushed to GitHub.

```
# Set next version number
$ export RELEASE=x.x.x

# Create tags
$ git commit --allow-empty -m "Release $RELEASE"
$ git tag -a $RELEASE -m "v$RELEASE"

# Push
$ git push upstream --tags
```

<!-- ----------------------- -->
<!--         LICENSE         -->
<!-- ----------------------- -->
## License

Distributed under the GNU v3.0 License. See `LICENSE.md` for more information.


<!-- ----------------------- -->
<!--       CHANGELOG         -->
<!-- ----------------------- -->
## Changelog

Link to release history and/or `CHANGELOG` 




<!--

## Deleting tags

In order to delete tags the following commands might be useful
      
# Delete All local tags. (Optional Recommended)
$ git tag -d $(git tag -l)

# Fetch remote All tags. (Optional Recommended)
$ git fetch

# Delete All remote tags.
# Note: pushing once should be faster than multiple times
$ git push origin --delete $(git tag -l) 

# Delete All local tags.
$ git tag -d $(git tag -l)

-->