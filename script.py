#!/usr/bin/python3
#Modules
import os
import sys
import subprocess

#######################  OPTIONS  #######################
max_number_of_sequences=1000



##1. Gather user input for taxonomic group and protein family
print("-------------------------------------------")
print("-------------------------------------------")
#pfam = input("Enter Protein Family:\n")
pfam = "glucose-6-phosphatase"
#pfam = "ABC transporters"

#taxo = input("Enter Taxonomic Group:\n")
taxo = "aves"
#taxo = "mammals"
print("-------------------------------------------")
print("-------------------------------------------")



##2. Gather desired protein sequences  (Include checks)
#2a. Query for taxonID
print("Gathering taxonID for " + taxo + "\n...")
esearchTaxoquery = "esearch -db taxonomy -spell -query \"" + taxo + "\" | efetch -format uid"
esearchTaxoUID = subprocess.check_output(esearchTaxoquery, shell=True).decode("utf-8").rstrip() #QUERY TAXONID
print("TAXONID: " + str(esearchTaxoUID) + "\n...\nGathered")

if (esearchTaxoUID == ""): #error check
  print("Invalid taxonomic group\nExiting program...")
  exit()
  
print("-------------------------------------------")

#2b. Query for protein sequences filtered with taxonID with :exp to get taxo subtree groups
print("Gathering protein sequences of " + pfam + " in " + taxo + " txid:" +esearchTaxoUID + "\n...")
esearchProtquery = "esearch -db protein -spell -query \"txid" + esearchTaxoUID + "[Organism:exp]" + " AND " + pfam + "[PROT]" + "\" | efetch -format fasta > seq.fasta"
esearchProtfasta = os.system(esearchProtquery)
print("Gathered")

#2c. Give user more information about queried sequences (no. of seq)
with open("seq.fasta") as infile:
  infileread = infile.read()
  seqcount = infileread.count(">")

print("Number of sequences gathered: " + str(seqcount))

if (seqcount == 0): #error check
  print("Invalid protein family\nExiting program...")
  exit()
elif (seqcount > max_number_of_sequences):
  print("Exceeds max number of sequences, " + str(max_number_of_sequences) + "\nExiting program...")
  exit()
  
print("-------------------------------------------")



#######info -db taxonomy -fields
#######need to use [Organism:exp] to get all associated taxID in subtree
#######einfo -db protein -fields


##3. CLUSTALO for alignment, EMBOSS for plotcon for sequence conservation



##4. Scan for PROSITE motifs in sequences



##5. Other EMBOSS analysis


