# tRIBS Official Benchmark Cases

This repository provides a set of official benchmark cases for the tRIBS (TIN-based Real-time Integrated Basin Simulator) distributed hydrological model. Its primary purpose is to allow users to:

1.  **Validate a new tRIBS installation** by ensuring it can replicate official results.
2.  **Provide standardized example datasets** for learning how to set up and run tRIBS simulations.

This repository is designed to be a companion to the main [tRIBS model source code repository](https://github.com/tRIBS-Model/tRIBS).

## Available Benchmarks

This repository contains the input files for the following benchmark simulations:

*   **`point-scale-happy-jack/`**: A single-point simulation at the Happy Jack SNOTEL site in Arizona. This case is ideal for testing the model's vertical soil moisture and energy balance components.
*   **`watershed-scale-big-spring/`**: A full watershed simulation for the Big Spring basin. This case is designed to test the model's hydrologic routing, spatial processes, and mass balance at the basin scale. It includes input files for both **serial** and **parallel (MPI)** model runs.

## Quickstart: How to Verify Your tRIBS Installation

Follow these steps to run a benchmark and verify that your tRIBS installation is producing correct results.

### Step 1: Prerequisites

Before you begin, ensure you have the following:

*   A successful compilation and installation of the tRIBS model.
*   A Python 3 environment.
*   The [pytRIBS](https://github.com/tRIBS-Model/pytRIBS) Python package and its dependencies.

### Step 2: Run a Benchmark Simulation

Navigate into one of the benchmark directories. Each directory contains a specific `README.md` with detailed instructions on how to execute the tRIBS simulation for that case.
