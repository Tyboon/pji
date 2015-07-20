#!/usr/bin/python
# -*- coding: utf-8 -*-

import common
import results as pr
import time
import random
import os
import smtplib	# ?
import sys
import traceback	# ?
import resource		# Resource usage information.
import cgitb
import cgi
import json

cgitb.enable()


def get_result_id():
    return time.strftime('%Y_%m_%d_%H_%M_%S') + "_%i" % random.randint(1,32768)


def valid_request(form):
	back_code='<form><input type="button" value="Back" onclick="history.go(-1)"></form>'
	error_code='<p>Following errors have been found :<br/><ul>\n'
	error_found=False

	if not(form.has_key('decompo')):
        	error_found = True
        	error_code = error_code + '<li> Enter a decomposition </li>\n'
	else :
		if   (form.has_key('decompo') and not(len(form['decompo'].value.strip()) is 0)):      
			decompo = form['decompo'].value
	if error_found:
		error=error_code + '</ul></p>' + back_code
		return None
        
	return decompo



def launch_prog(resid,decompo):
	#fait empreinte et calcule activite
	pass



def process_request(form):
    resid = form["run_id"].value

    req = valid_request(form)
    if req is None:
        return
     
    seqtemp = comon.get_temp_jobdir(resid)+'/'+resid+'.seq'
    fseqtemp = open(seqtemp,'w')
    fseqtemp.write(req)
    fseqtemp.close()

    launch_prog(resid, req)
    
    return resid


def main():
    fs = cgi.FieldStorage()
    
    run_id = process_request(fs)

    res_dir=common.RESULT_DIR+run_id

    res_dir_link=common.HTML_PATH+"result/"+run_id

    sys.stdout.write("Content-Type: application/json")
    
    sys.stdout.write("\n")
    sys.stdout.write("\n")

    result={}
    result['success'] = True
    result['run_id'] = run_id

    result_return = ""
    result_html = open(res_dir+"/results.php", "w")

    result_return = pr.header(result_return)

    result_return=pr.print_result(run_id, res_dir, result_return)

    result_return=pr.footer(result_return)

    result_html.write(result_return)

    result_html.close()
    result['html'] = result_return

    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")

main()
        
 
