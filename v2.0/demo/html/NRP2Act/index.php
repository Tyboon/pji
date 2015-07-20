<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link style="text/css" rel="stylesheet" href="/Style/css/page_theme.css" />
    <link href="/NRP2Act/NRP2Act.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="/libs/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
    <script type="text/javascript" src="/scripts/bioinfo.js"></script>
   <script type="text/javascript" src="/example_web_server/js/script.js"></script>
   <title>bonsai  :: Bioinformatics Software Server</title>
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
   <h1 id="title">Example web server</h1>                 
   </div>
   
   <div id="center_sup">
     <div class="theme-border" style="display:none"></div>
     <div id="link_home" style="display:inline-block"><a href="/" class="text_onglet"><img src="/Style/icon/home_w.png" alt="home_general"/></a></div>
   <div class="tabs" id="menu_central" style="display:inline-block"><?php include("menu_central.txt")?></div>
   </div>
   <div id="main">
    <div id="center">
     <!--Partie à modifier-->
      <h2>What is NRP2Act?</h2>
      <p> NRP2Act is a software that permits to predict NRP activity using its monomer decomposition and its structure.

	.... A DEVELOPPER 
      </p>
      </div><!-- center -->
    </div><!-- main-->

<!-- appel du fichier lib.inc contenant des fonctions php -->
<?php require("../lib.inc")?>

<!-- appel de la fonction footer qui permet d'afficher au bas de la page (nom du logiciel, un lien vers le mail, la date de modif -->
<!-- Modifier le nom Example_web_server par le nom de votre logiciel -->
<?php footer("Example_web_server","Example_web_server", "alan.lahure@univ-lille1.fr","2015"); ?>
</div>                                                                                

</body>                                        
</html>        
