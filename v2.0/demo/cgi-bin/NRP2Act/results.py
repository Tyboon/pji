#!/usr/bin/python
# -*- coding: utf-8 -*-

import common as pc
import os
import re
import sys
import cgitb
import cgi

cgitb.enable()



def format_error_message(msg):
    return '<li><span style="font-weight:bold; color:#FF0000;font-size:150%%;">' + msg + '</span></li>'


def header(result_return):
    result_return =result_return+"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link href="/protea/protea.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
    <script type="text/javascript" src="/scripts/bioinfo_propre.js"></script>
    <script type="text/javascript" src="/protea/js/script.js"></script>
    <title>Bonsai  :: Bioinformatics Software Server</title>
    </head>
    <body> 
    <div class="frametitle">
    <h1 id="title">NRP2Act : NRP activity prediction</h1>                 
    </div>
    <div id="center_sup">
    <div class="theme-border" style="display:none"></div>
    <div id="link_home" style="display:inline-block"><a href="/" class="text_onglet"><img src="/Style/icon/home_w.png" alt="home_general"/></a></div>
    <div class="tabs" id="menu_central" style="display:inline-block"><?php include("../../menu_central.txt")?></div>
    </div>
    <div id="main">
    <div id="center">"""
    return result_return



def footer(result_return):
    result_return=result_return+"""    </div></div><!-- bloc droit-->
    <?php require("../../../lib.inc")?>
    <?php footer("Example_web_server","Example_web_server", "alan.lahure@univ-lille1.fr","2015");?>
    </div>                                                                             
    </body>                                        
    </html>"""
    return result_return
