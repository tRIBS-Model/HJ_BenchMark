# Benchmark Case: Point-Scale Happy Jack

This directory contains all the necessary files to run a point-scale simulation of the [Happy Jack SNOTEL Site](https://wcc.sc.egov.usda.gov/nwcc/site?sitenum=969) in Northern Arizona, USA.

This benchmark is designed to test the vertical soil moisture and energy balance components of the tRIBS model[^1]<sup>,</sup>[^2].

## 1. Prerequisites

Before running this simulation, please ensure you have a compiled tRIBS executable (v5.3.0 or later). For instructions on compiling the model from source or using the Docker image, please refer to the main [tRIBS Documentation](https://tribshms.readthedocs.io/en/latest/).

## 2. How to Run the Simulation

The tRIBS model is executed from the command line. From within this directory (`point-scale-happy-jack/`), you can run the simulation using the following command structure:

```bash
/path/to/your/tRIBS/executable src/in_files/happy_jack.in
```
**Note:** The provided input file (`happy_jack.in`) is configured with relative paths. By default, it will write all model outputs into the `results/test/` directory.

## 3. How to Verify Your Results

After the simulation has successfully completed, you must return to the **root directory of the repository** to use the automated verification script.

1.  Navigate back to the repository root:
    ```bash
    cd ../
    ```

2.  Run the verification script, specifying the `point-scale-happy-jack` benchmark:
    ```bash
    python verification/verify.py point-scale-happy-jack
    ```

If your installation is correct, you will see a `[PASS]` message for all checks, confirming that your results match the official reference values.

## Input File Structure

*   **`data/`**: Contains all GIS and meteorological forcing data required to run this benchmark case.
*   **`src/in_files/`**: Contains the main tRIBS input file (`happy_jack.in`). This is the file you can modify to explore different model parameters and options.
*   **`results/test/`**: The designated output directory for your simulation runs. It is pre-configured in the `.gitignore` file to prevent model outputs from being tracked by Git.

## References

[^1]: Sun N, H Yan, M Wigmosta, R Skaggs, R Leung, and Z Hou. 2019. “Regional snow parameters estimation for large-domain hydrological applications in the western United States.” Journal of Geophysical Research: Atmospheres. doi: 10.1029/2018JD030140

[^2]: Yan H, N Sun, M Wigmosta, R Skaggs, Z Hou, and R Leung. 2018. “Next-generation intensity-duration-frequency curves for hydrologic design in snow-dominated environments.” Water Resources Research, 54(2), 1093–1108.
BCQC Data Format
