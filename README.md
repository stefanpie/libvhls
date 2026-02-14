<img src="branding/logo_libvhls.svg" width="100%" alt="libvhls logo">
<hr>

🚧 This project is under construction 🏗️, updates to come... 🚧

## About

`libvhls` is a Python library to interface with the Vitis HLS tool and Vitis HLS projects.

`libvhls` provides APIs to extract structured information from Vitis HLS projects including source files, user pragmas, synthesis reports for resources and latency, synthesized HDL, design LLVMIR, and so on.

`libvhls` also provides APIs to call the Vitis HLS tool to create projects, manage source files, set design options, and run build commands such as synthesis, co-simulation, and export.

In the future, we hope to incorporate more experimental features such as the following:

- Interface to launch and monitor real-time synthesis runs
- "Out-of-Context" HLS synthesis for fast prototyping
- Auto testbench code and data generation from Python
- Complete support for extracting structured data from things like source code, logs, reports, scheduling data, biniding data, and intermidaite represenations (LLVMIR)
- Integration with other tools like the LightningSim / OmniSim simulator, DSE tools like FIFOAdvisor and OptDSL+AutoDSE, and QoR models
- Fine-grained control over synthesis including parallel and incremental synthesis, scheduling, binding, and RTL generation

This project is still under development and highly experimental. As we refine the library, we will provide official documentation and usage examples.

## Installation

```bash
uv add git+https://github.com/stefanpie/libvhls
```

```bash
pip install git+https://github.com/stefanpie/libvhls
```

## What's Included

`libvhls` has several components for users to use when building their own tools and projects.

- `VitisHLS` Tool Driver
  - The `VitisHLS` class provides an interface to execute commands and scripts via the Vitis HLS tool.
  - The embedded commands runner can extract structured information from the Vitis HLS output log such as error warnings for feedback to the user.
- `Command` classes that can be executed with `VitisHLS`.
  - This includes commands documented in the Vitis HLS user guide such as `OpenProject`, `CSim`, `Synth`, and `Export` commands.
- We also provide some custom convenience `Command` classes such as `UserTCL` to execute arbitrary TCL commands defined by the user.
- Users can also create their own `Command` classes to define custom commands.
- `Project` and `Solution` classes to load and represent Vitis HLS projects and solutions.
  - This includes C++ source files, pragma information, synthesis reports data, intermediated LLVMIR data, extracted scheduling information, extracted binding information, and synthesized HDL.
  - All the data is structured and documented via the library's typed Python API.

<!-- # Demos

## Design Space Exploration

## ML-Based Performance Prediction

## LLM Design Generation

## Scheduling Visualization

## DFG and CFG Extraction

## HW-SW Co-Design

## LLM Integration -->
