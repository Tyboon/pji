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
<form id="formulaire" method="post" enctype="multipart/form-data">
  <div class="formulaire">
    <p>
      <strong>Paste</strong> your nucleic sequences in multi-FASTA format<br />
      <textarea id="paste_seq" name="seqtext" rows="15" cols="80"></textarea><br />
      or <strong>Upload</strong> a multi-FASTA file
           <input type="file" name="seqfile"></input>
      <br/><br/>
      <input id="ex1" type="submit" name="example" value="Example 1" />
      <input id="ex2" type="submit" name="example" value="Example 2" />
      <br />
    </p>
  </div>
  
  <div class="formulaire">
    <p>
      <input id="reverse" type="checkbox" name="reverse" checked="checked" />
      Use both strands<br />
      
      <input id="aln" type="checkbox" name="aln" checked="checked" />
      Produce a multiple alignment
      <select id="alnmeth" name="alnmeth">
        <option value="C">ClustalW</option>
        <option value="T">T-Coffee</option>
        <option value="D">Dialign2</option>
      </select>
    </p>
    
    <p>
      Your <strong>email address</strong> (optional) <input id="email" type="text" name="email" size="25" />
    </p>
  </div>


    <p>
      <input id="reset" type="reset" name="reset" value="Reset" />
      <input id="run" type="submit" name="button" value="Run Protea" />
      <input type="hidden" name="command" value="request" />
    </p>
 
   
</form>

</div></div><!-- bloc droit-->

<?php require("../lib.inc")?>
<?php footer("PROTEA","Protea", "protea@lifl.fr","2013"); ?>
</div>                                                                                

</body>                                        
</html>        
