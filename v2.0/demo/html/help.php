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
<h2>Submission form</h2>

<p>

<a name="fasta"></a> 
Your data set should include <b>at least two</b> distinct RNA sequences, 
and sequences should be in <b>FASTA</b> format.
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
 are accepted. They are simply ignored by Carnac.
</p>  

<p>
Carnac offers several parameters that determine the final predictions
The most reasonable choice is to use default values. This choice leads to the 
most reliable results in average.
</p>

<p>
<a name="eliminate"></a><b>Eliminate redundant sequences</b><br />
By default, CARNAC discards sequences that are too close
(more than 98% of identity). You should uncheck the box if you 
want all your sequences to be folded.
</p>

<p>
<a name="gccontent"></a><b>Take GC content into consideration</b><br />
 When this option is selected, Carnac
uses variable energy thresholds for stems according to the average GC percent
of the involved sequence.
</p>

<p>
<a name="single"></a><b>Allow isolated stems</b> <br />
When this option is selected, Carnac permits the 
creation of stems in one sequence alone, without any counterpart in any other sequence.
This option may give better results if there is a large evolutionnary distance
between structures, or when the sequences are of different lengths. 
But it is time and space consuming. So it should be selected 
with caution.
</p>



<h2>Ouput files</h2>
</br>
<p>
For each sequence, Carnac computes a putative secondary structure. The result is stored in four formats: CT, JPEG, PS, and as a list of contrained base pairings.
 JPEG and PS files are both automatically produced from the CT file
using NAview.  It is also possible to
visualize all structures in the same window with the home-made Java
applet <a target="RNAfamily" href="/RNAfamily/rnafamily.php">RNAfamily</a>.
</p>

<p>
If no structure is detected,
then the message <b>No structure found</b> is displayed. 
</p>

<p>
<b>CT</b> - <i>Connectivity Table format</i> <br />
This is a text file which contains the nucleic acid sequence
 and base pairing information from which a structure plot may be computed.
</p>

<p>
<b>JPEG</b> - <i>Joint Photographic Experts Group format</i> <br />
 This is a graphical format that produces inline images for web-pages and documents.
</p>

<p>
<b>PS</b> - <i>PostScript format</i><br />
 This is a ready-to-print high quality vector format. 
It may require additional tools for viewing, such as gsview.
</p>

<p>
<b>List of constraints</b> - this file describes the structure as a set of initial contraints for external programs, such as 
 <a href="http://kinefold.curie.fr/" target=kine>Kinefold</a> or <a href="http://www.bioinfo.rpi.edu/applications/mfold/" target=mfold>Mfold</a>.
Each line corresponds to one helix: <tt> F i j k</tt> forces the formation of base pairs
<tt>i.j</tt>, <tt>i+1.j-1</tt>, ... , <tt>   i+k-1.j-k+1</tt>.  
</p>

<p>
It is also possible to download an archive storing all result files (ct, ps, jpeg and constraints). 
</p>

<h2>Retrieve result with an ID</h2>
</br>
<p>
Each job is assigned an identifier, that allows to retrieve folding results. 
Files are stored for 24h after job submission.
</p> 
</div></div><!-- bloc droit-->

   <?php require("../../lib.inc")?>
   <?php footer("Carnac","CARNAC", "carnac@univ-lille1.fr","2013"); ?>


</body>                                        
</html>        


