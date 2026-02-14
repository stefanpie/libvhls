Welcome to libvhls's documentation!
===================================

`libvhls` is a Python library to interface with the Vitis HLS tool and Vitis HLS projects.

`libvhls` provides APIs to extract structured information from Vitis HLS projects including source files, user pragmas, synthesis reports for resources and latency, synthesized HDL, design LLVMIR, and so on.

`libvhls` also provides APIs to call the Vitis HLS tool to create projects, manage source files, set design options, and run build commands such as synthesis, co-simulation, and export.

In the future, we hope to incorporate more experimental features such as the following:

- Interface to launch and monitor real-time synthesis runs
- Integration of the LightningSim simulator
- Fine-grained control over synthesis including parallel and incremental synthesis, scheduling, binding, and RTL generation

This project is still under development and highly experimental. As we refine the library, we will provide official documentation and usage examples.

.. toctree::
   :maxdepth: 4
   :caption: Contents:
   
   api/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
