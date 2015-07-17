import tempfile
import tarfile
import zipfile
import traceback
import os
import smtplib
import time
import random

## URLs
SERVER_NAME = 'http://'+os.environ['SERVER_NAME'];
FULL_HTML_URL = SERVER_NAME + "/carnac/"
FULL_CGI_URL = SERVER_NAME + "/cgi-bin/carnac/carnac.py"
HTML_URL = '/carnac/'
CGI_URL = '/cgi-bin/carnac/carnac.py'
RESULTS_BASE_URL = HTML_URL + "result/"
FULL_RESULTS_URL = FULL_CGI_URL + "?command=result&amp;run_id="

## DIFFERENT PATHS
HTML_PATH = "/bio2/www/html/carnac"
CGI_PATH = "/bio2/www/cgi-bin/carnac"
CLEANING_TIMESTAMP = os.path.join(CGI_PATH, "cleaning_timestamp.txt")
TRACE_LOG = os.path.join(CGI_PATH, 'trace.log')

TEMP_DIR = os.path.join(CGI_PATH, 'tmp/')
TEMPLATE_DIR = os.path.join(CGI_PATH, 'template/')
RESULT_DIR = os.path.join(HTML_PATH, "result/")
EXAMPLE_FILE = os.path.join(CGI_PATH, 'example.fasta')

## TEMPLATE FILES
CSS = '/carnac/carnac.css'
MENU_CENTRAL = os.path.join(HTML_PATH, "menu_central.txt")
MENU = os.path.join(HTML_PATH, "menu.txt")


SEQUENCE_LIMIT=10
RELOAD_TIME=5
UMASK=002
ARCHIVE_EXT = ".zip"

## in hours
CLEANING_INTERVAL = 1
## in hours
REMOVING_INTERVAL = 72


## SOFTWARE PATHS
RNATOOLS = '/bio2/www/cgi-bin/RNA/rnatools/'
APP = '/bio2/app/'
COLOURS = '/bio2/www/cgi-bin/RNA/colours/'

# rna tools
BRACKET2CT = RNATOOLS + 'bracket2ct.pl'
CT2FORCED = RNATOOLS + 'ct2forced.pl'
CT2PARENTHESIS = RNATOOLS + 'ct2parenthesis.pl'
EQ2FASTA = RNATOOLS + 'eq2fasta.pl'

# app
NAVIEW = APP + 'naview/Bin/naview'
DEFAULT_NAV = APP + 'naview/default.nav'
PLT22PS = APP + 'naview/Bin/plt22ps'

# colours
DISPLAY_ALIGNMENTS = "python " + RNATOOLS + "display_alignment/display_align.py"

# programs
GARDENIA = 'gardenia'
CARNAC = '/bio2/www/cgi-bin/carnac/carnac'
CLUSTALW = 'clustalw'
RNAFOLD = 'RNAfold'



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
    tmpdir = os.path.join(TEMP_DIR, run_id)
    return tmpdir

def result_dir(run_id):    
    resdir = os.path.join(RESULT_DIR, run_id)
    return resdir

def pending_file(run_id):
    temp_dir = tmp_dir(run_id)
    pend = os.path.join(temp_dir, run_id + ".pend")
    return pend

def fasta_path(run_id):
    temp_dir = tmp_dir(run_id)
    fpath = os.path.join(temp_dir, run_id + ".fasta")
    return fpath

def stdout_path(run_id, softname):
    temp_dir = tmp_dir(run_id)
    stdout = os.path.join(temp_dir, softname + "_stdout.txt")
    return stdout

def stderr_path(run_id, softname):
    temp_dir = tmp_dir(run_id)
    stderr = os.path.join(temp_dir, softname + "_stderr.txt")
    return stderr

def command_path(run_id, softname):
    temp_dir = tmp_dir(run_id)
    cmd = os.path.join(temp_dir, softname + "_command.txt")
    return cmd

def add_to_archive(run_id, files):
    arch_path = archive_path(run_id)
    resarchive = zipfile.ZipFile(arch_path, mode="w", 
                                 compression=zipfile.ZIP_DEFLATED)
    for f in files:
        (dirname, filename) = os.path.split(f)
        resarchive.write(f, filename)
    resarchive.close()

def archive_name(run_id):
    return run_id + ARCHIVE_EXT

def archive_path(run_id):
    resdir = result_dir(run_id)
    return os.path.join(resdir, archive_name(run_id))

def archive_url(run_id):
    url = result_url(run_id)
    return url + archive_name(run_id)

def result_url(run_id):
    return RESULTS_BASE_URL + run_id + "/"

def full_result_url(run_id):
    return FULL_RESULTS_URL + run_id


def remove_old_results():
    now = time.time()

    try:
        stamp = open(CLEANING_TIMESTAMP, 'w')
        stamp.write('%f'%now)
        stamp.close()

        for fname in os.listdir(RESULT_DIR):
            stats = os.stat(os.path.join(RESULT_DIR, fname))

            difference = (now - stats[8]) / 60.0 / 60.0
            
            if difference >= REMOVING_INTERVAL:
                os.system('rm -rf ' + os.path.join(RESULT_DIR, fname))
    except:
        err = open(TRACE_LOG, 'a')
        traceback.print_exc(file=err)
        err.close()
        
def clean_results():
    try:
        stamp = open(CLEANING_TIMESTAMP, 'r')
        last_clean = float(stamp.read())
        stamp.close()
        now = time.time()

        difference = (now - last_clean) / 60.0 / 60.0

    except:
        difference = CLEANING_INTERVAL + 1
    
    if difference >= CLEANING_INTERVAL:
        remove_old_results()

