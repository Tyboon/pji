import traceback

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions

import carnac_common as cc


MAKO_LOOKUP = TemplateLookup(directories=[cc.TEMPLATE_DIR])

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

def get_template(template_name, **kwargs):    
    try:
        mytemplate = MAKO_LOOKUP.get_template(template_name)
        return mytemplate.render(**kwargs)
    except:
        err = open(cc.TRACE_LOG, 'a')
        traceback.print_exc(file=err)
        err.close()
        return None


def serve_template(template_name, **kwargs):

    fmenu = open(cc.MENU, "r")
    fmenuc = open(cc.MENU_CENTRAL, "r")
    menu = fmenu.read()
    menuc = fmenuc.read()
    fmenu.close()
    fmenuc.close()
    
    try:
        mytemplate = MAKO_LOOKUP.get_template(template_name)
        print mytemplate.render(menu=menu, menu_central=menuc, **kwargs)
    except:
        print exceptions.html_error_template().render()

def index_page():
    template_name = "form.mako"
    arg = {"head_title":"carnac", "example":""}
    serve_template(template_name=template_name, **arg) 

def example_page():
    template_name = "form.mako"
    fexample = open(cc.EXAMPLE_FILE, "r")
    example = fexample.read()
    fexample.close()

    arg = {"head_title":"carnac", "example":example}
    serve_template(template_name=template_name, **arg) 

def wait_page(run_id, email):
    template_name = "wait.mako"
    wait_url = cc.CGI_URL + "?command=result&amp;run_id=" + str(run_id)
    reload_time = cc.RELOAD_TIME
    arg = {"head_title":"carnac: job running...", "email":email,
           "run_id":run_id, "reload_time":reload_time, "url":wait_url}
    
    serve_template(template_name=template_name, **arg)

def result_page(run_id, img, sequences, tgz, stdout, alignment_url, alignment,
                rnafolds):
    arg = {"head_title":"carnac: results " + run_id, "run_id":run_id,
           "img":img, "sequences":sequences, "tgz":tgz, "stdout":stdout,
           "alignment_url":alignment_url, "alignment":alignment, 
           "rnafolds":rnafolds}
    
    serve_template(template_name="results.mako", **arg)
    
def error_page(errors):
    template_name = "error.mako"
    arg = {"head_title":"CARNAC: Errors found", "errors":errors}
    serve_template(template_name=template_name, **arg) 

def traceback_page():    
    tb = traceback.format_exc()
    arg = {"head_title":"CARNAC: debug", "tb":tb}
    serve_template(template_name="traceback.mako", **arg)

