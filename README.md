# HLA-EPregistry_download
Upload eplet-data from HLA-Eplet-registry

# Introduction

This project come in addition of HLA-EPI_Bash (https://github.com/Obecalp/HLA-EPI_Bash-edit) and aim to upload required eplets data to run it from HLA Eplet Registry (https://epregistry.com.br/index/databases/database/ABC). 


This project don't aim to be long term, the script is strongly dependant of the website structure, and any redesign would be susceptible make it obsolete. Still, it's entirely functionnal thee 07/06/2023

# Dependencies

There isn't any meaningfull dependencies, only basic libraries are used (csv,sys)

# Input

There isn't any input, all 3 file (Extract_Eplete, multiplet.sh, merge.sh) must be in the same case, then the user only has to run multiplet.sh with a cup of cofee


# Data information

As said in the introduction, the data targeted concern Eplet-allele relation combined with eplet information.

All data are not required for HLA-EPI, so only a part of the data will be downloaded:
- The alleles downloaded are A,B,C,DQA1,DQB1,DRB1,DPB1. These are the considered as the most pertinent for HLA-EPI usage.
- The Exposition data is converted  in boolean, High/Intermediate become Exposed, Very Low/Low become false
- The section Luminex + non luminex allele is downloaded, but the "only luminex" section won't be. Still, all alleles concerned will be downloaded.



# Output

A csv file dated is created containing all data required for HLA-EPI as update_dd_mm_yyyy.csv. The format data is "HLA;allele;exposition;verification" for exemple C;0101;t;t

For more clarity five more case are created, one for each website page concerned by HLA-EPI (ABC,DQ,DP,DR,interlocus). They contain:
- The html page used to extract the data
- the "tempo.txt" file used to extract exposition/verification
- the log containing all corrupted alleles encounter. The Eplet name and the allele are in the file.
- the csv  specific to the website page



