# Benchmark Case: Watershed-Scale Big Spring

This directory contains all the necessary files to run a watershed-scale simulation of the Big Spring basin, a forested tributary to Sycamore Creek in Northern Arizona, USA.

This benchmark is designed to test the model's hydrologic routing, spatial processes, and mass balance at the basin scale. It includes separate input files for running the model in both **serial** and **parallel (MPI)** modes.

## 1. Prerequisites

Before running this simulation, please ensure you have a compiled tRIBS executable (v5.3.0 or later). For general instructions, please refer to the main [tRIBS Documentation](https://tribshms.readthedocs.io/en/latest/).

#### For Parallel Mode

To run the simulation in parallel, you must have:
1.  **OpenMPI** (or a similar MPI library) installed on your system.
2.  Compiled the **parallel version** of tRIBS, which requires enabling the MPI option during the CMake configuration. This typically produces a different executable (e.g., `tRIBSpar`).

## 2. How to Run the Simulation

The tRIBS model is executed from the command line. The commands differ for serial and parallel execution.

### Serial Mode

From within this directory (`watershed-scale-big-spring/`), run the serial simulation using the standard executable and the `big_spring.in` file:

```bash
/path/to/your/tRIBS/executable src/in_files/big_spring.in
```

### Parallel Mode

Run the parallel simulation using the `mpirun` command, your parallel tRIBS executable (e.g., `tRIBSpar`), and the `big_spring_par.in` file. The `-n` flag specifies the number of processors.

```bash
mpirun -n 3 /path/to/your/partRIBS/executable src/in_files/big_spring_par.in
```
**Note:** Both input files are configured with relative paths and will write model outputs into the `results/test/` directory.

## 3. How to Verify Your Results

After a simulation has successfully completed, you must return to the **root directory of the repository** to use the automated verification script. The command is different for each mode.

1.  Navigate back to the repository root:
    ```bash
    cd ../
    ```

2.  Run the appropriate verification command:

    *   To verify the **serial** run:
        ```bash
        python verification/verify.py watershed-scale-serial
        ```

    *   To verify the **parallel** run:
        ```bash
        python verification/verify.py watershed-scale-parallel
        ```

If your installation is correct, you will see a `[PASS]` message for all checks, confirming that your results match the official reference values.

## Input File Structure

*   **`data/`**: Contains all GIS and meteorological forcing data required to run this benchmark case.
*   **`src/in_files/`**: Contains the tRIBS input files for the serial (`big_spring.in`) and parallel (`big_spring_par.in`) runs.
*   **`results/test/`**: The designated output directory for your simulation runs. It is pre-configured in the `.gitignore` file.
