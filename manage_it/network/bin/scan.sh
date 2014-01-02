#!/bin/bash
# requires root privleges

#http://www.intrinium.com/Default.aspx?TabId=87&PostID=262
file_date=`date +%Y-%m-%d_%H-%M`
options="-sSUV --top-ports=15 -T4 -v -O --version-light --traceroute --script=ms-sql-info,nbstat,smb-os-discovery,snmp-sysdescr --script-args snmpcommunity=public"
networks="192.168.1.0/24 192.168.100.0/24 10.108.0.0/24"
file_path="/home/kamil/nmap"
xml_file_name="$file_path/$file_date.xml"

/usr/bin/nmap $options -oX=$xml_file_name $networks

# link to last and previous scan
prev="$file_path/previous.xml"
last="$file_path/last.xml"
rm $prev
readlink -f $last | xargs -I {} ln -s {} $prev
rm $last
ln -s $xml_file_name $last

#chown kamil:kamil $xml_file_name
