#encoding: utf-8
import socket
import sys
import os
from colorama import init,Fore,Style 
from datetime import datetime
init()

print """

-------------------------------------------------------------------------------------------------------------------
|                                                                                                                 |
|                                                           PPPPPPPPPPPPPPPPP   MMMMMMMM               MMMMMMMM   |
|                                                            P::::::::::::::::P  M:::::::M             M:::::::M  |
|                                                            P::::::PPPPPP:::::P M::::::::M           M::::::::M  |
|                                                            PP:::::P     P:::::PM:::::::::M         M:::::::::M  |
| nnnn  nnnnnnnn       mmmmmmm    mmmmmmm     aaaaaaaaaaaaa     P::::P     P:::::PM::::::::::M       M::::::::::M |
| n:::nn::::::::nn   mm:::::::m  m:::::::mm   a::::::::::::a    P::::P     P:::::PM:::::::::::M     M:::::::::::M |
| n::::::::::::::nn m::::::::::mm::::::::::m  aaaaaaaaa:::::a   P::::PPPPPP:::::P M:::::::M::::M   M::::M:::::::M |
| nn:::::::::::::::nm::::::::::::::::::::::m           a::::a   P:::::::::::::PP  M::::::M M::::M M::::M M::::::M |
| n:::::nnnn:::::nm:::::mmm::::::mmm:::::m    aaaaaaa:::::a   P::::PPPPPPPPP    M::::::M  M::::M::::M  M::::::M   |
| n::::n    n::::nm::::m   m::::m   m::::m  aa::::::::::::a   P::::P            M::::::M   M:::::::M   M::::::M   |
| n::::n    n::::nm::::m   m::::m   m::::m a::::aaaa::::::a   P::::P            M::::::M    M:::::M    M::::::M   |
| n::::n    n::::nm::::m   m::::m   m::::ma::::a    a:::::a   P::::P            M::::::M     MMMMM     M::::::M   |
| n::::n    n::::nm::::m   m::::m   m::::ma::::a    a:::::a PP::::::PP          M::::::M               M::::::M   |
| n::::n    n::::nm::::m   m::::m   m::::ma:::::aaaa::::::a P::::::::P          M::::::M               M::::::M   |
| n::::n    n::::nm::::m   m::::m   m::::m a::::::::::aa:::aP::::::::P          M::::::M               M::::::M   |
| nnnnnn    nnnnnnmmmmmm   mmmmmm   mmmmmm  aaaaaaaaaa  aaaaPPPPPPPPPP          MMMMMMMM               MMMMMMMM   |
|                                                                                                                 |
|                                                                                                                 |
|                                       Author : Pierre-Marie Quantin                                             |
|                                       Year   : 17/12/2018                                                       |
|                                                                                                                 |
 -----------------------------------------------------------------------------------------------------------------|                                                                                                              
                                                                                                               
                                                                                                            
"""
#Variables utilisateurs
hote = raw_input("IP to scan: ")
minPort = int(raw_input("Port min: "))
maxPort = int(raw_input("Port max: "))

#Dictionnaire des ports connus
myDico = {
    "80": "HTTP",
    "443" : "HTTPS"
}

#Début du processus
t1 = datetime.now()

#Test des ports ouverts/fermés
try:
    for port in range(minPort,maxPort + 1 ):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((hote, port))
        # Si résultat = 0 alors le port est ouvert
        if result == 0:
            print Fore.GREEN+"Port {}: Open".format(port)
            print (Style.RESET_ALL)
            
        #Sinon le port est fermé
        else:
            print Fore.RED+"Port {}: Close".format(port)
        sock.close()

except socket.error:
    print "Erreur..."
    sys.exit()

#Fin du processus
t2 = datetime.now()

#Calcul différence de temps processus
diff = t2 -t1

#Affichage du temps du processus
print Fore.WHITE+"time elapsed: " + str(diff)
