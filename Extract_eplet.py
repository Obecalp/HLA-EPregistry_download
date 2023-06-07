#!/usr/bin/env python3

import sys
import csv





#Part of affine: DPB1*10:123Q -> 10123
def allele_find(relation,allele):
	sortie=''						
	compteur=0
	for caractere in allele:
		compteur=compteur+1
		if caractere=="*":
			break
	for i in range(compteur,len(allele)):
		try:
			if allele[i] != ':':
				sortie+=str(int(allele[i]))
		except ValueError:
			continue
	if len(sortie)<4:
		return None
	return sortie

#Part of Affine(): Collect HLA of an allele (A,B,C...): DPB1*10:123->DPB1
def HLA_find(relation,HLA):
	if ("DR" not in HLA) and ("DQ" not in HLA) and("DP" not in HLA) and("A" not in HLA) and("B" not in HLA) and ("C" not in HLA):
		print("erreur groupe HLA à la relation: Epitope: ",relation," Allele: ",HLA)
	if "DR" in HLA:
		if "DRB1" in HLA: return "DR"
		else: return None
	elif "DQ" in HLA:
		if "DQA1" in HLA: return "DQA1"
		if "DQB1" in HLA: return "DQ"
		else: return None
	elif "DP" in HLA:
		if "DPB1" in HLA: return "DP"
		else: return None
	elif "A" in HLA: return "A"
	elif "B" in HLA: return "B"
	elif "C" in HLA: return "C"
	else: return None

# Input: allele as C*10:123 as given on the website Eplet registry. Output: ['C','10123'] Exclude every HLA group non used by HLA-EPI as DRB2, DQA2 etc...
#If the allele is corrupted, don't return it then return an error with the eplet and the corrupted allele.

def Affine(eplet,liste): 			
	Alleles=[]
	Allele=[]
	for data in liste:
		Corrupt= False
		if HLA_find(eplet,data) == '' or HLA_find(eplet,data) == None:
			Corrupt=True
		Allele.append(HLA_find(eplet,data))
		if allele_find(eplet,data) == '' or allele_find(eplet,data) == None:
			Corrupt=True
			print("erreur Allele à la relation: Epitope: ",eplet," Allele: ",data)
		Allele.append(allele_find(eplet,data))
		if Corrupt==False: Alleles.append(Allele)
		Allele=[]
	return Alleles


#begin the research of the allele list corresponding to the eplet found at the line 'position' in the page html 'liste'
def seek_item(quote,liste,position):
	for line in range(len(liste)-position):
		if quote in liste[position+line]:
			inter=liste[position+line+1].replace(' ','')
			query=inter.split(",")
			query[0]=query[0].split(">")[1]
			for verification in range(len(query)):
				if "<" in query[verification]:
					query.remove(query[verification])
			return query




table_html=[]
paire=[]
databank=[]
html_file= open(sys.argv[1],"r") 
var=''

Allalleles=[]


for i in html_file:
	table_html.append(i)


#step1: find every eplet using the quote "HLA alleles..."
#step2: use seek_item to return the allele list in the next line "Liste of all..)
#step3: append both in a paire, then append the paire to databank as [[eplet1,[allele1,allele2,...],[eplet2,[allele1,allele2,...]]]
for i in range(len(table_html)):
	if "HLA alleles that share the eplet" in table_html[i]:
		for mot in range(len(table_html[i].split(" "))):
			if table_html[i].split(" ")[mot]=='eplet':
				var=table_html[i].split(" ")[mot+1]
		Eplet=var.split("<")[0]
		paire.append(Eplet)
		AllAllelesbrut=seek_item("List of all (Luminex® or not) HLA alleles",table_html,i)
		AllAlleles=Affine(Eplet,AllAllelesbrut)
		paire.append(AllAlleles)
		databank.append(paire)
		paire=[]

html_file.close()

#Using the tempo.txt file, extract all position/exposition data

entry=[]
sub_entry=[]
sortie=[]
file_v1 = open(sys.argv[2])
file_v2 = [i.split('\n')[0].replace(' ','') for i in file_v1]
for i in range(len(file_v2)):
	if len(file_v2[i])>1 and  file_v2[i].isdigit()==False: 
		sub_entry.append(file_v2[i])
	elif file_v2[i].isdigit()==True: 
		if len(sub_entry)>0: entry.append(sub_entry)
		sub_entry=[]
entry.append(sub_entry)
liste=[]
sublist=[]

#warning: currently (06/06/2023) there isn't information about exposition for the interlocus eplet on Eplet registry, "true" is used currently by default.
for i in entry:
	if sys.argv[1] != "interlocus/interlocus.html":
		if "Intermediate" in i[1]: sublist.append("t")
		if "High" in i[1]: sublist.append("t")
		if "Low" in i[1]:
			sublist.append("f")
		if len(i)>2 and i[2]=="Yes": sublist.append("t")
		else: sublist.append("f")
		if len(sublist)>0: liste.append(sublist)
		sublist=[]
	else:	

		sublist.append("t")
		if len(i)>1 and i[1]=="Yes": sublist.append("t")
		else: sublist.append("f")
		if len(sublist)>0: liste.append(sublist)
		sublist=[]
file_v1.close()


HLA_CSV=[]
row=[]

#combine Exposition/verification and allele list
for i in range(len(databank)):
	for j in databank[i][1]:
		
		row.append(j[0])
		row.append(j[1])
		row.append(databank[i][0])
		row.append(liste[i][0])
		row.append(liste[i][1])
		HLA_CSV.append(row)
		row=[]


with open(sys.argv[3],'w',newline='') as fichier_CSV:
			trans= csv.writer(fichier_CSV, delimiter=';')
			for i in range(len(HLA_CSV)):
				trans.writerow([str(HLA_CSV[i][0]),str(HLA_CSV[i][1]),str(HLA_CSV[i][2]),str(HLA_CSV[i][3]),str(HLA_CSV[i][4])])
