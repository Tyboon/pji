#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import re
import cgi
import cgitb

import protea_webgate_common as pc
cgitb.enable()

def read_file_param(url_param_file):
    param={}
    try:
        file_param=open(url_param_file, "r")
        lines=file_param.readlines()
        i=0
        while i<len(lines):
            line=lines[i]
            if re.search("^!", line):
                line=lines[i].rstrip()
                tab=line.split("$")
                if tab[0][1:]=="seq":
                    key="sequence"
                    value=tab[1]+"\n"
                else:
                    key=tab[0][1:]
                    value=tab[1]
                param[key]=value
            elif line!="" and line!="\n":
                value+=line;
                param[key]=value
            i+=1
        if param.has_key("error_messages"):
            del param["error_messages"] 
    except IOError as e:
        param["error"]="I/O error({0}): {1}".format(e.errno, e.strerror)+"  "+url_param_file
    file_param.close()
    return param
            
                
        
def main():
    fs = cgi.FieldStorage()
    id_result = fs['id'].value
    name_soft = fs['name_soft'].value
    url_param_file=pc.PROTEA_HTML+"/result/"+id_result+"/param.txt"
    param={}
    param=read_file_param(url_param_file)
    result={}
    result=dict(result.items()+param.items())
    if param.has_key("error"):
        result['success'] = False
        result['size']="error"
    else:
        result['sucess'] = True
        
    sys.stdout.write("Content-Type: application/json")
    sys.stdout.write("\n\n")
    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")
    
main()
