#!/usr/bin/env python

import cgi
import os
import sys
import socket

import carnac_common
import carnac_html
import carnac_run
import carnac_results

try:

  os.umask(carnac_common.UMASK)
  carnac_common.clean_results()
  
  form = cgi.FieldStorage()

  if form.has_key('example'):
    carnac_html.content_html()
    carnac_html.example_page()
  elif form.has_key('reset'):
     carnac_html.content_html()
     carnac_html.index_page()
  elif form.has_key('command'):
    if form['command'].value == 'request':
      carnac_html.content_html()
      carnac_run.process_request(form)
    elif form['command'].value == 'result':
      carnac_html.content_html()
      carnac_results.retrieve_results(form)
  else:
    carnac_html.content_html()
    carnac_html.index_page()
    
except:
  carnac_html.content_html()
  carnac_html.traceback_page()
