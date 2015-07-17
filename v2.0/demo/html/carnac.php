<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link style="text/css" rel="stylesheet" href="/Style/css/page_theme.css" />
    <link href="/carnac/carnac.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="/libs/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
    <!--<script type="text/javascript" src="/scripts/bioinfo.js"></script>-->
    <script type="text/javascript" src="/scripts/bioinfo.js"></script>
   <script type="text/javascript" src="/carnac/js/script.js"></script>
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
   <h1 id="title">carnac :: RNA structure inference</h1>                 
   </div>
   
   <div id="center_sup">
     <div class="theme-border" style="display:none"></div>
     <div id="link_home" style="display:inline-block"><a href="/" class="text_onglet"><img src="/Style/icon/home_w.png" alt="home_general"/></a></div>
   <div class="tabs" id="menu_central" style="display:inline-block"><?php include("menu_central.txt")?></div>
   </div>
   <div id="main">
    <div id="center">
<!--<h2>Predicting secondary structure for a set of homologous RNA sequences</h2>-->
      <h2>What is Carnac ?</h2>
<p>

Carnac is a software tool for analysing the hypothetical secondary
structure of a family of homologous RNA.  It aims at predicting if the
sequences actually share a common secondary structure.  When this
structure exists, Carnac is then able to correctly recover a large
amount of the folded stems.  The input is a set of single-stranded
RNA sequences that need not to be aligned.  The folding strategy
relies on a thermodynamic model with energy minimization. It combines
information coming from locally conserved elements of the primary
structure and mutual information between sequences with covariations
too.
</p>
<ul>
     <li> <a href="/carnac/examples.php" class="aLoad">See examples</a></li>
     <li> <a href="/carnac/name.php" class="aLoad"">Where does the name <i>Carnac</i> come from ?</a></li>
</ul>



<h2>Visualization</h2>

<p>
Carnac produces CT files.  One can get a  2D representation of the secondary structure using 
 one of the two viewers:</p>
<ul>
     <li> <b>Naview </b>  is a freely-distributed program that produces plots of RNA secondary structure 
 </li>
     <li> <b>RNAfamily</b>  is a home-made viewer that allows to display several secondary structures on the same drawing 
using  backbone representation [<a href="/RNAfamily/rnafamily.php" >More information on RNAfamily</a>]</li>
</ul>


<h2>Availability</h2>

<p>
You can use Carnac via the <a href="/carnac/form.php" class="aLoad">web interface</a>. 
It is also possible to download and install it locally (<a href="/carnac/src/carnac.tar.gz">carnac.tar.gz</a> and <a href="/carnac/src/README">read_me</a>).
You need a C compiler. <br />
A Windows executable is also available in this <a href="/carnac/src/carnac-Win32.zip">zip archive</a> .
</p>

<h2>References</h2>
<p>
Touzet H. and Perriquet O.<br/>
CARNAC: folding families of non coding RNAs.<br/>
<i>Nucleic Acids Research</i> 142, 2004 [<a href="http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&amp;db=pubmed&amp;dopt=Abstract&amp;list_uids=15215367">pubmed</a>]
</p>

<p>
Perriquet O, Touzet H, Dauchet M.<br/>
Finding the common structure shared by two homologous RNAs.<br/>
<i>Bioinformatics</i> 19(1):108-16, 2003 Jan [<a href="http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&amp;db=PubMed&amp;list_uids=12499300&amp;dopt=Abstract">pubmed</a>]
</p>
</div></div><!-- bloc droit-->

<?php require("../../lib.inc")?>
<?php footer("Carnac","CARNAC", "carnac@univ-lille1.fr","2013"); ?>
</div>                                                                                

</body>                                        
</html>        


