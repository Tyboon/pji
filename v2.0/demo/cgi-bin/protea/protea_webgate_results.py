#!/usr/bin/python
# -*- coding: utf-8 -*-

import protea_webgate_common as pc
import tarfile
import os
import re
import sys
import cgitb
import cgi

cgitb.enable()


def job_failed(arch, resid):
    try:
        fi = arch.extractfile(resid + '/fail')
        return True
    except:
        return False

def extract_stdout(arch, resid):
    try:
        fi = arch.extractfile(resid + '/stdout')
        content = fi.read()
        return content
    except:
        return None

def extract_stderr(arch, resid):
    try:
        fi = arch.extractfile(resid + '/stderr')
        content = fi.read()
        return content
    except:
        return None

def extract_resume(resid):
    try:
        fi = open(pc.PROTEA_RESULT_DIR+resid+'/resume',"r")
        content = fi.read()
        return content
    except:
        return None

def extract_needlep(arch, resid):
    try:
        fi = arch.extractfile(resid + '/needlep.out')
        content = fi.read()
        return content
    except:
        return None

def extract_proteins(arch, resid):
    try:
        fi = arch.extractfile(resid + '/proteins.fasta')
        content = fi.read()
        return content
    except:
        return None



def extract_aa_alignment(arch, resid):
    try:
        fi = arch.extractfile(resid + '/proteins_aligned.html')
        content = fi.read()
        return content
    except:
        return None

def exist_alignments(arch, resid):
    try:
        fi = arch.extractfile(resid + '/proteins_aligned.html')
        fi = arch.extractfile(resid + '/sequences_aligned_proteins.html')
        return True
    except:
        return False


def extract_rev_alignment(arch, resid):
    try:
        fi = arch.extractfile(resid + '/sequences_aligned_proteins.html')
        content = fi.read()
        return content
    except:
        return None


def extract_length(arch, resid):
    try:
        fi = arch.extractfile(resid + '/length.out')
        content = fi.read()
        match = re.search('[0-9]+', content)
        if match is not None:
            return match.group(0)
    except:
        return None
    return None

def extract_identity_percentage(arch, resid):
    try:
        fi = arch.extractfile(resid + '/needle.out')
        content = fi.read()
        match = re.search('[0-9]+.[0-9]+', content)
        if match is not None:
            return '%.1f %%' % float(match.group(0))
    except:
        return None
    return '(not available)'


def extract_coding_prediction(arch, resid):
    try:
        content = extract_needlep(arch, resid)
        match = re.search('prediction = CODING', content)
        if match is not None:
           return True
        return False
    except:
        return None
    return None

def extract_coding_pvalue(arch, resid):
    try:
        content = extract_needlep(arch, resid)
        match = re.search('pvalue = [-0-9eE.]+', content)
        return match.group(0)[9:]
    except:
        return None

def extract_coding_zscore(arch, resid):
    try:
        content = extract_needlep(arch, resid)
        match = re.search('zscore = [^\n]*', content)
        return match.group(0)[9:]
    except:
        return None



def format_error_message(msg):
    return '<li><span style="font-weight:bold; color:#FF0000;font-size:150%%;">' + msg + '</span></li>'

def readable_error(err):
    res = ''

    match = re.search('invalid token', err)
    if match is not None:
        res = res + format_error_message('Input is not in multi FASTA format')

    match = re.search('unknown nucleotide', err)
    if match is not None:
        res = res + format_error_message('Input sequence is not a valid nucleic sequence')

    match = re.search('complement: Assertion', err)
    if match is not None:
        res = res + format_error_message('Input sequence is too short')

    match = re.search('Empty sequence', err)
    if match is not None:
        res = res + format_error_message('Input sequence is empty')

    if res is '':
        return None

    return res


def print_result(result_id, result_archive,res_dir_link, result_return):
    try:
        resfile = tarfile.TarFile.gzopen(result_archive)
        resres = extract_resume(result_id)

        res_dir="/protea/result/"+result_id
        
        if job_failed(resfile, result_id):
            reserr = extract_stderr(resfile, result_id)
            if reserr is None:
                reserr = ''
            readreserr = readable_error(reserr)
            if readreserr is None:
                resout = extract_stdout(resfile, result_id)
                if resout is None:
                    resout = ''
                result_return=result_return+"<h2>Job failed:</h2>"
                result_return=result_return+"<ul><li>Error output</li><pre>"+reserr+"/pre><li>Standard output</li><pre>"+resout+"</pre></ul>"
                result_return=result_return+resres
                
            else:
                result_return=result_return+"<h2>Job failed:</h2>"
                result_return=result_return+"<ul>"+readreserr+"</ul>"
                result_return=result_return+resres
                
        else:
            resneedle = extract_identity_percentage(resfile, result_id)
            if resneedle is None:
                resneedle = '(not available)'
            reslength = extract_length(resfile, result_id)
            if reslength is None:
                reslength = '(not available)'
        
            respred = extract_coding_prediction(resfile, result_id)
            if respred is not None:
                respz = extract_coding_pvalue(resfile, result_id)
                if respz is None:
                    respz = extract_coding_zscore(resfile, result_id)
                    if respz is None:
                        respz = '(no reliable assignment)'
                    else:
                        respz = '(Z-score = ' + respz + ')'
                else:
                    respz = '(P-value = ' + respz + ')'
                
                if respred:
                    respredt = '<strong>CODING</strong> ' + respz
                else:
                    respredt = '<strong>OTHER</strong> ' + respz
                result_return=result_return+"<ul><li>Prediction: "+respredt+"</li>"
                
                if respred:
                    aa_seqs = extract_proteins(resfile, result_id);
                    if exist_alignments(resfile, result_id):
                        aa_aln = extract_aa_alignment(resfile, result_id);
                        rev_aln = extract_rev_alignment(resfile, result_id);
                        result_return=result_return+"<li>Predicted amino acid sequences [<a href='"+res_dir+"/proteins.fasta'>fasta</a> - <a href='"+res_dir+"/proteins_aligned.aln'>multiple alignment</a>]</li>"
                        result_return=result_return+"<pre>"+aa_aln+"</pre>"
                        result_return=result_return+"<li>Nucleic sequences [<a href='"+res_dir+"/sequences.fasta'>fasta</a> - <a href='"+res_dir+"/sequences_aligned_proteins.aln'>reverse translation of multiple alignment</a>]</li>"
                        result_return=result_return+"<pre>"+rev_aln+"</pre>"
                        
                    else:
                        result_return=result_return+"<li>Download predicted amino acid sequences <a href='"+res_dir+"/proteins.fasta'>fasta</a></li>"
                        result_return=result_return+"<pre>"+aa_seqs+"</pre>"
                        
            else:
                result_return = result_return+''
                                
            result_return=result_return+"</ul><h2>General information</h2><ul>"
            result_return=result_return+"<li>Average identity percentage is "+resneedle+"</li>"
            result_return=result_return+"<li>Average length is "+reslength+"</li>"
            result_return=result_return+"<li>Submitted sequences [<a href='"+res_dir+"/sequences.fasta'>fasta</a>]</li></ul>"
            result_return=result_return+resres
            
        resfile.close()
    except:
        result_return=result_return+"Error with the archive"
        
    return result_return

def retrieve_results(form):
    if not form.has_key('result_id'):
        protea_webgate_common.error_page('Missing result identifier !')
        return 

    result_id = form['result_id'].value
    result_wait = protea_webgate_common.get_result_wait(result_id)
    try:
        s = os.stat(result_wait)
        protea_webgate_common.print_wait_page(result_id)
    except OSError:
        result_archive = protea_webgate_common.get_result_archive(result_id)
        try:
            s = os.stat(result_archive)
            print_result(result_id,result_archive)
        except OSError:
            protea_webgate_common.error_page('No result with job ID <strong>' + result_id + '</strong> !!')



def extract_file(form):
    if not form.has_key('result_id'):
        protea_webgate_common.content_html()
        protea_webgate_common.error_page('Missing result identifier !')
        return 

    result_id = form['result_id'].value
    result_wait = protea_webgate_common.get_result_wait(result_id)
    try:
        s = os.stat(result_wait)
        protea_webgate_common.content_html()
        protea_webgate_common.print_wait_page(result_id)
    except OSError:
        result_archive = protea_webgate_common.get_result_archive(result_id)

        if not form.has_key('file'):
            protea_webgate_common.content_html()
            protea_webgate_common.error_page('Missing file name !')
            return

        exfilename = form['file'].value
        exfilecontent = None
        
        try:
            s = os.stat(result_archive)
            resfile = tarfile.TarFile.gzopen(result_archive)

            try:
                exfile = resfile.extractfile(result_id + '/' + exfilename)
                exfilecontent=exfile.read()
            except:
                protea_webgate_common.content_html()
                protea_webgate_common.error_page('No such file or directory <strong>' + exfilename + '</strong> for job ID <strong>' + result_id + '</strong>!!')

            resfile.close()
        except OSError:
            protea_webgate_common.content_html()
            protea_webgate_common.error_page('No result with job ID <strong>' + result_id + '</strong> !!')

        if exfilecontent is not None:
            length = len(exfilecontent)
            # protea_webgate_common.content_download(result_id + '_' + exfilename, length)
            protea_webgate_common.content_text()
            print exfilecontent
            
    sys.stdout.flush()




def get_result_archive(form):
    if not form.has_key('result_id'):
        protea_webgate_common.content_html()
        protea_webgate_common.error_page('Missing result identifier !')
        return 

    result_id = form['result_id'].value
    result_wait = protea_webgate_common.get_result_wait(result_id)
    try:
        s = os.stat(result_wait)
        protea_webgate_common.content_html()
        protea_webgate_common.print_wait_page(result_id)
    except OSError:
        result_archive = protea_webgate_common.get_result_archive(result_id)
        
        try:
            s = os.stat(result_archive)
            resfile = open(result_archive)
            resfilecontent = resfile.read()
            resfile.close()
            length = len(resfilecontent)
            protea_webgate_common.content_download(result_id + protea_webgate_common.PROTEA_RESULT_EXT, length)
            print resfilecontent
            sys.stdout.flush()
        except:
            protea_webgate_common.content_html()
            protea_webgate_common.error_page('No result archive with job ID <strong>' + result_id + '</strong> !!')
            
def header(result_return):
    result_return =result_return+"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link href="/protea/protea.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
    <script type="text/javascript" src="/scripts/bioinfo_propre.js"></script>
    <script type="text/javascript" src="/protea/js/script.js"></script>
    <title>Bonsai  :: Bioinformatics Software Server</title>
    </head>
    <body> 
    <div class="frametitle">
    <h1 id="title">protea :: protein coding gene prediction</h1>                 
    </div>
    <div id="center_sup">
    <div class="theme-border" style="display:none"></div>
    <div id="link_home" style="display:inline-block"><a href="/" class="text_onglet"><img src="/Style/icon/home_w.png" alt="home_general"/></a></div>
    <div class="tabs" id="menu_central" style="display:inline-block"><?php include("../../menu_central.txt")?></div>
    </div>
    <div id="main">
    <div id="center">"""
    return result_return



def footer(result_return):
    result_return=result_return+"""    </div></div><!-- bloc droit-->
    <?php require("../../../lib.inc")?>
    <?php footer("Protea","Protea", "protea@lifl.fr","2013"); ?>
    </div>                                                                             
    </body>                                        
    </html>"""
    return result_return
