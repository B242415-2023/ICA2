#!/usr/bin/python3
#Modules
import os
import sys
import subprocess

#######################  OPTIONS  #######################
max_number_of_sequences=1000
availthreads = subprocess.check_output("nproc", shell=True).decode("utf-8").rstrip()

#Folders
os.system("mkdir motifs")

##1. Gather user input for taxonomic group and protein family
print("-------------------------------------------")
print("-------------------------------------------")
#pfam = input("Enter Protein Family:\n")
pfam = "glucose-6-phosphatase"
#pfam = "ABC transporter"

#taxo = input("Enter Taxonomic Group:\n")
taxo = "aves"
#taxo = "mammals"
#pfam = "kinase"
#taxo = "rodents"
#pfam = "adenyl cyclases"
#taxo = "vertebrates"


print("-------------------------------------------")
print("-------------------------------------------")



##2. Gather desired protein sequences  (Include checks)
#2a. Query for taxonID
print("Gathering taxonID for " + taxo + "\n...")
esearchTaxoquery = "esearch -db taxonomy -spell -query \"" + taxo + "\" | efetch -format uid"
esearchTaxoUID = subprocess.check_output(esearchTaxoquery, shell=True).decode("utf-8").rstrip() #QUERY TAXONID
print("Gathered" + "\nTAXONID: " + str(esearchTaxoUID) )

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


##3. CLUSTALO for alignment, EMBOSS for plotcon for sequence conservation plot
#3a. ClustalO
print("Aligning sequences via ClustalO with: " + availthreads + " threads\n...")

os.system("clustalo -i seq.fasta -o aligned.fasta --force --threads=" + str(availthreads))

print("Aligned")
print("-------------------------------------------")

#3b.  plotcon
print("Plotting convservation of seuqnece alignment\n...")

os.system("plotcon -sequences aligned.fasta -winsize=4 -graph png -sprotein1")

print("Plotted")
print("-------------------------------------------")



##4. Scan for PROSITE motifs in sequences patmatmotifs
print("Scanning sequences for motifs\n...")
#4a. Separate sequences in seq.fasta
with open("seq.fasta") as infile:
  allseq = infile.read().rstrip().split(">")
  allseq1 = [">" + seqelement for seqelement in allseq.pop(0)]

#4bi. Create list of headers
seqheaders = []
for myseq in allseq1:
  headerend = myseq.find("\n")
  header = myseq[:headerend]
  seqheaders.append(header)
  
#4bii. Create dictionary of header:fasta
seqdict = {}
i=0
for header in seqheaders:
  seqdict[header] = allseq1[i]
  i=i+1
  
#4c. Run patmatmotifs on each seq in allseq1
for header in seqheaders:
  #print("Scanning: " + header)
  with open("temp.fasta", "w") as infile:
    infile.write(seqdict.get(header))
  headerfileformat = header.replace(">", "").replace(" ", "_").replace("[", "").replace("]", "").replace(",", "").replace(":", "")
  os.system("patmatmotifs -auto -full -rdesshow2 -rscoreshow2 -sequence temp.fasta -outfile ./motifs/" + headerfileformat + ".patmatmotifs")
  
print("Done. Results in ./motifs/")
print("-------------------------------------------")

#patmatmotifs -sequence seq.fasta -outfile motif.txt



##5. Other EMBOSS analysis


#########notes#############
########remove plurals
########## error trap for every step
#####if statement for different esearch filters, remove 'associated' predicted isoform partial
##########switch error checks to try, except       to catch all errors and outcomes
