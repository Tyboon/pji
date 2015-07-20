#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

#Remplacer exemple_web_server par le nom de votre logiciel
HTML_PATH = "/bio2/www/html/NRP2Act"
CGI_PATH = "/bio2/www/cgi-bin/NRP2Act"

TEMP_DIR = os.path.join(CGI_PATH, 'tmp/')
RESULT_DIR = os.path.join(HTML_PATH, "result/")



#Renvoie le pwd pour le dossier tmp/
def tmp_dir(run_id):    
    tmpdir = os.path.join(TEMP_DIR, run_id)
    return tmpdir


#Renvoie le pwd du dossier result/
def result_dir(run_id):    
    resdir = os.path.join(RESULT_DIR, run_id)
    return resdir


#Retourne le pwd du dossier où sont stockés les résultats de la requête
def result_dir_html(run_id):    
    resdir = os.path.join(RESULT_DIR, run_id)
    return resdir


def content_html():
    print 'Content-Type: text/html'
    print


def content_text():
    print 'Content-Type: text/plain'
    print


