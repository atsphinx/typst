========
Overview
========

What is this
============

This is Sphinx extension to provide custom builders
that covert doctree to Typst document and PDF.

This will increase scenes using Sphinx for documentation.

About Typst
-----------

Typst is a new markup-based typesetting system for the sciences. [#1]_
It has easy syntax to learn and lightweight builder to generate PDF.

They design it to be alternative LaTeX.

.. [#1] https://typst.app/docs/

Motivation
==========

I publish "Tech-ZINE" [#2]_ using Sphinx and ``latexpdf`` builder.

.. [#2] It means non-commercial publications about engineerings.

Currently, Sphinx can create PDF document easily because it provides official docker image.
But, I think that it has some problems.

* Image size is too large.
* It is little hard to use image with other extensions.
* It is very hard to build without using docker image.

I want to create PDF as easy and low-layer as possible.
So, I try to adopt Typst as PDF builder that can run without container layer.

Goal
====

As above, this is personal project from private motivation.
But, I think that it should have goal of project.

I set three goals as milestone.

For v0.0.1
----------

On this version, it should be able to generate full-featured PDF of this project.

For v0.1.0
----------

On this version, it should be able to generate full-featured PDF of any own projects.

Example:

* sphinx-revealjs
* oEmbedPy

For v1.0.0
----------

On this version, it should be able to generate full-featured PDF of major Sphinx documentations.

* Sphinx

.. todo:: It is plan.
