#!/usr/bin/python                                                                                                                                                                                            
# coding: utf-8                                                                                                                                                                                              

import sys
import os
import cgi
import cgitb
import sys
import protea_webgate_common
import json

cgitb.enable()


def readFile(file):
    """ read a file and return its content """
    try:
        fi = open(file, "r")
        try:
            content = fi.read()
        finally:
            fi.close()
    except IOError:
        return None

    return content

def main():

    fs = cgi.FieldStorage()

    result={}

    run_id=fs.getvalue('result_id')

    res_dir = protea_webgate_common.PROTEA_RESULT_DIR+run_id
    path_result=res_dir+"/results.html"

    sys.stdout.write("Content-Type: application/json")

    sys.stdout.write("\n")
    sys.stdout.write("\n")

    result_return = readFile(path_result)
    


    result['success'] = True
    result['run_id'] = run_id
    result['html'] = result_return

    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")

main()
