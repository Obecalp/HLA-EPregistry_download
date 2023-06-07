#!/usr/bin/bash



#get_It: telecharge la page en argument 1, la formate pour la rendre utilisable par Extract_Eplet et crée un fichier csv portant le nom en $1 dans un dossier $1 (le crée si non existant)
function get_It {
	if [ ! -e $1 ] 
		then 
		mkdir "$1"
		fi
	 wget "-O" "$1/$1.html" "$2" #exemple si ABC en argument 1: télécharge le lien et nomme le fichier ABC.html
#formatage de la page html pour ne laisser que les ID,Eplet,exposition,confirmation(Yes/' ') et stocke le résulta dans "tempo.txt"

grep "-Ei" "<td>|href=\"\#myModalReport" "$1/$1.html" | grep "-v" "<small" | sed "-e" "s/&nbsp;//g" | sed "-e" "s/<[^>]*>//g" > "$1/tempo.txt" 
#exécution d'Extract_eplet avec la page html et tempo.txt, stocke les log dans last_log.txt
./Extract_eplet.py "$1/$1.html" "$1/tempo.txt" "$1/$1.csv" > "$1/last_log.txt"
}

function replace {
	for i in $(cat "communs.txt")
	do
	sed "-i" "s/$i\;/$i\_$1;/g" "$1/$1.csv"
	done
	}

get_It "ABC" "https://epregistry.com.br/index/databases/database/ABC"
get_It "DQ" "https://epregistry.com.br/index/databases/database/DQ"
get_It "DP" "https://epregistry.com.br/index/databases/database/DP"
get_It "DR" "https://epregistry.com.br/index/databases/database/DRB"
get_It "interlocus" "https://epregistry.com.br/index/databases/database/DRDQDP"

cut "-d" ';' "-f" "3" "ABC/ABC.csv" | uniq | grep "-wE" "$(cut "-d" ';' '-f' "3" "DR/DR.csv" | uniq)" > "communs.txt"
cut "-d" ';' "-f" "3" "ABC/ABC.csv" | uniq | grep "-wE" "$(cut "-d" ';' '-f' "3" "DQ/DQ.csv" | uniq)" >> "communs.txt"
cut "-d" ';' "-f" "3" "ABC/ABC.csv" | uniq | grep "-wE" "$(cut "-d" ';' '-f' "3" "DP/DP.csv" | uniq)" >> "communs.txt"
cut "-d" ';' "-f" "3" "DP/DP.csv" | uniq | grep "-wE" "$(cut "-d" ';' '-f' "3" "DR/DR.csv" | uniq)" >> "communs.txt"
cut "-d" ';' "-f" "3" "DP/DP.csv" | uniq | grep "-wE" "$(cut "-d" ';' '-f' "3" "DQ/DQ.csv" | uniq)" >> "communs.txt"
cut "-d" ';' "-f" "3" "DQ/DQ.csv" | uniq | grep "-wE" "$(cut "-d" ';' '-f' "3" "DR/DR.csv" | uniq)" >> "communs.txt"

replace "ABC"
replace "DQ"
replace "DP"
replace "DR"

date=$(date "+%d_%m_%Y")
#fusion des 4 fichier csv en un fichier csv sous le format update_jj_mm_aaaa.csv
./merge.py "tempo.csv" "ABC/ABC.csv" "DR/DR.csv" "DP/DP.csv" "DQ/DQ.csv" "interlocus/interlocus.csv"

cat "tempo.csv" | uniq > "update_$date.csv"
rm "tempo.csv"
rm "communs.txt"
