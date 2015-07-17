#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json
import carnac_common as cc

def main():
    run_id=""
    run_id = cc.new_run()
    result={}
    if run_id!="":
        result['success'] = True
        result['run_id'] = run_id
    else:
        result['sucess'] = False
        
    sys.stdout.write("Content-Type: application/json")
    sys.stdout.write("\n\n")
    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")
    
main()
    
