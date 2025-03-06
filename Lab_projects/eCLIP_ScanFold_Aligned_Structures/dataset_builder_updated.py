import os
import requests

# ========================
# ENCODE API Configuration
# ========================

# Base URL for the ENCODE Project API
ENCODE_BASE_URL = "https://www.encodeproject.org"

# API endpoint for searching eCLIP experiments that are released and tagged with "ENCORE"
SEARCH_URL = f"{ENCODE_BASE_URL}/search/?type=Experiment&assay_title=eCLIP&status=released&internal_tags=ENCORE&format=json&limit=all"

# HTTP headers specifying JSON response format
HEADERS = {"Accept": "application/json"}

# ===========================
# File Paths & Directories
# ===========================

# Directory where eCLIP data will be stored
DATA_DIR = "ENCODE_eCLIP_data"

# Full path to the MANE IDs text file (needed for processing)
MANE_IDS_PATH = "/lustre/hdd/LAS/wmoss-lab/abdelraouf/eclip_YBX3/MANE_ids.txt"

# Full path to the script that processes downloaded eCLIP data
SCRIPT_PATH = "/lustre/hdd/LAS/wmoss-lab/abdelraouf/eclip_YBX3/eclip_str_extrac4.py"

# ===========================
# Function Definitions
# ===========================

def fetch_all_experiments():
    """
    Fetches all eCLIP experiments from the ENCODE database.
    
    Returns:
        list: A list of experiments (each represented as a dictionary).
    """
    response = requests.get(SEARCH_URL, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ ERROR: Failed to fetch ENCODE data. Status Code: {response.status_code}")
        return []
    
    data = response.json()
    return data.get("@graph", [])  # Return only the relevant list of experiments

def get_best_bed_file(exp_accession):
    """
    Finds the best available BED file for a given experiment.

    Args:
        exp_accession (str): The accession ID of the ENCODE experiment.

    Returns:
        dict or None: The metadata of the best BED file found, or None if no BED file is available.
    """
    exp_url = f"{ENCODE_BASE_URL}/experiments/{exp_accession}/?format=json"
    response = requests.get(exp_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ ERROR: Could not fetch {exp_accession}. Status Code: {response.status_code}")
        return None

    exp_data = response.json()
    all_files = exp_data.get("files", [])

    # Debug: Print all available files for this experiment
    print(f"\n📝 Files available for {exp_accession}:")
    for file in all_files:
        print(f"  - ID: {file.get('@id')}, Format: {file.get('file_format')}, Type: {file.get('file_format_type')}, Output: {file.get('output_type')}, HREF: {file.get('href')}")

    # Filter for BED files with narrowPeak format
    bed_files = [file for file in all_files if file.get("file_format") == "bed" and file.get("file_format_type") == "narrowPeak"]

    if not bed_files:
        print(f"⚠️ No BED files found for {exp_accession}")
        return None

    # Prioritize "optimal" peaks if available
    optimal_beds = [f for f in bed_files if "optimal" in f.get("output_type", "").lower()]

    if optimal_beds:
        return optimal_beds[0]  # Return the first optimal BED file

    return bed_files[0]  # Otherwise, return the first available BED file

def download_bed_file(file_metadata, cell_line, protein):
    """
    Downloads a BED file, extracts it, and generates a SLURM job script for processing.

    Args:
        file_metadata (dict): Metadata of the BED file to download.
        cell_line (str): The associated cell line.
        protein (str): The associated protein name.

    Returns:
        None
    """

    # Extract file URL from metadata
    file_url = f"{ENCODE_BASE_URL}{file_metadata['href']}"
    file_name = file_metadata["href"].split("/")[-1]  # Extract the filename from URL
    file_name_unzipped = file_name.replace(".gz", "")  # Name of the extracted file

    # Define the directory structure for storing the files
    save_path = os.path.join(DATA_DIR, cell_line, protein)
    os.makedirs(save_path, exist_ok=True)  # Ensure directory exists

    # Define full paths for downloaded and unzipped files
    full_file_path = os.path.join(save_path, file_name)
    full_unzipped_path = os.path.join(save_path, file_name_unzipped)

    # Check if the file is already extracted
    if os.path.exists(full_unzipped_path):
        print(f"✅ Unzipped file already exists: {full_unzipped_path}")
        return

    # Download the BED file
    print(f"⬇️ Downloading {file_name} -> {full_file_path}")
    
    with requests.get(file_url, stream=True) as response:
        if response.status_code == 200:
            with open(full_file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"✅ Download complete: {full_file_path}")
        else:
            print(f"❌ ERROR: Failed to download {file_url}")
            return

    # Extract the BED file
    os.system(f"gunzip -f {full_file_path}")
    print(f"✅ Unzipped: {full_unzipped_path}")

    # Define output and log file paths inside the correct folder
    output_file = os.path.join(save_path, f"{protein}_out.txt")
    log_file = os.path.join(save_path, f"{protein}_log.txt")

    # Define SLURM script path inside the correct folder
    slurm_script_path = os.path.join(save_path, f"run_{protein}.slurm")

    # Create the SLURM script content
    slurm_script_content = f"""#!/bin/bash

#SBATCH --time=10-00:00:00          # Maximum job runtime (10 days)
#SBATCH --cpus-per-task=1        # Request 1 CPU core
#SBATCH --nodes=1                  # Run on a single node
#SBATCH --partition=nova           # Partition to use
#SBATCH --mem=50G                 # Request 50 GB memory
#SBATCH -J "AZ-NEW-{protein}"       # Job name
#SBATCH --mail-user=raouf@iastate.edu  # Email notifications
#SBATCH --mail-type=BEGIN           # Notify when the job begins
#SBATCH --mail-type=END             # Notify when the job ends
#SBATCH --mail-type=FAIL            # Notify when the job fails
#SBATCH --hint=nomultithread        # Optimize for non-hyperthreaded CPUs
#SBATCH -C "intel&avx512"

# Load Conda environment
module load micromamba
eval "$(micromamba shell hook --shell=bash)"
micromamba activate /lustre/hdd/LAS/wmoss-lab/programs/envs/ScanFold2

# Run the processing script
python {SCRIPT_PATH} {full_unzipped_path} {output_file} {log_file} {MANE_IDS_PATH}

echo "Job completed successfully."
"""

    # Write the SLURM script to a file
    with open(slurm_script_path, "w") as slurm_file:
        slurm_file.write(slurm_script_content)

    print(f"✅ SLURM script created: {slurm_script_path}")

    # Submit the SLURM job
    os.system(f"sbatch {slurm_script_path}")
    print(f"✅ SLURM job submitted: {slurm_script_path}")

# ===========================
# Main Execution
# ===========================

def main():
    """
    Main function to fetch eCLIP experiments, download BED files, and submit SLURM jobs.
    """
    experiments = fetch_all_experiments()
    
    if not experiments:
        print("⚠️ No experiments found. Exiting...")
        return

    print(f"✅ Found {len(experiments)} eCLIP experiments!")

    for experiment in experiments:
        exp_accession = experiment.get("accession")
        cell_line = experiment.get("biosample_ontology", {}).get("term_name", "Unknown")
        protein = experiment.get("target", {}).get("label", "Unknown")

        print(f"\n🔹 Processing {protein} in {cell_line}")

        best_bed_file = get_best_bed_file(exp_accession)
        if best_bed_file:
            download_bed_file(best_bed_file, cell_line, protein)
        else:
            print(f"⚠️ No BED files found for {exp_accession}")

if __name__ == "__main__":
    main()

