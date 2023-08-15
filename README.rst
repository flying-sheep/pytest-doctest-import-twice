pytest reproducer
=================

When using the following together, pytest 7.4.0 creates multiple instances of modules instead of reusing already-executed ones.
The bug triggers in pytest’s collection phase.

Necessary for the bug to trigger:

- ``--import-mode=importlib`` (I’m sure it’s also possible with ``append`` in another way)
- ``--doctest-modules``
- no ``src/`` layout
- importing from a submodule.

Run with e.g.

.. code:: bash

   hatch run pytest
   # or if you like typing
   python -m virtualenv .venv; source .venv/bin/activate; pip install -e .; pytest

No matter if you opt to install in dev mode like this, specify ``PYTHONPATH``,
or install regularly, the bug is reproducible in any case.

how it works
------------

The module in ``__init__.py`` gets created and executed twice,
but when each instance executes ``from .singleton import MyVindictiveSingleton``,
that reuses the same instance of the submodule.

.. code:: mermaid

   flowchart LR
   A[__init__.py] -->|imports| C(singleton.py)
   B[__init__.py] -->|imports| C(singleton.py)

tracebacks
----------

The two tracebacks are almost identical, but show that a cached version of a submodule is used
(fewer ``frozen importlib._bootstrap`` frames).

It’s also possible to put some code in ``conftest.py`` or a plugin and have the second execution there.

.. code:: pytb

   File "<venv>/lib/python3.11/site-packages/_pytest/pathlib.py", line 538, in import_path
     spec.loader.exec_module(mod)  # type: ignore[union-attr]
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
   File "<proj>/pytest_doctest_import_twice/__init__.py", line 1, in <module>
     from .singleton import MyVindictiveSingleton
   File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
   File "<frozen importlib._bootstrap>", line 1128, in _find_and_load_unlocked
   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
   File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
   File "<frozen importlib._bootstrap>", line 1149, in _find_and_load_unlocked
   File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
   File "<proj>/pytest_doctest_import_twice/__init__.py", line 3, in <module>
     instance = MyVindictiveSingleton()
                ^^^^^^^^^^^^^^^^^^^^^^^


.. code:: pytb

   File "<venv>/lib/python3.11/site-packages/_pytest/pathlib.py", line 538, in import_path
     spec.loader.exec_module(mod)  # type: ignore[union-attr]
     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   File "<frozen importlib._bootstrap_external>", line 940, in exec_module
   File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
   File "<proj>/pytest_doctest_import_twice/__init__.py", line 3, in <module>
     instance = MyVindictiveSingleton()
                ^^^^^^^^^^^^^^^^^^^^^^^
