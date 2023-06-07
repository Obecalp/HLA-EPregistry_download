#!/usr/bin/bash



#get_It:  create the a case with the name in $1 if not existent, download website page adress in arg 1, create a txt file containing all exposition/verification data, then run Extract_Eplet to create a csv specific to the website page
function get_It {
	if [ ! -e $1 ] 
		then 
		mkdir "$1"
		fi
	 wget "-O" "$1/$1.html" "$2"

grep "-Ei" "<td>|href=\"\#myModalReport" "$1/$1.html" | grep "-v" "<small" | sed "-e" "s/&nbsp;//g" | sed "-e" "s/<[^>]*>//g" > "$1/tempo.txt" 

#run Extract_eplet with html and txt file, put the corrupted allele in the logs.
./Extract_eplet.py "$1/$1.html" "$1/tempo.txt" "$1/$1.csv" > "$1/last_log.txt"
}

#some different eplet have same name in different website pages, replace rename them with _X where X is the HLA.
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

#merge the five files (I bet you didn't guess it) in a temporary csv, exlude the double, then name it as update_dd_mm_yyyy
./merge.py "tempo.csv" "ABC/ABC.csv" "DR/DR.csv" "DP/DP.csv" "DQ/DQ.csv" "interlocus/interlocus.csv"

cat "tempo.csv" | uniq > "update_$date.csv"
rm "tempo.csv"
rm "communs.txt"
