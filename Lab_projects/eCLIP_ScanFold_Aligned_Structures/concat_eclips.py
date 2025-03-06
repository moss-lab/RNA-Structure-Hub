import sys
import os
import pandas as pd
import logging  # Import logging module

# ===============================
# Setup Logging Configuration
# ===============================

# Log file path
log_file = "processing.log"

# Configure logging to track errors and progress
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# ===============================
# Define Directory & Variables
# ===============================

# Root directory containing the output files from the previous script
dir = "ENCODE_eCLIP_data_missing10eclips"

# List to store individual DataFrames before merging
dataframes = []

# List of columns used for merging (ensuring consistency across files)
merge_columns = [
    "ENST_ID", "Chrom", "strand", "trans_start", "trans_end",
    "Sequence", "Refolded_Structure", "Refolded_MFE",
    "Refolded_z-score", "Refolded_ED"
]

# ===============================
# Process Each File in Directory
# ===============================

# Iterate through all cell line directories inside the root directory
for cell_line in os.listdir(dir):
    cell_line_path = os.path.join(dir, cell_line)

    # Ensure the path is a directory (not a file)
    if os.path.isdir(cell_line_path):

        # Iterate through protein type directories inside the cell line directory
        for protien_type in os.listdir(cell_line_path):
            protien_type_path = os.path.join(cell_line_path, protien_type)

            # Ensure the path is a directory (not a file)
            if os.path.isdir(protien_type_path):

                # Iterate through all files in the protein type directory
                for file in os.listdir(protien_type_path):

                    # Process only files that end with "_out.txt"
                    if file.endswith("_out.txt"):
                        file_path = os.path.join(protien_type_path, file)

                        try:
                            # Read the tab-separated file into a pandas DataFrame
                            df = pd.read_csv(file_path, sep="\t")

                            # Add metadata columns for "Cell Line" and "Protein Type"
                            df["Cell Line"] = cell_line
                            df["Protein Type"] = protien_type

                            # Reorder columns to ensure consistency
                            df = df[
                                [
                                    "ENST_ID", "Chrom", "strand", "trans_start", "trans_end",
                                    "Sequence", "Refolded_Structure", "Refolded_MFE",
                                    "Refolded_z-score", "Refolded_ED", "Cell Line", "Protein Type"
                                ]
                            ]

                            # Append processed DataFrame to the list
                            dataframes.append(df)

                            # Log successful processing of the file
                            logging.info(f"Processed: {file_path}")

                        except Exception as e:
                            # Log errors encountered while processing the file
                            logging.error(f"Error processing {file_path}: {e}")

# ===============================
# Merge All DataFrames
# ===============================

# Concatenate all collected DataFrames into a single dataset
final_df = pd.concat(dataframes, ignore_index=True).drop_duplicates()

# Group by unique identifiers while aggregating "Protein Type" values
final_df = final_df.groupby(
    merge_columns + ["Cell Line"], as_index=False
).agg({
    "Protein Type": lambda x: ", ".join(set(x.dropna()))  # Combine all unique protein types for each entry
})

# ===============================
# Save the Final Merged Dataset
# ===============================

# Define output file path inside the original directory
output_file = os.path.join(dir, "final_merged_data.csv")

# Save the merged dataset as a CSV file
final_df.to_csv(output_file, index=False)

# Log final output file location
logging.info(f"Final merged dataset saved: {output_file}")

# Print success message to the console
print(f"\nProcess complete. Log file: {log_file}")

