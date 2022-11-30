# FUNCTIONAL TREAMENT EFFECTS

[![main](https://github.com/timmens/functional-treatment-effects/actions/workflows/main.yml/badge.svg)](https://github.com/timmens/functional-treatment-effects/actions/workflows/main.yml)
[![image](https://codecov.io/gh/timmens/functional-treatment-effects/branch/main/graph/badge.svg)](https://codecov.io/gh/timmens/functional-treatment-effects)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/timmens/functional-treatment-effects/main.svg)](https://results.pre-commit.ci/latest/github/timmens/functional-treatment-effects/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Repo Size](https://img.shields.io/github/repo-size/timmens/functional-treatment-effects)

## Repository Information

This is the companion repository to the working paper *Causal Inference with Functional
Data* by [Tim Mensinger](https://www.tmensinger.com) and
[Dominik Liebl](https://www.dliebl.com/). It contains all necessary scripts to reproduce
dependencies of the presentation and paper, and to render the presentation itself ---we
are also working on automizing the compilation of the paper itself.

In the following we will explain how to use this repository to reproduce the results. If
you have any questions please contact Tim via email: `tmensinger[at]uni-bonn.de`.

## Build

In the following we explain how to reproduce the results on your machine.

### Environment

To reproduce this repository we require you to have Python and several other libraries
installed. A full list of requirements is provided in the
[environment.yml](./environment.yml) file. If you have these requirements installed you
can go to the next subsection. The easiest way to automatically install these packages
is to use the package manager conda, which you can install
[here](https://docs.conda.io/en/latest/miniconda.html). Once installed, open a shell and
execute

```console
$ cd /to/project/root
$ conda env create -f environment.yml
$ conda activate functional-treatment-effects
```

This installs the required packages into a specific environment, which avoids messing up
your local Python installation.

### pytask

Once the environment is installed and activated you can `cd` into the project root and
build the project by executing

```console
$ pytask
```

The [`pytask`](https://github.com/pytask-dev/pytask) command executes all necessary
scripts in the correct order.

> **Note** Every time you reopen the shell you have to activate the environment again
> using
>
> ```console
> conda activate functional-treatment-effects
> ```

otherwise you won't have access to the installed packages.

### Results

After running `pytask` you will find a new folder named `bld`. All created files can be
found there. Specifically you'll find figures in `bld/figures/` and the presentation in
`bld/presentation`.
