Python Continuous Documentation
===============================

## Introduction

So you've written your Python library and you were a good little developer,
keeping docstrings updated with [Sphinx formatting][1]. It's easy to get
started turning these docstrings into beautiful, hosted HTML, updated every
time you push to GitHub.

## Setting Up Your Project

### Installation

As always, I suggest using a [virtualenv][2] for local Python development!
Inside your virtualenv, run:

    pip install sphinx

### Setup

Create a `doc` directory in your project, we'll add it to git later:

    mkdir -p doc
    cd doc

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

    ``docpkg`` Package
    ==================

    .. automodule:: docpkg
       :members:

    -------------------

    **Sub-Modules:**

    .. toctree::

       docpkg.main
       docpkg.config

Now we're going to create two more files, `docpkg.main.rst` and
`docpkg.config.rst`.  I'll give you `docpkg.main.rst`, create
`docpkg.config.rst` the same way:

    ``docpkg.main`` Module
    ========================

    .. automodule:: docpkg.main
       :members:

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

    git add doc/requirements.txt doc/Makefile doc/source/conf.py doc/source/*.rst
    git commit

### Creating GitHub Pages Branch

GitHub will generate a [GitHub Pages](https://pages.github.com/) site for any
repository that has a `gh-pages` branch. Let's set ours up now:

    git checkout --orphan gh-pages
    git rm -rf .

Now add an `index.html` file and commit:

    touch index.html
    git add index.html
    git commit -m 'initial commit'

Obviously you'll want to replace this empty `index.html` with a real one at
some point. Eventually, we'll be creating a `latest/` subdirectory symlink that
will always point to the latest version of the docs. A good starting point
would be a simple redirect to `latest/`.

## Setting up Jenkins

This is where the magic happens. We will configure a Jenkins build to checkout
your `gh-pages` and `master` branches. Then, we will build the docs from
`master` directly into `gh-pages`. Finally, we will commit and push the
`gh-pages` branch using the "Git Publisher" post-build action.

Let's start with a free-style job.

### Cloning the Repositories

Choose "Multiple SCMs", so we can checkout both branches at once.

For the first Git SCM, fill in the Repository URL and set the branch specifier
to `*/gh-pages`.

For the second Git SCM, fill in the same Repository URL and leave the branch
specifier as `*/master`. Under "Additional Behaviours", choose "Check out to a
sub-directory and choose enter `master/`. Also add the "Wipe out repository &
force clone" option, to prevent building stale docs.

### Building the Docs

Add an "Execute shell" build step. In it, let's add some code:

    virtualenv .venv
    source .venv/bin/activate

    pip install -U -r master/doc/requirements.txt
    pip install -U master/

    git rm -rf .
    sphinx-build -b html master/doc/source/ .

    git commit -m "jenkins regenerated documentation $(date +%F)"

### Pushing to GitHub Pages

We've now built and committed our new docs to the `gh-pages` branch, but we
need to push it to GitHub before it will be rendered. Add a "Git Publisher"
post-build action:

* Push Only If Build Succeeds: ***&#x2713;***
* Add Branch:
  * Branch to push: `gh-pages`
  * Target remote name: `origin`

## Finishing Steps

You should now be able to try out your Jenkins build a few times, and see the
results on your projects Github Pages site. Try making some changes and
rebuilding. Cool, huh?

Before calling it done, you'll probably want to add a build trigger so that
this project is built automatically (otherwise it's not "continuous
documentation"). I recommend triggering the build after another job that runs
unit tests, but using a webhook directly from GitHub pushes works too.

## Frequently Asked Questions

### Q: How do I link to other projects?

***A:*** This is one of my favorite parts of Sphinx, the ability to link
directly to classes, functions, and modules in third-party projects on the
Internet. We can do this because we enabled the `intersphinx` extension, see
[its documentation][3] for its use.

### Q: Does my project meet the requirements?

***A:*** If you have a `setup.py` with an `install_requires` field to pull in
its own dependencies from [PyPi][4], that should be all you need!

### Q: Is it only for documenting code?

***A:*** Sphinx documentation is built using their heavily extended
[reStructuredText][5] markup. You can easily add items to your
``.. toctree::`` with anything you want, such as usage manuals or code samples.

[1]: http://pythonhosted.org/an_example_pypi_project/sphinx.html#full-code-example
[2]: http://www.virtualenv.org/en/latest/
[3]: http://sphinx-doc.org/latest/ext/intersphinx.html
[4]: https://pypi.python.org/pypi
[5]: http://sphinx-doc.org/rest.html
