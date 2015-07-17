<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link style="text/css" rel="stylesheet" href="/Style/css/page_theme.css" />
    <link href="/carnac/carnac.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="/libs/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
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
<form id="formulaire" method="post">
  <div class="formulaire">
    <table class="vide">
      <tr>
	<td class="label">Enter a <b>name</b> for the sequences 
	  <i>(optional) </i> : 
	  <input id="seq_name" type="text" name="seq_name" size="20" />
	</td>
      </tr>
    </table>
  </div>

  <div class="formulaire">
    <table class="vide">
      <tr>
	<td class="label"><b>Paste</b> your RNA sequences in FASTA
	  format &nbsp;&nbsp;[<a href="/carnac/help.php#fasta">?</a>]
	</td>
      </tr>
      <tr>
	<td>
	  <textarea id="paste_seq" name="sequence" rows="15" cols="40"></textarea>
	</td>
      </tr>
      <tr>
	<td>
	  or
	</td>
      </tr>
      <tr>
	<td class="label"> 
	  <B>upload</B> a file
	  <input type="file" name="file" value="file"></input>
	</td>
      </tr> 
      <tr>
	<td><input id="ex1" type="submit" name="example" value="Example" /></td>
      </tr>
    </table>
  </div>

  <div class="formulaire">
    <table class="vide">
     <tr><B>Options</B></tr>
      <tr>
	<td class="label">
	  <input id="GC" type="checkbox" name="GC" value="pourcentage GC" />
	  Disable threshold correction according to GC%
	  [<a href="/carnac/help.php#gccontent">?</a>]
	</td>
    </tr>
    <tr>
    <td class="label">
	  <input id="threshold" type="checkbox" name="threshold" value="threshold sequence redundant" checked />
	  Eliminate redundant sequences
	  [<a href="/carnac/help.php#eliminate">?</a>]
	</td>
      </tr>
    </table>
  </div>


  <div class="formulaire">
    <table class="vide">
      <tr>
	<td class="label"> 
	  Enter your <b>E-mail</b> address <i>(optional)</i>: 
	  <input id="email" type="text" name="email" size="20" />
	</td>
      </tr>
    </table>
  </div>

  <div class="center">
    <input type="submit" id="reset" name="reset" value="Reset" /> 
    <input type="submit" id="run" name="button" value="Run CARNAC" />
    <input type="hidden" name="command" value="request" /> 
  </div>

</form>

</div></div><!-- bloc droit-->


			       <?php require("../../lib.inc")?>
			       <?php footer("Carnac","CARNAC", "carnac@univ-lille1.fr","2013"); ?>
                                                                                


</body>                                        
</html>        

