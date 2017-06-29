Client command extension support
================================

The client command extension adds support for extending the selvpc client while
considering ease of creation.

Precedence of command loading
------------------------------

* hard coded commands are loaded first
* external commands (installed in the environment) are loaded then

Commands that have the same name will be overwritten by commands that are
loaded later. To change the execution of a command for your particular
extension you only need to override the execute method.


selvpc.commands entry_point
---------------------------

To activate the commands in a specific extension module, add an entry in
setup.cfg under selvpc.commands. For example::

    [entry_points]
    selvpc.commands =
        awesome = contrib.commands.awesome