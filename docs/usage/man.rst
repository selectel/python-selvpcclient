======
selvpc
======


SYNOPSIS
========

  `selvpc` [options] <command> [command-options]

  `selvpc help`

  `selvpc help` <command>


DESCRIPTION
===========

`selvpc` is a command line client for the Selectel VPC.
It implements 100% of the API, allowing management of projects,
resources, quotas and much more.


OPTIONS
=======

To get a list of available commands and options run::

    selvpc help
    selvpc help

To get usage and options of a command run::

    selvpc help <command>
    selvpc help <command>


EXAMPLES
========

List created projects::

    selvpc project list

List added subnets::

    selvpc subnet list
