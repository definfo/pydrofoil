Welcome to Pydrofoil's documentation!
=====================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


Pydrofoil is an experimental emulator-generator for ISA models written in
`Sail`__. It can generate emulators for RISC-V__, ARM__, CHERIoT__ based on
their respective Sail models. The Pydrofoil-generated emulators achieve fast
performance by doing dynamic binary translation (aka just-in-time compilation)
from guest instructions into host machine instructions. It's built on top of
the `RPython meta-jit compiler`__ and reuses all its optimizations, backends,
etc. Performance is typically an order of magnitude better than the emulators
generated by Sail.

To get started with the RISC-V emulator, please consult :doc:`building_pydrofoil`.

To read a more thorough description of how the project works, please refer to
our `2025 ECOOP paper`_. To cite this work, please use the following BibTex snippet:

.. code-block:: bibtex

    @InProceedings{bolztereick_et_al:LIPIcs.ECOOP.2025.3,
      author =	{Bolz-Tereick, CF and Panayi, Luke and McKeogh, Ferdia and Spink, Tom and Berger, Martin},
      title =	{{Pydrofoil: Accelerating Sail-Based Instruction Set Simulators}},
      booktitle =	{39th European Conference on Object-Oriented Programming (ECOOP 2025)},
      pages =	{3:1--3:31},
      series =	{Leibniz International Proceedings in Informatics (LIPIcs)},
      ISBN =	{978-3-95977-373-7},
      ISSN =	{1868-8969},
      year =	{2025},
      volume =	{333},
      editor =	{Aldrich, Jonathan and Silva, Alexandra},
      publisher =	{Schloss Dagstuhl -- Leibniz-Zentrum f{\"u}r Informatik},
      address =	{Dagstuhl, Germany},
      URL =		{https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2025.3},
      URN =		{urn:nbn:de:0030-drops-232962},
      doi =		{10.4230/LIPIcs.ECOOP.2025.3},
      annote =	{Keywords: Instruction set architecture, processor, domain-specific language, just-in-time compilation, meta-tracing}
    }

.. _`2025 ECOOP paper`: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECOOP.2025.3

.. toctree::
   :maxdepth: 1
   :hidden:

    Building Pydrofoil <building_pydrofoil>
    Using Pydrofoil <using_pydrofoil>
    Developing Pydrofoil <developing_pydrofoil>
    Background: Optimizations <background_optimizations>
    Arm <arm>
    CHERIoT <cheriot>
    Scripting API <scripting-api>
    Useful links <useful_links>

.. __: https://github.com/rems-project/sail
.. __: https://github.com/riscv/sail-riscv
.. __: https://github.com/rems-project/sail-arm
.. __: https://github.com/CHERIoT-Platform/cheriot-sail
.. __: https://www3.hhu.de/stups/downloads/pdf/BoCuFiRi09_246.pdf

..
    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
