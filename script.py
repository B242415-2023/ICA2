#!/usr/bin/python3
#Modules
import os
import sys
import subprocess

#######################  OPTIONS  #######################
max_number_of_sequences=1000
availthreads = subprocess.check_output("nproc", shell=True).decode("utf-8").rstrip()

#######################  FUNCTIONS  #######################
#for calling bash commands for each individual sequence
def indivbash(bashline, outfileloci, outfileformat, dirorheader, goutfileformat =""):
  os.system("mkdir " + outfileloci)
  for header in seqheaders:
    with open("temp.fasta", "w") as infile:
      infile.write(seqdict.get(header))
    if (dirorheader == 1):
      try:
        headerfileformat = header.replace(">", "").replace(" ", "_").replace("[", "").replace("]", "").replace(",", "").replace(":", "")
        os.system(bashline + outfileloci + headerfileformat + outfileformat)
      except:
        print("Error with " + header)
    if (dirorheader == 2):
      try:
        headerfileformat = header.replace(">", "").replace(" ", "_").replace("[", "").replace("]", "").replace(",", "").replace(":", "")
        os.system(bashline + outfileloci + headerfileformat + outfileformat + " -goutfile " + outfileloci + headerfileformat + goutfileformat)
      except:
        print("Error with " + header)
    else:
      try:
        os.system(bashline + outfileloci + outfileformat)
      except:
        print("Error with " + header)

#######################  Folders  #######################
os.system("mkdir results")
os.system("mkdir temp")



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
#esearchTaxoquery = "esearch -db taxonomy -spell -query \"" + taxo + "\" | efetch -format uid"
#esearchTaxoUID = subprocess.check_output(esearchTaxoquery, shell=True).decode("utf-8").rstrip() #QUERY TAXONID
#print("Gathered" + "\nTAXONID: " + str(esearchTaxoUID) )

#if (esearchTaxoUID == ""): #error check
#  print("Invalid taxonomic group ?(Please avoid plurals)\nExiting program...")
#  exit()
  
print("-------------------------------------------")

#2b. Query for protein sequences filtered with taxonID with :exp to get taxo subtree groups
#print("Gathering protein sequences of " + pfam + " in " + taxo + " txid:" +esearchTaxoUID + "\n...")

#esearchProtquery = "esearch -db protein -spell -query \"txid" + esearchTaxoUID + "[Organism:exp]" + " AND " + pfam + "[PROT]" + "\" | efetch -format fasta > seq.fasta"
#esearchProtfasta = os.system(esearchProtquery)

print("Done")

#2c. Give user more information about queried sequences (no. of seq)
with open("seq.fasta") as infile:
  infileread = infile.read()
  seqcount = infileread.count(">")

print("Number of sequences gathered: " + str(seqcount))

if (seqcount == 0): #error check
  print("Invalid protein family (Please avoid plurals)\nExiting program...")
  exit()
elif (seqcount > max_number_of_sequences):
  print("Exceeds max number of sequences, " + str(max_number_of_sequences) + "\nExiting program...")
  exit() ################EDIT NEED TO MAKE IT SO PROGRAM WILL ASK IF WANT TO CONTINUE
  
  
###########GIVE OPTION AND INFO ABOUT SEQ SPECIES ORIGIN
  
print("-------------------------------------------")



#######info -db taxonomy -fields
#######need to use [Organism:exp] to get all associated taxID in subtree
#######einfo -db protein -fields


##3. CLUSTALO for alignment, EMBOSS for plotcon for sequence conservation plot
#3a. ClustalO
print("Aligning sequences via ClustalO with: " + availthreads + " threads\n...")

os.system("clustalo -i seq.fasta -o ./results/aligned.fasta --force --threads=" + str(availthreads))

print("Done")
print("-------------------------------------------")

#3b.  plotcon
print("Plotting convservation of sequence alignment\n...")

os.system("plotcon -sequences ./results/aligned.fasta -winsize=4 -graph png -sprotein1 -gdirectory results")

print("Done")
print("-------------------------------------------")



##4. Sequence data prep
print("Sequence data preparation\n...")
#4a. Separate sequences in seq.fasta
with open("seq.fasta") as infile:
  allseq = infile.read().rstrip().split(">")
  allseq.pop(0)
  allseq1 = [">" + seqelement for seqelement in allseq]

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

print("Done")
print("-------------------------------------------")

##5 Run patmatmotifs on each seq in allseq1 (Scan for PROSITE motifs in sequences patmatmotifs)
print("Scanning sequences for motifs\n...")

indivbash("patmatmotifs -auto -full -raccshow2 -rstrandshow2 -rusashow2 -rdesshow2 -rscoreshow2 -sequence temp.fasta -outfile ", "./results/motifs/", ".patmatmotifs", 1)

print("Done - Results in ./results/motifs/")
print("-------------------------------------------")



##6. EMBOSS Analysis 1 - sigcleave - signal sequence cleavage site
print("Scanning sequences for signal peptide cleavage sites\n...")
indivbash("sigcleave -rdesshow2 -rscoreshow2 -rusashow2 -auto -sequence temp.fasta -outfile " , "./results/sigcleave/", ".sigcleave", 1)
print("Done - Results in ./results/sigcleave/")
print("-------------------------------------------")

##7. EMBOSS Analysis 2 - charge - protein charge plot
print("Gathering protein charge\n...")
indivbash("charge -auto -seqall temp.fasta -outfile ", "./results/charge/", ".charge", 1)
print("Done - Results in ./results/charge/")
print("-------------------------------------------")

##8. EMBOSS Analysis 3 - freak - resuidue frequency plot
print("Plotting residue frequency\n...")
indivbash("freak -auto -graph svg -seqall temp.fasta -odirectory ", "./results/freak/", "", 0)
print("Done - Results in ./results/freak")
print("-------------------------------------------")

##9. EMBOSS Analysis 4 - helixturnhelix - helix turn helix motif searching for nucleic acid binding motifs
print("Scanning for nucleic acid binding site motifs\n...")
indivbash("helixturnhelix -sprotein1 -warning FALSE -rdesshow2 -auto -sequence temp.fasta -outfile ", "./results/helixturnhelix/", ".helixturnhelix", 1)
print("Done - Results in ./results/helixturnhelix")
print("-------------------------------------------")

##10. EMBOSS Analysis 5 - hmoment - calculate and plot hydrophobic moment 
print("Plotting hydrophobic moments\n...")
indivbash("hmoment -auto -seqall temp.fasta -graph svg -outfile ", "./results/hmoment/", ".hmoment", 2 , ".svg")
indivbash("hmoment -auto -seqall temp.fasta -graph svg -goutfile ", "./results/hmoment/", ".svg", 1)
print("Done - Results in ./results/hmoment")
print("-------------------------------------------")


##5. Other EMBOSS analysis


#########notes#############
########remove plurals
########## error trap for every step
#####if statement for different esearch filters, remove 'associated' predicted isoform partial
##########switch error checks to try, except       to catch all errors and outcomes
