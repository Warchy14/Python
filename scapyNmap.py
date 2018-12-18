#encoding: utf-8
# coding: utf8
# -*- coding: utf-8 -*-
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from colorama import init,Fore,Style 
import time, os
init()

#Clear le cmd
os.system('cls')

print "\n"
print "--------------------------------------------------------------------------------"

print """

.______   .___  ___.      _______.  ______     ___      .______   ____    ____ 
|   _  \  |   \/   |     /       | /      |   /   \     |   _  \  \   \  /   / 
|  |_)  | |  \  /  |    |   (----`|  ,----'  /  ^  \    |  |_)  |  \   \/   /  
|   ___/  |  |\/|  |     \   \    |  |      /  /_\  \   |   ___/    \_    _/   
|  |      |  |  |  | .----)   |   |  `----./  _____  \  |  |          |  |     
| _|      |__|  |__| |_______/     \______/__/     \__\ | _|          |__|


                                   Git : Warchy14
                                                                               
"""
print "--------------------------------------------------------------------------------"
print "\n"

#Variables utilisateurs
hote = raw_input("IP to scan: ")

#Génère aléatoirement le port source
src_port = RandShort()
minPort = int(raw_input("Port min: "))
maxPort = int(raw_input("Port max: "))

#Début du processus
t1 = time.time()
nbrPort = 0

#Décoration
print "\n"
print "--------------------------------------------------------------------------------"

conf.verb = 0 # rendre non verbeux scapy

#Test des ports ouverts/fermés
for port in range(minPort,maxPort + 1 ):
    # Forge un paquet tcp de type sr1 avec flag S (Syn)
    tcp_connect_scan_resp = sr1(IP(dst=hote)/TCP(sport=src_port,dport=port,flags="S"),timeout=1)

    #Si port de type 'NoneType' alors port closed
    if(str(type(tcp_connect_scan_resp))=="<type 'NoneType'>"):
        print Fore.RED+"Port {}: Closed".format(port)
        print (Style.RESET_ALL)

    # Si couche TCP existe alors:      
    elif(tcp_connect_scan_resp.haslayer(TCP)):

        #Si le flag = 0x12 alors le port est Open
        if(tcp_connect_scan_resp.getlayer(TCP).flags == 0x12):
            # Forge un paquet tcp de type sr1 avec le flag AR (Ack, RST)
            send_rst = sr(IP(dst=hote)/TCP(sport=src_port,dport=port,flags="AR"),timeout=1)
            print Fore.GREEN+"Port {}: Open".format(port)
            print (Style.RESET_ALL)
            nbrPort = nbrPort + 1
            
        #Si le flag = 0x14 alors le port est closed        
        elif (tcp_connect_scan_resp.getlayer(TCP).flags == 0x14):
            print Fore.RED+"Port {}: Closed".format(port)
            print (Style.RESET_ALL)
            
        #Si couche TCP existe alors et le flag ne correspond pas à 0x12 ou 0x14 alors le port est closed
        else:
            print Fore.RED+"Port {}: Closed".format(port)
            print (Style.RESET_ALL)

#Fin du processus
t2 = time.time()

#Calcul différence de temps processus
diff = t2 - t1

#Décoration
print "--------------------------------------------------------------------------------"


#Affichage du temps du processus et le nombre de port(s) ouvert(s)

if nbrPort <= 1:
    print Fore.YELLOW+"Il y a " + str(nbrPort) + " port ouvert. Temps d'execution : %s secondes " % round(diff,1)
else:
    print Fore.YELLOW+"Il y a " + str(nbrPort) + " ports ouverts. Temps d'execution : %s secondes " % round(diff,1)
