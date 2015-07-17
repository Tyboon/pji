<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link title="test" type="text/css" rel="stylesheet" href="/RNA/rna.css" />
<title>CARNAC : error message</title>
</head>
<body>

<? include '/bio1/www/html/Style/lib.inc'; ?>

<? entete("CARNAC","error"); ?>
<? menu_central("RNA/carnac"); ?>
    <div class="section">



<div class="error">Error ! </div>

<p>
Carnac could not recognize the format of one or more sequences.
</p>

<ul>
<li> Your data set should include <b>at least two</b> distinct sequences.</li>
</ul>
<ul>
<li> Sequences should be in <b>FASTA</b> format.
A sequence in FASTA format consists of a
        single-line description, followed by lines of sequence
        data. The first character of the description line is a
        greater-than (&quot;&gt;&quot;) symbol in the first
        column. All lines should be shorter than 80 characters. An
        example  in FASTA format is: 

<div class="exemple">        
<pre>
> Name of the sequence 1
ctgcgagcgcgcgatgatagcgcggcgagcatgtagcatgctagctgtcgcgagcact
cggccgagatcaggcgatgcatgcgcagggagcagcgagcgacgagcacagcatgctagctagatgcatgctgtaggcagc
cgccgagagacgatggagctgc
> Name of the sequence 2
gacagatacgataagaggacgggatagaacgtagacatcgccgagagacgatggagctgc
cggccgagatcaggcgatgcatgcgcagggagcaggcgagcatgtagcatgctagctgtcgcgagcact
</pre>
</div>
</li>
</ul>
<ul>
<li>  <b>Lower-case and upper-case</b> letters are both
        accepted.</li>
</ul>
<ul>
<li>  The full  standard <b>IUPAC</b> nucleic acid code is not supported : only <tt>A</tt>, <tt>C</tt>, <tt>G</tt>, <tt>T</tt> and <tt>U</tt> symbols are recognized.</li>
</ul>
<ul>
<li>  <b>Numerical digits <tt>0</tt>, ..., <tt>9</tt>, <tt>-</tt> and dot <tt>.</tt></b> symbols are accepted. They are simply ignored by Carnac.</li>
  
</ul>

<br /><br />

<div class="center">
  <input type="button" name="nom" value="Submit a new job"
onclick="window.location.href='/RNA/carnac/carnac.php'" />
</div>

  </div><!-- section -->

<? footer("CARNAC","carnac","carnac@lifl.fr"); ?>