import os
import re
import sys
import pickle

import carnac_common as cc
import carnac_html as chtml


class sequence:
    def __init__(self, name, ct, jpeg, ps, bra, F):
        self.name = name
        self.ct = ct
        self.jpeg = jpeg
        self.ps = ps
        self.bra = bra
        self.F = F
        

def print_results(run_id):
    res_dir = cc.result_dir(run_id)
    res_url = cc.result_url(run_id)
    arch_url = cc.archive_url(run_id)

    sequences = []
    rnafolds = []
    img = None
    for res_file in os.listdir(res_dir):
        res_file_abs = os.path.join(res_dir, res_file)        
        (shortname, extension) = os.path.splitext(res_file)
        if extension == ".ct":
            fct = open(res_file_abs, 'r')
            content = fct.read()
            fct.close()
            content = content.splitlines()
            first_line = content[0].split()
            name = " ".join(word for word in first_line[1:])
            ct = res_url + shortname + ".ct"
            ps = res_url + shortname + ".ps"
            jpeg = res_url + shortname + ".jpeg"
            bra = res_url + shortname + ".bra"
            F = res_url + shortname + ".F"
            seq = sequence(name, ct, jpeg, ps, bra, F)
            sequences.append(seq)
            if img is None:
                img = jpeg
        elif shortname.startswith('rnafold'):
            fseq = open(res_file_abs, 'r')
            result = ""
            for (i, line) in enumerate(fseq):
                if i == 1 or i == 2:
                    for (j, car) in enumerate(line):
                        if j % 100 == 0 and j != 0:
                            result += "\n"
                        result += car
                else:
                    result += line
            fseq.close()
            rnafolds.append(result)

    alignment_path = os.path.join(res_dir, "alignment.html")
    if os.path.isfile(alignment_path):
        falignment = open(alignment_path, "r")
        alignment = falignment.read()
        falignment.close()
        alignment_url = res_url + "alignment.html"
    else:
        alignment = None
        alignment_url = None

    stdout = os.path.join(res_url, "carnac_stdout.txt")
    chtml.result_page(run_id, img, sequences, arch_url, stdout, alignment_url,
                      alignment, rnafolds)
    
def retrieve_results(form):
    if not form.has_key('run_id'):
        chtml.error_page(['Missing run identifier !'])
        return 

    run_id = form['run_id'].value
    pend = cc.pending_file(run_id)
    try:
        s = os.stat(pend)
        fpend = open(pend, "rb")
        req = pickle.load(fpend)
        email = req["email"]
        chtml.wait_page(run_id, email)
    except OSError:
        try:
            if len(os.listdir(cc.result_dir(run_id))) > 0:
                print_results(run_id)
            else:
                chtml.error_page(['No result with job ID <strong>' +
                                  run_id + '</strong> !!'])
        except OSError:
            chtml.error_page(['Job ID <strong>' + run_id + '</strong> ' +
                              'does not exist'])
            
