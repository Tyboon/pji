#!/usr/bin/python                                                                                                                                                                
# -*- coding: utf-8 -*-

import tempfile
import traceback
import os
import smtplib
import time
import random

SERVER_NAME = 'http://'+os.environ['SERVER_NAME'];
PROTEA_PUBLIC_URL = SERVER_NAME + '/cgi-bin/protea/protea_webgate.py'
PROTEA_ROOT = '/bio2/www/cgi-bin/protea/'
PROTEA_HTML = '/bio2/www/html/protea/'
PROTEA_CSS = '/protea/protea.css'

PROTEA_MENU_CENTRAL='/bio2/www/html/protea/menu_central.txt'
PROTEA_MENU='/bio2/www/html/menu.txt'

PROTEA_SMTP_SERVER='localhost'

PROTEA_SEQUENCE_LIMIT=10
PROTEA_SIZE_LIMIT=50000

RELOAD_TIME=5

PROTEA_UMASK=002

PROTEA_TEMP_DIR = PROTEA_ROOT + 'tmp/'


PROTEA_EXE="protea"


##variable des scripts globaux de bel/bioinfo
PROTEA_SOFT_NAME='PROTEA'
PROTEA_RESPONSABLE='protea'
PROTEA_RESPONSABLE_MAIL='protea@lifl.fr'
##

PROTEA_MAINTENER_MAIL='Arnaud FONTAINE<arnaud.fontaine@inria.fr>'


PROTEA_MAIL='%s<%s>'%(PROTEA_SOFT_NAME,PROTEA_RESPONSABLE_MAIL)

PROTEA_TRACE_LOG='./trace.log'


PROTEA_RESULT_EXT='.tgz'
PROTEA_RESULT_PENDING_EXT='.pending'
PROTEA_TEMPLATE_ROOT = PROTEA_ROOT + 'template/'
PROTEA_RESULT_DIR = PROTEA_HTML+ 'result/'
PROTEA_TEMP_TEMPLATE = 'PROTEA_WEBGATE_TEMP_'



PROTEA_CLEANING_TIMESTAMP = './cleaning_timestamp'
## in hours
PROTEA_CLEANING_INTERVAL = 1
## in hours
PROTEA_REMOVING_INTERVAL =24*7 


PROTEA_DIALIGN2_DIR = '/usr/share/dialign';

def new_run():    
    runid = new_run_id()
    resdir = result_dir(runid)
    tmpdir = tmp_dir(runid)
    os.mkdir(resdir)
    os.mkdir(tmpdir)
    return runid

def new_run_id():
    """ generate a job id """
    return time.strftime('%b_%d_%Y_%H_%M_%S') + "_%i" % random.randint(1,32768)

def tmp_dir(run_id):    
    tmpdir = os.path.join(PROTEA_TEMP_DIR, run_id)
    return tmpdir

def result_dir(run_id):    
    resdir = os.path.join(PROTEA_RESULT_DIR, run_id)
    return resdir




def send_a_mail(to,subject,body):
    try:
        srv = smtplib.SMTP(PROTEA_SMTP_SERVER)
        msg = '''\
Return-Path: %s
From: %s
To: %s
Subject: %s

%s
''' %(PROTEA_MAIL, PROTEA_MAIL, to, subject, body)
        srv.sendmail(PROTEA_MAIL, [to], msg)
        srv.quit()
    except:
        errfilename = PROTEA_TRACE_LOG
        errfile = open(errfilename, 'a')
        traceback.print_exc(file=errfile)
        errfile.close()
    



def alert_launch(resid):
    send_a_mail(PROTEA_MAINTENER_MAIL, 'Protea job submission', '''\
Dear Protea maintener,

an Protea Web request has been submitted.

Details can be found at
  %s
'''%(PROTEA_PUBLIC_URL + '?command=result&amp;result_id=' + resid))


def alert_maintener(resid):
    send_a_mail(PROTEA_MAINTENER_MAIL, 'Protea job failed', '''\
Dear Protea maintener,
an Protea Web request has failed.

Details can be found at
  %s
''' %(PROTEA_PUBLIC_URL + '?command=result&amp;result_id=' + resid))



def get_template(name):
  file = open(PROTEA_TEMPLATE_ROOT + name + '.html')
  text = file.read()
  file.close()
  return text



def get_header(title):
    mfile = open(PROTEA_MENU)
    mcontent = mfile.read()
    mfile.close()
    mcfile = open(PROTEA_MENU_CENTRAL)
    mccontent = mcfile.read()
    mcfile.close()
    
    return get_template('head') % {'title':title,'css':PROTEA_CSS,'menuc':mccontent,'menu':mcontent,'soft':PROTEA_SOFT_NAME}


def get_footer():
    return get_template('end') % {'soft':PROTEA_SOFT_NAME,'responsable':PROTEA_RESPONSABLE,'mail':PROTEA_RESPONSABLE_MAIL}


def index_page():
  print get_header('Protea webserver') + get_template('request') + get_footer()


def traceback_page():
  errfilename = get_temp_filename()
  errfile = open(errfilename, 'w')
  traceback.print_exc(file=errfile)
  errfile.close()
  errfile = open(errfilename, 'r')
  text = errfile.read()
  error_page('<pre>' + text + '</pre>\n')
  errfile.close()
  os.remove(errfilename) 


def error_page(error):
  print get_header('Protea error page') + get_template('error') % {'error':error} + get_footer()


def get_temp_filename():
  return tempfile.mktemp(prefix=PROTEA_TEMP_TEMPLATE, dir=PROTEA_TEMP_DIR)


def get_temp_jobdir(jobid):
  return PROTEA_TEMP_DIR + jobid


def get_result_wait(result_id):
  return PROTEA_RESULT_DIR + result_id + PROTEA_RESULT_PENDING_EXT


def get_result_archive(result_id):
    return PROTEA_RESULT_DIR +result_id+"/"+result_id+PROTEA_RESULT_EXT


def print_wait_page(result_id):
  html = get_header('Protea job running...')

  url = PROTEA_PUBLIC_URL + "?command=result&amp;result_id=%s" % result_id
    
  html = html + get_template('wait') % {'result_id':result_id,'reload_time':RELOAD_TIME,'url':url}

#  resume = get_result_wait(result_id)
#  fresume = open(resume,'r')
#  resume = fresume.read()
#  fresume.close()

#  html = html + resume + get_footer()
  html = html + get_footer()
    
  print html



def content_html():
    print 'Content-Type: text/html'
    print

def content_text():
    print 'Content-Type: text/plain'
    print


def content_download(name,length):
    print 'Content-Disposition: form-data;name="filename";filename="' + name + '"'
    print 'Content-Type: application/octet-stream'
    print 'Content-Length: %i'%length
    print



def remove_old_results():
    now = time.time()

    try:
        stamp = open(PROTEA_CLEANING_TIMESTAMP, 'w')
        stamp.write('%f'%now)
        stamp.close()

        for fname in os.listdir(PROTEA_RESULT_DIR):
            stats = os.stat(PROTEA_RESULT_DIR + fname)

            difference = (now - stats[8]) / 60.0 / 60.0
            
            if difference >= PROTEA_REMOVING_INTERVAL:
                os.system('rm -rf ' + PROTEA_RESULT_DIR + fname)
    except:
        err = open(PROTEA_TRACE_LOG, 'a')
        traceback.print_exc(file=err)
        err.close()
        

def clean_results():
    try:
        stamp = open(PROTEA_CLEANING_TIMESTAMP, 'r')
        last_clean = float(stamp.read())
        stamp.close()
        now = time.time()

        difference = (now - last_clean) / 60.0 / 60.0

    except:
        difference = PROTEA_CLEANING_INTERVAL + 1
    
    if difference >= PROTEA_CLEANING_INTERVAL:
        remove_old_results()

