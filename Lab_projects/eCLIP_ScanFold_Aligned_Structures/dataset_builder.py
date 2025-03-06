import os
import requests

# --------------------------------------------------------------------------------------
# 📌 ENCODE API Constants
# --------------------------------------------------------------------------------------
# ENCODE is a publicly available project that provides genome-wide experimental data.
# The script queries ENCODE to fetch eCLIP experiment data with specific filters.
ENCODE_BASE_URL = "https://www.encodeproject.org"
SEARCH_URL = f"{ENCODE_BASE_URL}/search/?type=Experiment&assay_title=eCLIP&status=released&internal_tags=ENCORE&format=json&limit=all"
HEADERS = {"Accept": "application/json"}

# --------------------------------------------------------------------------------------
# 📌 Directories and Paths
# --------------------------------------------------------------------------------------
# DATA_DIR: Directory where downloaded eCLIP data will be stored
# MANE_IDS_PATH: Full path to the MANE gene IDs file (used for downstream processing)
# SCRIPT_PATH: Full path to the script that will process extracted BED files
DATA_DIR = "ENCODE_eCLIP_data"
MANE_IDS_PATH = "/lustre/hdd/LAS/wmoss-lab/abdelraouf/eclip_YBX3/MANE_ids.txt"
SCRIPT_PATH = "/lustre/hdd/LAS/wmoss-lab/abdelraouf/eclip_YBX3/eclip_str_extrac4.py"


# --------------------------------------------------------------------------------------
# 📌 Function: fetch_all_experiments()
# 📌 Purpose: Query ENCODE API to fetch all available eCLIP experiments.
# --------------------------------------------------------------------------------------
def fetch_all_experiments():
    """Fetches all eCLIP experiments from ENCODE that match our search criteria."""
    response = requests.get(SEARCH_URL, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"❌ ERROR: Failed to fetch ENCODE data. Status Code: {response.status_code}")
        return []
    
    # Parse and return the experiment data
    data = response.json()
    return data.get("@graph", [])  # "@graph" contains the list of experiments


# --------------------------------------------------------------------------------------
# 📌 Function: get_best_bed_file()
# 📌 Purpose: Given an experiment accession, find the best BED file to use.
# --------------------------------------------------------------------------------------
def get_best_bed_file(exp_accession):
    """Finds the best available BED file for an experiment, prioritizing 'optimal' peaks."""
    
    # Construct API URL to fetch details about the experiment
    exp_url = f"{ENCODE_BASE_URL}/experiments/{exp_accession}/?format=json"
    response = requests.get(exp_url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ ERROR: Could not fetch {exp_accession}. Status Code: {response.status_code}")
        return None

    exp_data = response.json()
    all_files = exp_data.get("files", [])
    
    # Debugging: List all available files for this experiment
    print(f"\n📝 Files available for {exp_accession}:")
    for file in all_files:
        print(f"  - ID: {file.get('@id')}, Format: {file.get('file_format')}, Type: {file.get('file_format_type')}, Output: {file.get('output_type')}, HREF: {file.get('href')}")

    # Filter for BED files with "narrowPeak" format
    bed_files = [file for file in all_files if file.get("file_format") == "bed" and file.get("file_format_type") == "narrowPeak"]

    if not bed_files:
        print(f"⚠️ No BED files found for {exp_accession}")
        return None

    # Prioritize "optimal" peak BED files
    optimal_beds = [f for f in bed_files if "optimal" in f.get("output_type", "").lower()]
    
    # Return the best available BED file
    return optimal_beds[0] if optimal_beds else bed_files[0]


# --------------------------------------------------------------------------------------
# 📌 Function: download_bed_file()
# 📌 Purpose: Download the BED file, extract it, and generate a SLURM script to process it.
# --------------------------------------------------------------------------------------
def download_bed_file(file_metadata, cell_line, protein):
    """Downloads and extracts the BED file, then submits a SLURM job to process it."""

    # Extract BED file URL and filename
    file_url = f"{ENCODE_BASE_URL}{file_metadata['href']}"
    file_name = file_metadata["href"].split("/")[-1]
    file_name_unzipped = file_name.replace(".gz", "")

    # Define the directory structure: DATA_DIR/{cell_line}/{protein}/
    save_path = os.path.join(DATA_DIR, cell_line, protein)
    os.makedirs(save_path, exist_ok=True)

    full_file_path = os.path.join(save_path, file_name)
    full_unzipped_path = os.path.join(save_path, file_name_unzipped)

    # If the unzipped file already exists, skip re-downloading
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

    # Extract the downloaded file
    os.system(f"gunzip -f {full_file_path}")  
    print(f"✅ Unzipped: {full_unzipped_path}")

    # Define output and log filenames
    output_file = f"{protein}_out.txt"
    log_file = f"{protein}_log.txt"

    # --------------------------------------------------------------------------------------
    # 📌 SLURM Job Script Creation
    # --------------------------------------------------------------------------------------
    # A SLURM script is generated dynamically for each experiment and submitted for execution.
    slurm_script_path = os.path.join(save_path, f"run_{protein}.slurm")

    slurm_script_content = f"""#!/bin/bash

#SBATCH --time=10-00:00:00          
#SBATCH --cpus-per-task=1        
#SBATCH --nodes=1                  
#SBATCH --partition=nova           
#SBATCH --mem=50G                 
#SBATCH -J "AZ-NEW-{protein}"       
#SBATCH --mail-user=raouf@iastate.edu  
#SBATCH --mail-type=BEGIN           
#SBATCH --mail-type=END             
#SBATCH --mail-type=FAIL            
#SBATCH --hint=nomultithread        
#SBATCH -C "intel&avx512"

# Load Conda and activate the environment
module load micromamba
eval "$(micromamba shell hook --shell=bash)"
micromamba activate /lustre/hdd/LAS/wmoss-lab/programs/envs/ScanFold2

python {SCRIPT_PATH} {full_unzipped_path} {output_file} {log_file} {MANE_IDS_PATH}

echo "Job completed successfully."
"""

    # Write the SLURM script to a file
    with open(slurm_script_path, "w") as slurm_file:
        slurm_file.write(slurm_script_content)
    
    print(f"✅ SLURM script created: {slurm_script_path}")

    # **🚀 Submit the SLURM script automatically**
    os.system(f"sbatch {slurm_script_path}")
    print(f"✅ SLURM job submitted: {slurm_script_path}")


# --------------------------------------------------------------------------------------
# 📌 Main Script Execution
# 📌 Purpose: Fetch eCLIP experiments, get the best BED file, and process it.
# --------------------------------------------------------------------------------------
def main():
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

