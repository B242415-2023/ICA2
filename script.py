#!/usr/bin/python3
#Modules
import os
import sys
import subprocess



##1. Gather user input for taxonomic group and protein family
print("-------------------------------------------")
#pfam = input("Enter Protein Family:\n")
pfam = "glucose-6-phosphatase"
#pfam = "ABC transporters"

#taxo = input("Enter Taxonomic Group:\n")
taxo = "aves"
#taxo = "mammals"

print("-------------------------------------------")



##2. Gather desired protein sequences  (Include checks)
#2a. Query for taxonID
print("Gathering taxonID for " + taxo)
esearchTaxoquery = "esearch -db taxonomy -spell -query \"" + taxo + "\" | efetch -format uid"
esearchTaxoUID = subprocess.check_output(esearchTaxoquery, shell=True).decode("utf-8") #QUERY TAXONID
print("TAXONID: " + str(esearchTaxoUID))
#2b. Query for protein sequences filtered with taxonID with :exp to get taxo subtree groups
print("Gathering protein sequences of " + pfam + " in " + taxo + " txid:" +esearchTaxoUID + "...")
esearchProtquery = "esearch -db protein -spell -query \"txid" + esearchTaxoUID + "[Organism:exp]" + " AND " + pfam + "[PROT]" + "\" | efetch -format fasta > seq.fasta"
esearchProtfasta = os.system(esearchProtquery)
print("Gathered")
#2c. Give user more information about queried sequences (no. of seq)
with open("seq.fasta") as infile:
  infileread = infile.read()
  seqcount = infileread.count(">")

print("Number of sequences gathered: " + str(seqcount))
#2d. Check if empty. If empty, rerequest pfam and taxo



#######info -db taxonomy -fields
#######need to use [Organism:exp] to get all associated taxID in subtree
#######einfo -db protein -fields



##3. CLUSTALO for alignment, EMBOSS for plotcon for sequence conservation



##4. Scan for PROSITE motifs in sequences



##5. Other EMBOSS analysis


