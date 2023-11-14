#!/usr/bin/python3
#Modules
import os
import sys
import subprocess



##1. Gather user input for taxonomic group and protein family
pfam = input("Enter Protein Family:\n")
taxo = input("Enter Taxonomic Group:\n")



##2. Gather desired protein sequences  (Include checks)
#2a. Query for taxonID
esearchTaxoquery = "esearch -db taxonomy -spell -query \"" + taxo + "\" | efetch -format uid"
esearchTaxoUID = subprocess.check_output(esearchTaxoquery, shell=True).decode("utf-8") #QUERY TAXONID
print("TAXONID: " + str(esearchTaxoUID))
#2b. Query for protein sequences
esearchProtquery = "esearch -db protein -spell -query \"" + pfam + "\" | efetch -format "




#einfo -db taxonomy -fields
#######need to use [Organism:exp] to get all associated taxID in subtree
#########einfo -db protein -fields



##3. CLUSTALO for alignment, EMBOSS for plotcon for sequence conservation



##4. Scan for PROSITE motifs in sequences



##5. Other EMBOSS analysis


