# Tools
## 1.Extract.PY
Extract the relationship between ID and gene symbol from the annotation of the platform



## 2.convert_sra_to_fastq.sh

### Purpose
This script is designed to automate the conversion of SRA files to FASTQ format. It performs the following tasks:
- Searches for all `.sra` files in the current directory and its subdirectories.
- Prompts the user to confirm the list of found SRA files before proceeding.
- Determines whether the sequencing data is single-end or paired-end.
- Converts the SRA files using `fastq-dump --split-3` based on the sequencing type without multi-threading.
- Stores the converted FASTQ files in a directory named `rawdata`.

### How to Use
1. Place `convert_sra_to_fastq.sh` in the root directory where your `.sra` files are located.
2. Make sure you have `fastq-dump` installed and accessible in your PATH.
3. Give the script execution permissions with the command:
   'chmod +x convert_sra_to_fastq.sh'
4. Run the script:
   './convert_sra_to_fastq.sh'
5. Confirm the list of SRA files when prompted.
6. The script will create a `rawdata` directory and store the converted files there.

Please ensure you have sufficient disk space and permissions to create and write to the `rawdata` directory.

### Notes
- The script assumes that `fastq-dump` is the version 2.8.2 or higher.
- Ensure that the SRA files do not contain additional segments, as the script checks for single-end (4 lines) or paired-end (8 lines) sequencing data.
- The script will not delete the intermediary file list (`sra_files_list.txt`), which you may want to remove manually after the conversion.

