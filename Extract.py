import re
import csv

def extract_probe_gene_relationships_to_csv(file_path, output_file_path, pattern):
    relationships = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if pattern in line and 'RefSeq' in line:
                parts = line.split('\t')
                if len(parts) > 1:
                    probe_id = parts[0].strip()
                    # 在包含RefSeq的字段中查找基因symbol
                    refseq_part = next((part for part in parts if 'RefSeq' in part), None)
                    if refseq_part:
                        gene_symbol_match = re.search(r'\(([^)]+)\)', refseq_part)
                        if gene_symbol_match:
                            gene_symbol = gene_symbol_match.group(1)
                            relationships.append((probe_id, gene_symbol))

    with open(output_file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Probe ID', 'Gene Symbol'])  # 写入标题行
        for probe_id, gene_symbol in relationships:
            writer.writerow([probe_id, gene_symbol])

    return output_file_path

# 使用示例
input_path = 'C:\\Users\\Dr Cui\\Downloads\\GPL23159-69552.txt'
output_path = 'C:\\Users\\Dr Cui\\Downloads\\probe_gene_relationships.csv'
pattern = 'ZCCHC'

extract_probe_gene_relationships_to_csv(input_path, output_path, pattern)
