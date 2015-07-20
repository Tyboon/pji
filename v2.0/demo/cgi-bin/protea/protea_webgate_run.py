#!/usr/bin/python
# -*- coding: utf-8 -*-

import protea_webgate_common
import protea_webgate_results as pr
import time
import random
import os
import tarfile
import smtplib
import sys
import traceback
import resource		# Resource usage information.
import cgitb
import cgi
import json

cgitb.enable()

#AUTHORIZE_SEQ_BASES='actguACTGU'


def get_result_id():
    return time.strftime('%Y_%m_%d_%H_%M_%S') + "_%i" % random.randint(1,32768)


def count_sequences(seqdata):
    return seqdata.count('>')



def verif_mail(mail):
    res = mail.strip()
    if res.find(' ') > 0:
        return False
    a = res.find('@')
    if a <= 0:
        return False
    if res.find('@', a+1) > 0:
        return False
    return True



def valid_request(form):
    back_code='<form><input type="button" value="Back" onclick="history.go(-1)"></form>'
    error_code='<p>Following errors have been found :<br/><ul>\n'
    error_found=False

    if (form.has_key('seqfile') and form.has_key('seqtxt') and not((len(form['seqtxt'].value.strip()) is 0) or (len(form['seqfile'].value) is 0))):
        error_found = True
        error_code = error_code + '<li>Paste sequences <strong>OR</strong> upload a file</li>\n'
    else:
        if form.has_key('seqfile') and not(len(form['seqfile'].value) is 0):
            seq = form['seqfile'].value
        elif form.has_key('seqtext') and not(len(form['seqtext'].value.strip()) is 0):
            seq = form['seqtext'].value
        else:
            seq = None
            error_found = True
            error_code = error_code + '<li>Missing sequences</li>\n'
        if seq is not None:
            nbseq = count_sequences(seq)
	    if nbseq < 2:
		error_found = True
		error_code = error_code + '<li>Not enough sequences: protea requires <strong>at least 2 sequences</strong></li>'
            elif nbseq > protea_webgate_common.PROTEA_SEQUENCE_LIMIT:
                error_found = True
                error_code = error_code + '<li>Too many sequences: web version is limited to %i sequences</li>\n' % protea_webgate_common.PROTEA_SEQUENCE_LIMIT
            if len(seq) > protea_webgate_common.PROTEA_SIZE_LIMIT:
                error_found = True
                error_code = error_code + '<li>Sequences are too long: web version is limited to %i octets</li>\n' % protea_webgate_common.PROTEA_SIZE_LIMIT
            
    if not form.has_key('email'):
        email = None
#        error_found = True
#        error_code = error_code + '<li>Missing <b>email address</b></li>\n'
    else:
        email = form['email'].value.strip()
        if email is not '':
            if not verif_mail(email):
                error_found = True
                error_code = error_code + '<li>Invalid <strong>email address</strong></li>\n'
        else:
            email = None

    if form.has_key('alnmeth'):
        alnmeth = form['alnmeth'].value
    else:
        alnmeth = None
                
    if error_found:
        error=error_code + '</ul></p>' + back_code
        return None
        
    return {'seq':seq,'coding':True,'reverse':form.has_key('reverse'),'aln':form.has_key('aln'),'alnmeth':alnmeth,'email':email}


def resume_request(resid,coding,reverse,aln,alnmeth,email):
    subtime = time.asctime(time.localtime())
    resume=""
    if email is not None:
        resmail = '<li>Email sent to <code>%s</code></li>' % email
    else:
        resmail = ''

    rescod = ''
    if reverse:
        rescod = rescod + '<li>Using both strands</li>\n'
    else:
        rescod = rescod + '<li>Using only given strand</li>\n'

    if aln:
        rescod = rescod + '<li>A posteriori <strong>'
        if alnmeth == 'T':
            rescod = rescod + 'T-Coffee'
        elif alnmeth == 'D':
            rescod = rescod + 'Dialign2'
        else:
            rescod = rescod + 'ClustalW'
        rescod = rescod + '</strong> multiple alignment</li>\n'
    resume=resume+"<h2>Job Information</h2><ul>"
    resume=resume+"<li>Job ID : "+resid+"</li>"
    resume=resume+"<li>Submitted on "+subtime+"</li>"
    resume=resume+resmail
    resume=resume+rescod
    resume=resume+"</ul>"

    return resume

def launch_protea(reltmpseq,resid,coding,reverse,aln,alnmeth,email):
    tmpseq = os.path.abspath(reltmpseq)
    odir = protea_webgate_common.get_temp_jobdir(resid)

    protea_webgate_common.alert_launch(resid)

    cmd = protea_webgate_common.PROTEA_EXE + ' -kliw -m 2 -o . '
    if coding == 'T':
        if reverse == 'T':
            cmd = cmd + ' -p 6'
        else:
            cmd = cmd + ' -p 3'
        if aln:
            cmd = cmd + ' -a'
            if alnmeth == 'T':
                cmd = cmd + ' -t'
            elif alnmeth == 'D':
                cmd = cmd + ' -d'

    cmd = cmd + ' ' + tmpseq

    resarchive = tarfile.TarFile.gzopen(protea_webgate_common.get_result_archive(resid),mode='w')
    #resarchive.add(odir +  '/resume', resid + '/resume')

    os.putenv('DIALIGN2_DIR', protea_webgate_common.PROTEA_DIALIGN2_DIR)
    os.putenv('HOME_4_TCOFFEE', protea_webgate_common.PROTEA_ROOT)

    #os.mkdir(odir)
    prevdir = os.path.abspath(os.getcwd())
    os.chdir(odir)
    os.system('echo \"' + cmd + '\" > command')
    exitcode =  os.system(cmd + ' > stdout 2> stderr')
    os.chdir(prevdir)
    
    resarchive.add(odir + '/command', resid + '/command')
    resarchive.add(odir + '/stdout', resid + '/stdout')
    resarchive.add(odir + '/stderr', resid + '/stderr')
    
    if exitcode == 0:
        resarchive.add(odir + '/sequences.fasta', resid + '/sequences.fasta')
        resarchive.add(odir + '/needle.out', resid + '/needle.out')
        resarchive.add(odir + '/needle', resid + '/needle')
        resarchive.add(odir + '/length.out', resid + '/length.out')
#        resarchive.add(odir + '/dinucleotides.out', resid + '/dinucleotides.out')
        if coding:
            resarchive.add(odir + '/needlep.out', resid + '/needlep.out')
#            resarchive.add(odir + '/needlep', resid + '/needlep')
#            resarchive.add(odir + '/needlep_graph.tex', resid + '/needlep_graph.tex')
            try:
                s = os.stat(odir + '/proteins.fasta')
                resarchive.add(odir + '/proteins.fasta', resid + '/proteins.fasta')
                if aln:
                    resarchive.add(odir + '/proteins_aligned.aln', resid + '/proteins_aligned.aln')
                    resarchive.add(odir + '/proteins_aligned.html', resid + '/proteins_aligned.html')
                    resarchive.add(odir + '/sequences_aligned_proteins.aln', resid + '/sequences_aligned_proteins.aln')
                    resarchive.add(odir + '/sequences_aligned_proteins.html', resid + '/sequences_aligned_proteins.html')
            except OSError:
                s = None
    else:
        resarchive.add(tmpseq, resid + '/fail')
        protea_webgate_common.alert_maintener(resid)

    
    try:
        resarchive.close()
        #os.remove(protea_webgate_common.get_result_wait(resid))
    except:
        pass

        
    if email != "":
        protea_webgate_common.send_a_mail(email, 'Protea job completed', '''
Dear Protea user,
your Protea Web job is completed.

Results are available at
  %s

A compressed tar archive of your results can be downloaded at
  %s

Thank you for using Protea !
''' %(protea_webgate_common.PROTEA_PUBLIC_URL + '?command=result&amp;result_id=' + resid, protea_webgate_common.PROTEA_PUBLIC_URL + '?command=get&amp;result_id=' + resid))

#    try:
#        os.remove(tmpseq)
        #os.system('rm -rf ' + odir)
#    except:
#        pass


def read_file(data_form):
    url_file=protea_webgate_common.PROTEA_HTML+"/result/"+data_form["run_id"].value+"/"+data_form["name_file"].value
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

def stock_parameter(run_id, req):
    res_dir = protea_webgate_common.PROTEA_RESULT_DIR+run_id
    param = open(res_dir+"/param.txt", "w")
    for key, value in req.items():
        param.write("!"+key+"$")
        param.write(str(value))
        param.write("\n")
    param.close()


def process_request(form):
    resid = form["run_id"].value

    req = valid_request(form)
    if req is None:
        return
    
    #resid = get_result_id()
     
    stock_parameter(resid, req)
   
    seqtemp = protea_webgate_common.get_temp_jobdir(resid)+'/'+resid+'.seq'
    fseqtemp = open(seqtemp,'w')
    fseqtemp.write(req['seq'])
    fseqtemp.close()

    coding = 'F'
    if req['coding']:
        coding = 'T'
    
    reverse = 'F'
    if req['reverse']:
        reverse = 'T'

    aln = 'F'
    if req['aln']:
        aln = 'T'

    email = ''
    if req['email']:
        email = req['email'];
    
    resume = resume_request(resid,req['coding'],req['reverse'],req['aln'],req['alnmeth'],req['email'])

    launch_protea(seqtemp,resid,coding,reverse,aln,req['alnmeth'],email)
    
    filename_resume = protea_webgate_common.get_temp_jobdir(resid)+"/resume"
    resume_file=open(filename_resume, 'w')
    resume_file.write(resume)
    resume_file.close()

    #sys.stderr.write("protea_webgate_common.PROTEA_RESULT_DIR+resid : "+protea_webgate_common.PROTEA_RESULT_DIR+resid)

    os.system("cp -rp %s %s" % (protea_webgate_common.PROTEA_TEMP_DIR+resid, protea_webgate_common.PROTEA_RESULT_DIR))
    
    return resid


def main():
    fs = cgi.FieldStorage()
    
    run_id = process_request(fs)

    res_dir=protea_webgate_common.PROTEA_RESULT_DIR+run_id

    res_dir_link=protea_webgate_common.PROTEA_HTML+"result/"+run_id

    sys.stdout.write("Content-Type: application/json")
    
    sys.stdout.write("\n")
    sys.stdout.write("\n")

    result={}
    result['success'] = True
    result['run_id'] = run_id

    result_return = ""
    result_html = open(res_dir+"/results.php", "w")

    result_return = pr.header(result_return)

    result_archive = protea_webgate_common.get_result_archive(run_id)

    result_file = tarfile.TarFile.gzopen(result_archive)
    
    #result_return = result_return+"<button class='button_form_fill'>back to form</button></br>"

    result_return = result_return+"<h2>Protea results [<a href='/protea/result/"+run_id+"/"+run_id+".tgz'>archive</a>]</h2>"

    result_return=pr.print_result(run_id, result_archive, res_dir, result_return)

    #result_return = result_return+"</br></br><button class='button_form_fill'>back to form</button></br></br>"

    result_return=pr.footer(result_return)

    result_html.write(result_return)

    result_html.close()
    result['html'] = result_return

    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")

main()
        
        
