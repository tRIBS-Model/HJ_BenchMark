# tRIBS Official Benchmark Cases

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.17088973)

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

For example:
```bash
cd watershed-scale-big-spring
# Follow the instructions in watershed-scale-big-spring/README.md to run the model
```
The model will generate output files in the results/ subdirectory within the benchmark folder.

### Step 3: Verify Your Results

After the simulation is complete, return to the root directory of this repository. We provide an automated Python script to compare your model's output against the official reference values.

Run the verify.py script, specifying which benchmark you ran.
Example Usage:

To verify your results for the **serial watershed** run:
```bash
python doc/verification/verify.py watershed-scale-serial
```
To verify your results for the **point scale** run:
```bash
python doc/verification/verify.py watershed-scale-serial
```
**Expected Output**

The script will analyze your results and provide a clear, color-coded summary.

**On success, you will see a message like this:**
```bash
Verifying benchmark 'watershed-scale-serial' against references for tRIBS v5.3.0...

-> Analyzing your model output in 'watershed-scale-big-spring'...

--- Comparison Results ---
Total Change in Storage (mm)        | Ref: 9.3000        | Yours: 9.3000        | [PASS]
Total Evapotranspiration (mm)       | Ref: 650.8000      | Yours: 650.8000      | [PASS]
Total Precipitation (mm)            | Ref: 1250.2000     | Yours: 1250.2000     | [PASS]
Total Runoff (mm)                   | Ref: 590.1000      | Yours: 590.1000      | [PASS]
--------------------------

Success! All checks passed.
Your tRIBS installation appears to be working correctly for this benchmark.
```


---

## Advanced Analysis and Visualization

The `doc/` directory contains additional Jupyter Notebooks that were used in previous versions for plotting and analysis. These can be used for a more in-depth visual comparison of your results.

## For Maintainers

The official `reference_values.json` file can be updated by running the `doc/verification/generate_references.py` script. This should only be done after a new set of results has been generated following an official tRIBS model update.
