#!/bin/bash

# 查找所有的.sra文件并输出
find . -type f -name "*.sra" > sra_files_list.txt
echo "Found SRA files:"
cat sra_files_list.txt

# 等待用户确认
read -p "Are these files correct? (y/n) " -n 1 -r
echo    # 新行
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # 处理从 sourced 脚本或 subshell 中的退出
fi

# 创建rawdata目录
mkdir -p rawdata

# 读取文件名并进行处理
while IFS= read -r sra_file; do
  echo "Processing $sra_file"
  
  # 判断是单端还是双端测序
  lines=$(fastq-dump.2.8.2 -X 1 --split-spot -Z "$sra_file" | wc -l)
  
  # 根据行数决定如何处理
  if [ "$lines" -eq "4" ]; then
    echo "$sra_file is single-end"
    fastq-dump --outdir rawdata "$sra_file"
  elif [ "$lines" -eq "8" ]; then
    echo "$sra_file is paired-end"
    fastq-dump --split-3 --outdir rawdata "$sra_file"
  else
    echo "Unexpected format for $sra_file"
  fi
done < sra_files_list.txt

echo "All files have been processed."
