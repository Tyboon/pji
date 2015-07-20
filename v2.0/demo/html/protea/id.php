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

<h2> Retrieve result with an ID</h2>

<div class="formulaire">
<form id="form_id" method="post">
<p>The ID remains valid 1 week after sequence submission.</p>
<p> 

<strong>  Enter the ID :</strong>  
<input type="hidden" name="command" value="result"/>
<input id="run_id" type="text" name="run_id" size="20" />
<input type="submit" value="Get results" /></p>

</form>
</div>

</div></div><!-- bloc droit-->

<?php require("../lib.inc")?>
<?php footer("PROTEA","Protea", "protea@lifl.fr","2013"); ?>
</div>                                                                                

</body>                                        
</html>        