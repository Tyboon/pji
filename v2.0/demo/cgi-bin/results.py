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

import carnac_common as cc

cgitb.enable()



def header(result_return):
    result_return =result_return+"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link href="/carnac/carnac.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
    <script type="text/javascript" src="/scripts/bioinfo_propre.js"></script>
    <script type="text/javascript" src="/carnac/js/script.js"></script>
    
    <title>Bonsai  :: Bioinformatics Software Server</title>
    </head>
    <body> 
    <div class="frametitle">
    <h1 id="title">carnac :: RNA structure inference</h1>                 
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
    <?php require("../../../../lib.inc")?>
    <?php footer("Carnac","Carnac", "carnac@lifl.fr","2013"); ?>
    </div>                                                                             
    </body>                                        
    </html>"""
    return result_return




def display_result(run_id, res_dir, result_return, nb_seq, name_seq, res_dir_link):
    result_return=intro_html(run_id, res_dir, result_return, nb_seq, name_seq, res_dir_link)
    result_return=display_aligt(res_dir, result_return, res_dir_link)
    result_return=display_rnafold(res_dir, result_return, res_dir_link)
    result_return=end_display(res_dir, run_id, result_return, res_dir_link)
    return result_return


def seq_files(result_return, res_dir, name_seq):
    i=1
    for name in name_seq:
        if i<10:
            seq_file=res_dir+"/seq00"+str(i)
        elif (i>9 and i<100):
            seq_file=res_dir+"/seq0"+str(i)
        else:
            seq_file=res_dir+"/seq"+str(i)
        result_return=result_return+"<li>"+name+"<br/>"
        result_return=result_return+"<a href='"+seq_file+".ct'>CT file</a> , "
        result_return=result_return+"<a href='"+seq_file+".ps'>PS file</a> , "
        result_return=result_return+"<a href='"+seq_file+".jpeg'>JPEG file</a> , "
        result_return=result_return+"<a href='"+seq_file+".bra'>bracket notation</a> , "
        result_return=result_return+"<a href='"+seq_file+".F'>list of stems</a>"
        result_return=result_return+"</li>"
        i+=1
    return result_return
    

def intro_html(run_id, res_dir, result_return, nb_seq, name_seq, res_dir_link):
    #result_return = result_return+"<button class='button_form_fill'>back to form</button>"
    result_return = result_return+"<a href='"+res_dir_link+"/seq001.jpeg'><img src='"+res_dir_link+"/seq001.jpeg' width='200' align='right'></a>"
    result_return = result_return+"<h4>Results for job "+run_id+"</h4>"
    result_return = result_return+"<ul>"
    result_return= seq_files(result_return, res_dir_link, name_seq)

    result_return = result_return+"</ul>"
    result_return = result_return+"<br/>"
        
    return result_return


def display_aligt(res_dir, result_return, res_dir_link):
    result_return=result_return+"<b>Alignment [<a href='"+res_dir_link+"/alignment.html'>clustal</a>]</b> :"
    result_return=result_return+"<pre>"
    
    if os.path.exists(res_dir+"/alignment.html"):
        aligt_file=open(res_dir+"/alignment.html", "r")
        for line in aligt_file:
            result_return=result_return+line
        aligt_file.close()
    else:
        result_return=result_return+"       No alignment"

    result_return=result_return+"</pre>"
    
    return result_return
    
def display_rnafold(res_dir, result_return, res_dir_link):
    result_return= result_return+"<b>RNAfold structures</b> : "
    result_return= result_return+"<pre>"
    result_return= result_return+"</pre>"
    
    return result_return

def end_display(res_dir, run_id, result_return, res_dir_link):
    result_return= result_return+"<b>Download all files</b> : "
    result_return= result_return+"<a href='"+res_dir_link+"/"+run_id+".zip'>"+run_id+".zip</a>"
    result_return= result_return+"<br/><br/><br/>"
    result_return= result_return+"<b>More</b> <a href='"+res_dir_link+"/carnac_stdout.txt'>information</a><b> about the computational process</b>"
    result_return= result_return+"<br/><br/>"
    #result_return = result_return+"<button class='button_form_fill'>back to form</button><br/>"
    return result_return
