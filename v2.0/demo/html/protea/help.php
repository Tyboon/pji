<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link href="/Style/css/page_theme.css" rel="stylesheet" style="text/css"/>
   <link href="/protea/protea.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="/libs/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
    <!--<script type="text/javascript" src="/scripts/bioinfo.js"></script>-->
    <script type="text/javascript" src="/scripts/bioinfo.js"></script>
   <script type="text/javascript" src="/protea/js/script.js"></script>   
   <title>Bonsai  :: Bioinformatics Software Server</title>
    <script type="text/javascript">
        var i_am_old_ie = false;
    </script>
    <!--[if LT IE  9]>
    <script type="text/javascript">
            i_am_old_ie = true;
    </script>
    <![endif]-->
  </head>
  <body>
   
   
    <div class="frametitle">
   <h1 id="title">protea :: protein coding gene prediction</h1>                 
   </div>
   <div id="center_sup">
        <div class="theme-border" style="display:none"></div>
    <div id="link_home" style="display:inline-block"><a href="/" class="text_onglet"><img src="/Style/icon/home_w.png" alt="home_general"/></a></div>
   <div class="tabs" id="menu_central" style="display:inline-block"><?php include("menu_central.txt")?></div>
   </div>
   <div id="main">
    <div id="center">
<h2>Submission form</h2>

<p>

<a name="fasta"></a> 
Your data set should include <strong>at least two</strong> distinct RNA sequences, 
and sequences should be in <strong>FASTA</strong> format.
A sequence in FASTA format consists of a
        single-line description, followed by lines of sequence
        data. The first character of the description line is a
        greater-than (&quot;&gt;&quot;) symbol in the first
        column. All lines should be shorter than 80 characters.
</p>

<p>
Example of FASTA format:
</p>
<div class="exemple">
<pre>
> Name of the sequence 1
ctgcgagcgcgcgatgatagcgcggcgagcatgtagcatgctagctgtcgcgagcact
cggccgagatcaggcgatgcatgcgcagggagcagcgagcgacgagcacagcatgcta
gctagatgcatgctgtaggcagc
cgccgagagacgatggagctgc
> Name of the sequence 2
gacagatacgataagaggacgggatagaacgtagacatcgccgagagacgatggagctgc
cggccgagatcaggcgatgcatgcgcagggagcaggcgagcatgtagcatgctagctgtc
gcgagcact
</pre>
</div>

<p>
Lower-case and upper-case letters are both accepted.
The full  standard IUPAC nucleic acid code is not supported: 
only <tt>A</tt>, <tt>C</tt>, <tt>G</tt>, <tt>T</tt> and <tt>U</tt> symbols are recognized.
Numerical digits <tt>0</tt>, ..., <tt>9</tt>, <tt>-</tt> and dot <tt>.</tt> symbols
 are accepted. They are simply ignored by Protea.
</p>  

<p>
Protea offers several parameters that determine the final predictions
The most reasonable choice is to use default values. This choice leads to the 
most reliable results in average.
</p>
</div></div><!-- bloc droit-->

<?php require("../lib.inc")?>
<?php footer("PROTEA","Protea", "protea@lifl.fr","2013"); ?>
</div>                                                                                

</body>                                        
</html>        
