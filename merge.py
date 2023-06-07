#!/usr/bin/env python3

import sys
import csv

def extract(csvFile):
	entree=[]
	with open(csvFile,'r', newline='') as data:
		banque=csv.reader(data,delimiter=';')
		for row in banque:
			entree.append(row)
		matrice=[[i.strip('"').strip('/').strip('=').strip('"') for i in ligne] for ligne in entree]
	data.close()
	return matrice
donnee=[]

for i in range(2,len(sys.argv)):
	donnee.append([ligne for ligne in extract(sys.argv[i])])

with open(sys.argv[1],'w',newline='') as fichier:
		trans= csv.writer(fichier, delimiter=';')
		trans.writerow(['hla','allele','epitope','exposed','verified'])
		for matrice in range(len(donnee)):
			for ligne in range(len(donnee[matrice])):
				trans.writerow([str(donnee[matrice][ligne][0]),str(donnee[matrice][ligne][1]),str(donnee[matrice][ligne][2]),str(donnee[matrice][ligne][3]),str(donnee[matrice][ligne][4])])


fichier.close()
