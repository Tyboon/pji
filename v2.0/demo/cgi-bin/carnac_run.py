#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import random
import os
import sys
import traceback
import re
import glob
import thread
import resource
import pickle
import subprocess
import cgitb
import cgi
import json

import carnac_common as cc
import results as c_res
cgitb.enable()

def count_sequences(seqdata):
    """ return the number of sequences contains in seqdata """
    return seqdata.count('>')


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
            # get the number of sequences
            nbseq = count_sequences(seq)

            if nbseq > 15:
                error_found = True
                error_messages.append('Too much sequences: CARNAC does ' +
                                      'not accept <strong>more than 15 ' +
                                      'sequences.</strong>')
                
            # if just one sequence => error
            if nbseq < 2:
                error_found = True
                error_messages.append('Not enough sequences: CARNAC ' +
                                      'requires <strong>at least 2 ' +
                                      'sequences.</strong>')

            # valid the sequence format
            seq = format_fasta(seq)
            seq_test = valid_sequence(seq)
 
            if not seq_test:
                error_found = True
                error_messages.append("Sequences are not in Fasta format")
            else:
                req["seq"] = seq
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
    req["GC"] = form.has_key("GC")
    req["threshold"] = form.has_key("threshold")

    
    return (error_found, req)


def create_fasta(run_id, seq):
    """ 
    create a fasta file with the sequences seq 
    """

    fasta_path = cc.fasta_path(run_id)
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
    
    return (nb_seq, name_seq)

def resume_request(run_id, req):
    pend_path = cc.pending_file(run_id)
    fpend = open(pend_path, "wb")
    pickle.dump(req, fpend)
    fpend.close()

def convert_files(run_id, carnac_dir):
    prevdir = os.path.abspath(os.getcwd())
    os.chdir(carnac_dir)
    
    exist_structure = False
    for res_file in os.listdir(carnac_dir):
        res_file_abs = os.path.join(carnac_dir, res_file)        
        (shortname, extension) = os.path.splitext(res_file)
        
        if extension == '.ct':
            fct = open(res_file_abs, 'r')
            content = fct.read()
            fct.close()
            content = content.splitlines()
            for j in range(1, len(content)):
                tab = content[j].split(' ')
                if re.search('^0$', tab[4]) is None:
                    exist_structure = True
                    
            if exist_structure:    
                # ct2forced
                os.system('perl ' + cc.CT2FORCED + ' ' + shortname)
                # ct2parenthesis
                os.system('perl ' + cc.CT2PARENTHESIS +  ' ' + shortname)
                # naview
                os.system(cc.NAVIEW + ' ./' + shortname + ' o < ' + 
                          cc.DEFAULT_NAV + ' >/dev/null')
                # plt22ps
                os.system(cc.PLT22PS + ' -p' + ' ' + shortname + ' >/dev/null')
                # gs
                os.system('gs -sDEVICE=jpeg -sOutputFile=' + shortname +
                          '.jpeg -q -dBATCH '+  shortname + '.ps >/dev/null')
                
    os.chdir(prevdir)

def launch_gardenia(run_id, tmp_dir, sequences):
    pcomment = '\ *>.+[\r\n]+'
    pprimary = '([-\.\ atcgu0-9]+[\r\n]+)+'
    comment = re.compile(pcomment)
    primary = re.compile(pprimary)

    alignment = os.path.join(tmp_dir, "alignment.fa")
    stdout = cc.stdout_path(run_id, "gardenia")
    stderr = cc.stderr_path(run_id, "gardenia")
    cmd_path = cc.command_path(run_id, "gardenia")

    # test if there are some structures
    fseq = open(sequences, "r")
    test = False
    new_seq = False
    size = 0
    for line in fseq:
        if comment.search(line):
            new_seq = True
            if size > 2500:
                return ""
            size = 0
        if primary.search(line):
            size += len(line)
        if line.find("(") != -1:
            test = True
            break

    if not test:
        return ""

    command = "%s %s -s --fasta -o %s" % (cc.GARDENIA, sequences, alignment)
    fcmd = open(cmd_path, 'w')
    fcmd.write(command)
    fcmd.close()

    fstderr = open(stderr, 'w')
    fstdout = open(stdout, 'w')

    retcode = subprocess.call(command, stderr=fstderr, stdout=fstdout,
                              shell=True)
                                      
    fstderr.close()
    fstdout.close()

    return alignment

def launch_rnafold(run_id, tmp_dir):
    results = []

    cmd = "%s -noPS -C "

    for sequence in glob.glob(os.path.join(tmp_dir, "carnac/*.bra")):
        seq_filename = sequence.split('/')[-1]
        seq_name = seq_filename.split('.')[0]

        cmd_path = cc.command_path(run_id, "rnafold_" + seq_name)
        stderr = cc.stderr_path(run_id, "rnafold_" + seq_name)
        result = os.path.join(tmp_dir, "rnafold_" + seq_filename)

        command = cmd % (cc.RNAFOLD)
        fcmd = open(cmd_path, 'w')
        fcmd.write(command)
        fcmd.close()
        fstderr = open(stderr, 'w')
        fstdout = open(result, 'w')
        fstdin = open(sequence, "r")

        retcode = subprocess.call(command, stderr=fstderr, stdout=fstdout,
                                  stdin=fstdin, shell=True)
        fstderr.close()
        fstdout.close()
        fstdin.close()
        results.append(result)

    return results

def launch_carnac(run_id, req):
    archive_files = []
    res_dir = cc.result_dir(run_id)
    tmp_dir = cc.tmp_dir(run_id)
    #pend_path = cc.pending_file(run_id)
    stdout = cc.stdout_path(run_id, "carnac")
    stderr = cc.stderr_path(run_id, "carnac")
    cmd_path = cc.command_path(run_id, "carnac")
    fasta_path = cc.fasta_path(run_id)
    carnac_dir = os.path.join(tmp_dir, "carnac")
    
    if req["GC"]:
        if req["threshold"]:
            command = "%s -A -i 98 -s 0 -o %s %s" %(cc.CARNAC, tmp_dir, fasta_path)
        else:
            command = "%s -A -i 100 -s 0 -o %s %s" %(cc.CARNAC, tmp_dir, fasta_path)
    else:
        if req["threshold"]:
            command = "%s -i 98 -s 0 -o %s %s" %(cc.CARNAC, tmp_dir, fasta_path)
        else:
            command = "%s -i 100 -s 0 -o %s %s" %(cc.CARNAC, tmp_dir, fasta_path)
    fcmd = open(cmd_path, 'w')
    fcmd.write(command)
    fcmd.close()

    fstderr = open(stderr, 'w')
    fstdout = open(stdout, 'w')

    retcode = subprocess.call(command, stderr=fstderr, stdout=fstdout,
                              shell=True)
                                      
    fstderr.close()
    fstdout.close()

    if retcode != 0:
        return

    align_path = launch_gardenia(run_id, tmp_dir, 
                                 os.path.join(tmp_dir, "carnac.out"))


    os.system("cp %s %s"%(os.path.join(tmp_dir, "carnac.out"),
                          os.path.join(res_dir, "sequences.fasta")))

    #os.system("cp %s %s"%(pend_path, res_dir))
    os.system("cp %s %s"%(stdout, res_dir))
    if os.path.isfile(align_path):
        cmd = "%s -i fasta -w -M 55 %s %s"%(cc.DISPLAY_ALIGNMENTS, align_path, 
                                            res_dir)
        stderr = os.path.join(tmp_dir, "display_alignment.err")
        stdout = os.path.join(tmp_dir, "display_alignment.out")
        fstderr = open(stderr, "w")
        fstdout = open(stdout, "w")
        retcode = subprocess.call(cmd, stderr=fstderr, stdout=fstdout,
                                  shell=True)
        fstderr.close()
        fstdout.close()
        os.system("cp %s %s"%(align_path, res_dir))
        archive_files.append(align_path)

    convert_files(run_id, carnac_dir)
    results = launch_rnafold(run_id, tmp_dir)
    for result in results:
        os.system("cp %s %s"%(result, res_dir))
        archive_files.append(result)

    for res_file in os.listdir(carnac_dir):
        res_file_abs = os.path.join(carnac_dir, res_file)        
        (shortname, extension) = os.path.splitext(res_file)
        os.system("cp %s %s"%(os.path.join(carnac_dir, res_file),
                              os.path.join(res_dir, res_file)))
        archive_files.append(os.path.join(res_dir, res_file))
        
    archive_files.append(os.path.join(res_dir, "sequences.fasta"))
    cc.add_to_archive(run_id, archive_files)
    
    #os.remove(pend_path)
    
    if req["email"] is not None:
        mailer.send_success_mail(run_id, req["email"])
    
def stock_parameter(run_id, req):
    res_dir = cc.RESULT_DIR+run_id
    param = open(res_dir+"/param.txt", "w")
    for key, value in req.items():
        param.write("!"+key+"$")
        param.write(str(value))
        param.write("\n")
    param.close()

def process_request(form):
    if form.has_key("run_id"):
        run_id = form['run_id'].value
    else:
        run_id = cc.new_run()

    (errors, req) = extract_request(form)
    if errors:
        error_page=req["error_messages"]
        return (run_id, "", "", error_page)

    #run_id = cc.new_run()    
    
    stock_parameter(run_id, req)

    #resume_request(run_id, req)
    nb_seq, name_seq = create_fasta(run_id, req['seq'])

    launch_carnac(run_id, req)

    return (run_id, nb_seq, name_seq, "")


def read_file(data_form):
    url_file="/bio2/www/html/"+data_form["rep"].value+"/result/"+data_form["run_id"].value+"/"+data_form["name_file"].value
    sequences=""
    error=""
    try:
        file_fasta=open(url_file, "r")
        for line in file_fasta:
            sequences=sequences+line
        file_fasta.close()
    except IOError as e:
        error="problème dans l'ouverture du fichier "+e.strerror+"\n"
    
    return (sequences, error)
    
def main():
    fs = cgi.FieldStorage()

    run_id, nb_seq, name_seq, error = process_request(fs)

    res_dir = cc.RESULT_DIR+run_id

    res_dir_link = cc.HTML_URL+"result/"+run_id

    sys.stdout.write("Content-Type: application/json")

    sys.stdout.write("\n")
    sys.stdout.write("\n")

    result={}
    result['success'] = True
    result['run_id'] = run_id

    result_return = ""
    result_html = open(res_dir+"/results.php", "w")

    if error!="":
        result_return = c_res.header(result_return)
        result_return = error
        result_return = c_res.footer(result_return)
        result_html.write(str(error))
    else :  
        result_return = c_res.header(result_return)
        result_return = c_res.display_result(run_id, res_dir, result_return, nb_seq, name_seq, res_dir_link)
        result_return = c_res.footer(result_return)
        result_html.write(result_return)

    result_html.close()
    #result['result'] = result_return

    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")

main()