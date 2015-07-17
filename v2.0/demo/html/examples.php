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
<h2>RNase P RNA</h2>



<ul>
<li> RNA sequences : <a href="/carnac/RNase/rnase.fasta">see data set</a></li>
<li> Results of Carnac (CT files) : <a href="/carnac/RNase/RNaseP1.ct">structure 1</a>,  <a href="/carnac/RNase/RNaseP2.ct">structure 2</a>,  <a href="/carnac/RNase/RNaseP3.ct">structure 3</a>,  <a href="/carnac/RNase/RNaseP4.ct">structure 4</a>,  <a href="/carnac/RNase/RNaseP5.ct">structure 5</a></li>
</ul>


<p>
We have selected the Delta/Epsilon Purple Bacteria RNase P sequences
available in the <a href="http://jwbrown.mbio.ncsu.edu/RNaseP/" target="RNaseP">RNaseP database</a> developped by J.W. Brown. These RNAs present a common structure, in spite of the weak sequence
conservation (60% of identity in average).
We kept only full and
non redundant sequences. This gives five sequences:  
<i>D.desulfuricans</i> (M59357),
<i>D.vulgaris</i>,
<i>G.sulfurreducens</i>,
<i>C.jejuni</i> (AL139075),
<i>H.pylori</i> (AE000573).

We compare the secondary structure predicted by Carnac to the reference structure provided by the database. For the reference organism (<i>D.desulfuricans</i>), 
the real structure has around 15 stems, plus 2 pseudoknots. Some stems are not 
present in the structure of the other organisms.
</p>


<div class="center">
<table class="default">
<tr><th>  Organism </th><th> Number of <br />predicted stems </th><th> Correctness <br /> percentage</th></tr>
<tr><td><i> D.desulfuricans</i></td><td align="center">11 </td><td align="center">100%</td></tr>
  <tr><td><i> D.vulgaris</i></td><td align="center">10 </td><td align="center">100%</td></tr>
 <tr><td><i>G.sulfurreducens</i></td><td align="center"> 10 </td><td align="center">100%</td></tr>
 <tr><td><i>C.jejuni</i></td><td align="center"> 11 </td><td align="center">81%</td></tr>
<tr><td><i> H.pylori</i></td><td align="center"> 11 </td><td align="center">81%</td></tr>
</table>
</div>


<p>
Usual thermodynamic folding programs that work with a single sequence usually fail on that data set.
</p>

<h2>Ciliate telomerase RNA</h2>

<ul>
<li> RNA sequences : <a href="/carnac/Telomerase/telomerase.fasta">see data set</a></li>
<li> Results of Carnac (CT files) : <a href="/carnac/Telomerase/telomerase1.ct">structure 1</a>, <a href="/carnac/Telomerase/telomerase2.ct">structure 2</a>, <a href="/carnac/Telomerase/telomerase3.ct">structure 3</a></li>
</ul>

<p>
Telomerase is a ribonucleoprotein reverse transcriptase that synthesises telomeric DNA.  Sequences are available from
the <a href="http://www.sanger.ac.uk/Software/Rfam/index.shtml" target="RFAM">RFAM database</a>, with  accession number 
<a href="http://rfam.sanger.ac.uk/family/RF00025"> RF00025</a>. We selected three sequences
with poor primary structure conservation, that can not be correctly aligned with usual multiple alignment automatic methods.
The three structures predicted by Carnac are consistent with the model available in RFAM.
</p>

<div class ="center">
<img src="/carnac/Telomerase/telomerase1.jpeg" width="300" alt="telomerase1" />
<img src="/carnac/Telomerase/telomerase2.jpeg" width="300" alt="telomerase2" />
<img src="/carnac/Telomerase/telomerase3.jpeg" width="300" alt="telomerase3" />
</div>



<h2>When there is no structure : Enterovirus</h2>


<ul>
<li> RNA sequences : <a href="/carnac/Enterovirus/enterovirus.fasta">see data set</a></li>
<li> Results of Carnac (CT files) :
<a href="/carnac/Enterovirus/entero1.ct">structure 1</a>, 
<a href="/carnac/Enterovirus/entero2.ct">structure 2</a>,
<a href="/carnac/Enterovirus/entero3.ct">structure 3</a>,
<a href="/carnac/Enterovirus/entero4.ct">structure 4</a>,
<a href="/carnac/Enterovirus/entero5.ct">structure 5</a>,
<a href="/carnac/Enterovirus/entero6.ct">structure 6</a>,
<a href="/carnac/Enterovirus/entero7.ct">structure 7</a>,
<a href="/carnac/Enterovirus/entero8.ct">structure 8</a>,
<a href="/carnac/Enterovirus/entero9.ct">structure 9</a>,
<a href="/carnac/Enterovirus/entero10.ct">structure 10</a>,
<a href="/carnac/Enterovirus/entero11.ct">structure 11</a>
</li> 
</ul>

<p>
The program may also be used to analyze RNA sequences that are not functionnaly structured, or only with a partial structure.
We ran Carnac on a set of messenger RNA sequences of enterovirus, coding for a polyprotein: each sequence is 1800 nt long, and is 
composed of 5'UTR  (700 nt approximately) and the beginning of the ORF (1100 nt approximately) .
The 5' UTR is believed to share a common structure, but not the coding region 
(<a href="http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=Retrieve&amp;db=PubMed&amp;list_uids=2175364&amp;dopt=Abstract.">Le SY, Zuker M.</a>).
The figure below shows that all stems predicted by Carnac are located in the 5'UTR, before the START codon.'
</p>

<div class="center">
<img src="/carnac/Enterovirus/x1.jpg" alt="enterovirus1" /><br />
<img src="/carnac/Enterovirus/x2.jpg" alt="enterovirus2" /><br />
<img src="/carnac/Enterovirus/x3.jpg" alt="enterovirus3" /><br />
<img src="/carnac/Enterovirus/x4.jpg" alt="enterovirus4" /><br />
<img src="/carnac/Enterovirus/x5.jpg" alt="enterovirus5" /><br />
<img src="/carnac/Enterovirus/x6.jpg" alt="enterovirus6" /><br />
<img src="/carnac/Enterovirus/x7.jpg" alt="enterovirus7" /><br />
<img src="/carnac/Enterovirus/x8.jpg" alt="enterovirus8" /><br />
<img src="/carnac/Enterovirus/x9.jpg" alt="enterovirus9" /><br />
<img src="/carnac/Enterovirus/x10.jpg" alt="enterovirus10" /><br />
<img src="/carnac/Enterovirus/x11.jpg" alt="enterovirus11" /><br />
<img src="/carnac/Enterovirus/x12.jpg" alt="enterovirus12" /><br />
</div>

 </div></div>
   <?php require("../../lib.inc")?>
   <?php footer("Carnac","CARNAC", "carnac@univ-lille1.fr","2013"); ?>

</body>                                        
</html>        


