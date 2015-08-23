Python Continuous Documentation
===============================

## Introduction

So you've written your Python library and you were a good little developer,
keeping docstrings updated with [Sphinx formatting][1]. It's easy to get
started turning these docstrings into beautiful, hosted HTML, updated every
time you push to GitHub.

To see an example, check out the GitHub Pages for [this
project][2], generated using the
instructions in this tutorial!

## Setting Up Your Project

### Installation

As always, I suggest using a [virtualenv][3] for local Python development!
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

In the future, you might add others with themes or optional packages.

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

## Setting up Jenkins

This is where the magic happens. We will configure a Jenkins build to clone
your `gh-pages` and `master` branches. Then, we will build the docs from
`master` directly into `gh-pages`. Finally, we will commit and push the
`gh-pages` branch using the "Git Publisher" post-build action.

Let's start with a free-style job. When configuring your Git repository, make
sure you use the branch specifier `*/gh-pages`. We will clone the `master`
branch separately in the next section.

### Building the Docs

Add an "Execute shell" build step. In it, let's add some code:

```bash
virtualenv .venv
source .venv/bin/activate

repo_url=$(git config --get remote.origin.url)
rm -rf master/ || true
git clone $repo_url master/

pip install -U -r master/doc/requirements.txt
pip install -U master/

version=$(python master/setup.py --version)
git rm -rf ./$version/ || true
sphinx-build -b html master/doc/source/ ./$version/
ln -sf $version latest

git add ./$version/ latest
git commit -m "jenkins regenerated documentation $(date +%F)"
```

### Pushing to GitHub Pages

We've now built and committed our new docs to the `gh-pages` branch, but we
need to push it to GitHub before it will be rendered. Add a "Git Publisher"
post-build action:

* Push Only If Build Succeeds: ***&#x2713;***
* Add Branch:
  * Branch to push: `gh-pages`
  * Target remote name: `origin`

## Finishing Steps

You should now be able to try out your Jenkins build. The resulting docs will
be in the `latest/` subdirectory of the GitHub Pages project page. You will
probaby want to add an [`index.html`](index.html.example) with a redirect to
that subdirectory.

Before calling it done, you'll probably want to add a build trigger so that
this project is built automatically (otherwise it's not "continuous
documentation"). I recommend triggering the build after another job that runs
unit tests, but using a webhook directly from GitHub pushes works too.

## Frequently Asked Questions

### Q: How do I link to other projects?

***A:*** This is one of my favorite parts of Sphinx, the ability to link
directly to classes, functions, and modules in third-party projects on the
Internet. We can do this because we enabled the `intersphinx` extension, see
[its documentation][5] for its use.

### Q: Does my project meet the requirements?

***A:*** If you have a `setup.py` with an `install_requires` field to pull in
its own dependencies from [PyPi][6], that should be all you need!

### Q: Is it only for documenting code?

***A:*** Sphinx documentation is built using their heavily extended
[reStructuredText][7] markup. You can easily add items to your
``.. toctree::`` with anything you want, such as usage manuals or code samples.

### Q: What if I don't want to build `master`?

***A:*** As you may have seen, the Jenkins job clones the master branch of the
repository and builds the docs from there. However, you could also set up a
more robust system using the [Copy Artifact Plugin][8], where an upstream build
produces all artifacts necessary to build the documenation. Jenkins is capable
of some very powerful workflows!

### Q: Why do I get permissions errors when cloning the `master` branch?

***A:*** The `git clone` command inside the job's execute shell may not apply
the same SSH keys as the main `gh-pages` clone. You can turn on the [SSH Agent
Plugin][9] and
enable it in the job's "Build Environment" section to work around this.

### Q: Why not use [ReadTheDocs][10]?

***A:*** Please do! It is a fantastic service, and the inspiration for this
tutorial. However, the Jenkins + GitHub Pages duo will work in private [GitHub
Enterprise][11] environments and gives you full control over the doc building
process.

[1]: http://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example
[2]: http://icgood.github.io/continuous-docs/
[3]: http://www.virtualenv.org/en/latest/
[4]: https://pages.github.com/
[5]: http://sphinx-doc.org/latest/ext/intersphinx.html
[6]: https://pypi.python.org/pypi
[7]: http://sphinx-doc.org/rest.html
[8]: https://wiki.jenkins-ci.org/display/JENKINS/Copy+Artifact+Plugin
[9]: https://wiki.jenkins-ci.org/display/JENKINS/SSH+Agent+Plugin
[10]: https://readthedocs.org/
[11]: https://enterprise.github.com/home
