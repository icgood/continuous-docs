Python Continuous Documentation
===============================

[![Build Status](https://travis-ci.com/icgood/continuous-docs.svg?branch=main)](https://travis-ci.com/icgood/continous-docs)
[![Docs](https://img.shields.io/badge/docs-latest-informational)](http://icgood.github.io/continuous-docs/)

## Introduction

If you own a Python library that uses [Sphinx formatted][1] docstrings, it's
easy to get started turning these docstrings into beautiful HTML, hosted on
[GitHub Pages][4], updated every time you push to GitHub.

This repository is intended to be a working example of this method, check out
[the docs][2].

There is an older version of this tutorial
[written for Jenkins](https://github.com/icgood/continuous-docs/tree/jenkins).

#### Why not use [ReadTheDocs][8]?

Please do! This tutorial simply provides an alternative.

## Setting Up Your Project

### Installation

As always, I suggest using a [virtualenv][3] for local Python development.
Inside your virtualenv, run:

    pip install sphinx

### Setup

Create a `doc` directory in your project, we'll add it to git later:

```bash
mkdir -p doc
cd doc
```

Create the basic configuration and file structure:

    sphinx-quickstart

There are several questions you need to give a non-default answer to:

    > Separate source and build directories (y/N) [n]: y
    > Project name: yourproject
    > Author name(s): Your Name
    > Project version: 1.2.3
    > autodoc: automatically insert docstrings from modules (y/N) [n]: y
    > intersphinx: link between Sphinx documentation of different projects (y/N) [n]: y

### Creating the Doc Layout

When running `sphinx-quickstart`, you specified `index.rst` as the starting
point for your documentation pages. With Sphinx, you'll need every page linked
either directly or indirectly from `index.rst` using the `.. toctree::`
directive. Let's consider the following Python package:

    docpkg/__init__.py
    docpkg/main.py
    docpkg/config.py

One package, three modules. Replace your `index.rst` with the following:

```rst
``docpkg`` Package
==================

.. automodule:: docpkg
   :members:

-------------------

**Sub-Modules:**

.. toctree::

   docpkg.main
   docpkg.config
```

Now we're going to create two more files, `docpkg.main.rst` and
`docpkg.config.rst`.  I'll give you `docpkg.main.rst`, create
`docpkg.config.rst` the same way:

```rst
``docpkg.main`` Module
========================

.. automodule:: docpkg.main
   :members:
```

As you add more modules to your project, they need to be added to the
documentation structure. You can obviously put more than one `.. automodule::`
on a page, at your discretion.

### Building the Docs Locally

Once you have your doc layout created, you can build your documentation from
the `doc/` directory with:

    make html

Try navigating to `doc/build/html/index.html` in your browser!

### Add Documentation Requirements

I usually keep a `doc/requirements.txt` file around so that I don't have to
hard-code the dependencies necessary to build the documentation anywhere. For
now, this may only contain one:

    sphinx

In the future, you might add others with themes or sphinx extensions.

### Committing to Git

The entire `doc/` directory tree does not necessarily need to be put into git.
The following should suffice:

```bash
git add doc/requirements.txt doc/Makefile doc/source/conf.py doc/source/*.rst
git commit
```

### Creating GitHub Pages Branch

GitHub will generate a [GitHub Pages][4] site for any
repository that has a `gh-pages` branch. Let's set ours up now:

```bash
git checkout --orphan gh-pages
git rm -rf .
```

Now let's add the `.nojekyll` file. This tells GitHub that our content does not
use Jekyll for rendering. Finally, commit and push:

```bash
touch .nojekyll
git add .nojekyll
git commit -m 'initial commit'
git push origin gh-pages
```

## Setting up Travis CI

Thus far we have only built docs locally. We will now configure [Travis CI][9]
to build and deploy the docs any time we merge changes to our default branch.
It does so by committing the files under `doc/build/html` into the `gh-pages`
branch and pushing using your [GitHub Personal Access Token][10].

All the steps below operate on the `.travis.yml` file in your project
repository. It is assumed that you have already setup Travis to build your
project, otherwise [start there][12].

### Setting the Version

Because Python projects usually declare their version in `setup.py`, we want
Sphinx to look there to find the project version so our API docs reflect the
correct value.

In `doc/source/conf.py`, you likely see this value:

```python
release = '1.2.3'
```

Replace that line with one that reads the version correctly:

```python
import pkg_resources

# Read the project version from setup.py
release = pkg_resources.require(project)[0].version
```

### Building the Docs

To start, we need to make sure our build has Sphinx and other doc dependencies
installed, so add a new `install` step:

```yaml
install:
  - travis_retry pip install -U -r doc/requirements.txt
  # ...
```

Next, add an `after_success` step to build the docs:

```yaml
after_success:
  - make -C doc html
  # ...
```

### Deploying to GitHub Pages

Travis can [deploy to GitHub Pages][11] on build with the simple addition of a
`deploy` section:

```yaml
deploy:
  provider: pages
  skip_cleanup: true
  github_token: $GITHUB_TOKEN
  keep_history: true
  on:
    branch: main  # the default branch name
  local_dir: doc/build/html
```

If you have not already, turn on [GitHub Pages][4] for your repository using
the `gh-pages` branch under *Settings* &rarr; *GitHub Pages*.

### Setting Your GitHub Token

**This step should be taken very carefully!**

First, you should have a [token][10] with `repo` scope, so that Travis may
access and update your `gh-pages` branch. You will need to copy this token
shortly.

Navigate to your project settings in Travis. Under the *Environment Variables*
section, add a new variable:

| NAME | VALUE | BRANCH | DISPLAY VALUE IN BUILD LOG |
| ---- | ----- | ------ | -------------------------- |
| `GITHUB_TOKEN` | *paste your token here* | `main` | **LEAVE UNCHECKED** |

Change `main` if that is not the name of your default branch. Be absolutely sure
not to check *Display value in build log* or your API token may be leaked and
should be deleted.

### Commit

Commit and push your `.travis.yml` updates, and watch your Travis build logs to
watch it in action. If all goes well, your project's GitHub Pages site should be
now contain your latest and greatest API documentation.

:tada:

[1]: http://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example
[2]: http://icgood.github.io/continuous-docs/
[3]: https://docs.python.org/3/library/venv.html
[4]: https://pages.github.com/
[6]: https://pypi.python.org/pypi
[7]: http://sphinx-doc.org/rest.html
[8]: https://readthedocs.org/
[9]: https://travis-ci.com/
[10]: https://github.com/settings/tokens
[11]: https://docs.travis-ci.com/user/deployment/pages/
[12]: https://docs.travis-ci.com/user/tutorial/
