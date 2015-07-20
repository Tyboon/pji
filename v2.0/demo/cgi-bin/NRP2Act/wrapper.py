#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cgitb
import cgi
import json
import re
import sys
import common



#Fonction permettant de vérifier les données soumises dans le formulaire, retour dans un dictionnaire (req)
#Fonction qui sera modifiée pour le traitement de vos données
def extract_request(form):
    """ check the validity of the different fields of form """

    error_found = False
    error_messages = []
    req = {}
    
    #check the sequence name
    if form.has_key('decompo') and len(form['decompo'].value) is not 0:
        req["decompo"] = form['decompo'].value
    else:
        req["decompo"] = None
        error_found = True
        error_messages.append('Paste sequences <strong>OR</strong>' )
       
            
    req["error_msg"] = error_messages
    
    return req


#Lance le programme en fonction des données contenant dans req
#Fonction à modifier pour l'adapter à votre programme
def launch_software(run_id, req):
        #os.system("python example.py %s %s %s"%(common.RESULT_DIR+"/"+run_id+"/", run_id, req["case"]))
    	#TODO
	sys.stdout.write("COUCOU LAUNCH_SOFTWARE") 
	

#Vérifie si il n'y a pas d'erreur au retour des données soumises par le formulaire
def process_request(form):
    run_id = form['run_id'].value
    error=0
    error_page=""
    req = extract_request(form)
    
    if len(req["error_messages"])>0:
        error_page=req["error_messages"]
        error=1
    else :
        launch_software(run_id, req)

    return (error, error_page)



def main():
	form = cgi.FieldStorage()
    
	if form.has_key('command'):
		if form['command'].value == 'request':
			common.content_html()
			run.process_request(form,nom)
		elif form['command'].value == 'result':
			common.content_html()
			results.retrieve_results(form)
		else:
			common.content_html()
			common.error_page('invalid command')
	else:
		common.content_html()
		common.index_page()
	  


main()
