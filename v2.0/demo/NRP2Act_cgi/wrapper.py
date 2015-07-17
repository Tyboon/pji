#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import cgitb
import cgi
import json
import re
import sys
import common


#Compte le nombre de séquence données
def count_sequences(seqdata):
    """ return the number of sequences contains in seqdata """
    return seqdata.count('>')

#Vérification du mail
def verif_mail(mail):
    """ check the validity of email address """

    res = mail.strip()
    if res.find(' ') > 0:
        return False
    a = res.find('@')
    if a <= 0:
        return False
    if res.find('@', a+1) > 0:
        return False
    return True

#Vérifie si les séquences sont au bon format
def valid_sequence(seq):
    """ check the validity of the sequence seq """

    if seq is None:
        return False

    pattern =  """
        ^                               # beginning of string
        (                               # one sequence 
        \ *>.+[\r\n]+                   # line of the name
        ([-\.\ atcgu0-9]+[\r\n]+)+      # line of the primary structure
        )+$                             # end of one sequence                  
        """
    if re.search(pattern, seq, re.VERBOSE) is None:
        return False
    else:
        return True

#Vérification si le format donné est bien fasta
def format_fasta(seq):
    try:
        list_seq = seq.splitlines()
        temp_seq = ''
    
        # remove spaces for non-title line
        for x in list_seq:
            if re.search('^ *>', x) is None:
                x = x.lower()
                x = x.strip()
            else:
                x = x.replace(' ', '_')
            temp_seq = temp_seq + x + '\n'

        return temp_seq
    except:
        return None


#Création du fichier fasta avec les séquences soumises
def create_fasta(run_id, seq):
    """ 
    create a fasta file with the sequences seq 
    """

    fasta_path = common.fasta_path_result(run_id)
    ffasta = open(fasta_path, 'w')
    seq_list = seq.split ('>')
    nb_seq = len(seq_list)
    name_seq = []
    for i in range(1, len(seq_list)):
        split_seq = seq_list[i].split('\n')
        name_seq.append(split_seq[0])
        ffasta.write('>' + split_seq[0] + '\n')
        for x in range(1, len(split_seq)):
            ch = re.sub('[ 0-9-]', '', split_seq[x])
            ffasta.write(ch)
	ffasta.write('\n')        
    ffasta.close()


#Fonction permettant de vérifier les données soumises dans le formulaire, retour dans un dictionnaire (req)
#Fonction qui sera modifiée pour le traitement de vos données
def extract_request(form):
    """ check the validity of the different fields of form """

    error_found = False
    error_messages = []
    req = {}
    
    #check the sequence name
    if form.has_key('seq_name') and len(form['seq_name'].value) is not 0:
        req["seq_name"] = form['seq_name'].value
    else:
        req["seq_name"] = None
        
    # if both "sequence" and "file" are filled => error
    if (form.has_key('sequence') and form.has_key('name_file')
        and not((len(form['sequence'].value.strip()) is 0) or 
                (len(form['file'].value) is 0))
        ):
        error_found = True
        error_messages.append('Paste sequences <strong>OR</strong>' +
                              'upload a file.')
       
    else:
        # if a file is uploaded
        if form.has_key('file') and not (len(form['file'].value) is 0):
            seq = form['file'].value
            
        # if sequences are given in the textarea "sequence"
        elif (form.has_key('sequence') and
              not (len(form['sequence'].value.strip()) is 0) ):
            seq = form['sequence'].value
        else:
            seq = None
            error_found = True
            error_messages.append('Missing sequences.')
            
        if seq is not None:
            # get the number of sequences, optional
            """nbseq = count_sequences(seq)

            if nbseq > 15:
                error_found = True
                error_messages.append('Too much sequences: Example does ' +
                                      'not accept <strong>more than 15 ' +
                                      'sequences.</strong>')
                
            # if just one sequence => error
            if nbseq < 2:
                error_found = True
                error_messages.append('Not enough sequences: Example ' +
                                      'requires <strong>at least 2 ' +
                                      'sequences.</strong>')"""

            # valid the sequence format
            seq = format_fasta(seq)
            seq_test = valid_sequence(seq)
 
            if not seq_test:
                error_found = True
                error_messages.append("Sequences are not in Fasta format")
            else:
                req["seq"] = seq
 
   #check radio button CG
    if form.has_key('GC'):
        req["GC"] = form.has_key("GC")
    else:
        req["GC"] = None

    #check choose of case
    if form.has_key('case'):
        req["case"] = form['case'].value
    else:
        req["case"] = None

   # check email value
    if not form.has_key('email'):
        req["email"] = None
    else:
        email = form['email'].value.strip()
        if email is not '':
            if not verif_mail(email):
                error_found = True
                error_messages.append('Invalid <strong>email ' +
                                      'address</strong>.')
            else:
                req["email"] = email
        else:
            req["email"] = None
                            
    req["error_messages"] = error_messages
    
    return req


#Lance le programme en fonction des données contenant dans req
#Fonction à modifier pour l'adapter à votre programme
def launch_software(run_id, req):
    if req["GC"]!=None:
        os.system("python example.py %s %s %s gc"%(common.RESULT_DIR+"/"+run_id+"/", run_id, req["case"]))
    else :
        os.system("python example.py %s %s %s"%(common.RESULT_DIR+"/"+run_id+"/", run_id, req["case"]))
    

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
        create_fasta(run_id, req['seq'])
        launch_software(run_id, req)

    return (error, error_page)



def main():
    fs = cgi.FieldStorage()
    
    error, error_page=process_request(fs)

    sys.stdout.write("Content-Type: application/json")

    sys.stdout.write("\n")
    sys.stdout.write("\n")

    result={}
    if error==0:
        result['success'] = True
        result['run_id'] = fs['run_id'].value
        result['path_result'] = common.HTML_PATH+"/result/"+fs['run_id'].value+"/results.php"
    else:
        result['success'] = False

    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")

main()
