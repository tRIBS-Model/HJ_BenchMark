# verification/verify.py

import json
import math
import argparse
from pathlib import Path
import os
from contextlib import contextmanager

try:
    from pytRIBS.classes import Results
except ImportError:
    print("Error: pytRIBS is not installed. Please install it to run the verification script.")
    exit(1)

# =============================================================================
# SCRIPT CONFIGURATION
# =============================================================================
# Define the relative path to the official reference values file
REFERENCE_FILE = Path("doc/verification/generate/reference_values.json")
# Define the relative tolerance for floating-point comparisons
RELATIVE_TOLERANCE = 1e-3

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Map benchmark names to their root directories and input files
BENCHMARK_CONFIG = {
    "point-scale-happy-jack": {
        "root": Path("point-scale-happy-jack"),
        "in_file": "happy_jack.in"
    },
    "watershed-scale-serial": {
        "root": Path("watershed-scale-big-spring"),
        "in_file": "big_spring.in"
    },
    "watershed-scale-parallel": {
        "root": Path("watershed-scale-big-spring"),
        "in_file": "big_spring_par.in"
    }
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

@contextmanager
def working_directory(path):
    """A context manager that temporarily changes the working directory."""
    original_cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_cwd)

def calculate_user_water_balance(benchmark_root: Path, in_file_name: str) -> dict:
    """
    Calculates the water balance for the user's model run using pytRIBS.
    This function mirrors the logic from the generation script.
    """
    print(f"-> Analyzing your model output in '{benchmark_root}'...")
    relative_in_path = Path("src/in_files") / in_file_name

    with working_directory(benchmark_root):
        if not relative_in_path.exists():
            raise FileNotFoundError(f"Input file not found at: {benchmark_root / relative_in_path}")

        try:
            results = Results(str(relative_in_path))
            results.get_mrf_results()
            results.get_mrf_water_balance("full")
            water_balance_df = results.mrf['waterbalance']
            return water_balance_df.iloc[0].to_dict()
        except Exception as e:
            print(f"{RED}Error processing tRIBS output: {e}{RESET}")
            print(f"{YELLOW}Please ensure the model ran successfully and output files are in the correct location.{RESET}")
            exit(1)

# =============================================================================
# MAIN SCRIPT LOGIC
# =============================================================================

def main():
    """Main driver for the verification script."""
    parser = argparse.ArgumentParser(
        description="tRIBS Benchmark Verification Tool",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "benchmark_name",
        help="The name of the benchmark to verify.",
        choices=BENCHMARK_CONFIG.keys()
    )
    args = parser.parse_args()
    
    # 1. Load Reference Values
    if not REFERENCE_FILE.exists():
        print(f"{RED}Error: Reference file '{REFERENCE_FILE}' not found.{RESET}")
        print("Please ensure you are running this script from the root of the 'tRIBS-benchmarks' repository.")
        return

    with open(REFERENCE_FILE, 'r') as f:
        reference_data = json.load(f)

    reference_info = reference_data["benchmarks"].get(args.benchmark_name)
    if not reference_info:
        print(f"{RED}Error: Benchmark '{args.benchmark_name}' not found in reference file.{RESET}")
        return
        
    reference_values = reference_info["values"]
    print(f"Verifying benchmark '{args.benchmark_name}' against references for tRIBS v{reference_data['tRIBS_version']}...\n")

    # 2. Calculate Values from User's Run
    config = BENCHMARK_CONFIG[args.benchmark_name]
    user_values = calculate_user_water_balance(config["root"], config["in_file"])

    # 3. Compare Values and Print Results
    print("\nResults Comparison")
    all_passed = True
    
    # Sort keys for consistent output order
    sorted_keys = sorted(reference_values.keys())

    for key in sorted_keys:
        ref_val = reference_values.get(key)
        user_val = user_values.get(key)

        if ref_val is None or user_val is None:
            print(f"{YELLOW}Variable '{key}' could not be compared (missing from one of the results).{RESET}")
            all_passed = False
            continue

        # Use math.isclose for robust floating point comparison
        if math.isclose(ref_val, user_val, rel_tol=RELATIVE_TOLERANCE):
            status = f"{GREEN}[PASS]{RESET}"
        else:
            status = f"{RED}[FAIL]{RESET}"
            all_passed = False
        
        print(f"{key:<35} | Ref: {ref_val:<12.4f} | Yours: {user_val:<12.4f} | {status}")

    # 4. Print Final Summary
    print("--------------------------")
    if all_passed:
        print(f"\n{GREEN}Success! All checks passed.{RESET}")
        print("Your tRIBS installation appears to be working correctly for this benchmark.")
    else:
        print(f"\n{RED}Failure. One or more checks did not pass.{RESET}")
        print("Please review the differences above. Small discrepancies can sometimes occur due to compiler or OS differences.")
        print("If differences are large, please check your tRIBS installation and model setup.")

if __name__ == "__main__":
    main()