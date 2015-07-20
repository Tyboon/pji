#!/usr/bin/env python

import cgi
import os
import sys
import socket

import protea_webgate_common
import protea_webgate_run
import protea_webgate_results





try:

  os.umask(protea_webgate_common.PROTEA_UMASK)
  protea_webgate_common.clean_results()
  
  form = cgi.FieldStorage()
  ip = os.getenv("REMOTE_ADDR")
  #nom = socket.gethostbyaddr(ip)[0]
  nom = ip

  if form.has_key('command'):
    if form['command'].value == 'request':
      protea_webgate_common.content_html()
      protea_webgate_run.process_request(form,nom)
    elif form['command'].value == 'result':
      protea_webgate_common.content_html()
      protea_webgate_results.retrieve_results(form)
    elif form['command'].value == 'extract':
      protea_webgate_results.extract_file(form)
    elif form['command'].value == 'get':
      protea_webgate_results.get_result_archive(form)
    else:
      protea_webgate_common.content_html()
      protea_webgate_common.error_page('invalid command')
  else:
    protea_webgate_common.content_html()
    protea_webgate_common.index_page()
except:
  protea_webgate_common.content_html()
  protea_webgate_common.traceback_page()

