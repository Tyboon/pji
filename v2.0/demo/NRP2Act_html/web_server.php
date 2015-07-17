<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <link style="text/css" rel="stylesheet" href="/Style/css/bioinfo.css" />
    <link style="text/css" rel="stylesheet" href="/Style/css/page_theme.css" />
    <link href="/NRP2Act/NRP2Act.css" rel="stylesheet" style="text/css"/>
    <script type="text/javascript" src="/libs/jquery-1.11.3.min.js"></script>
    <script type="text/javascript" src="/libs/jquery.history.js"></script>
    <script type="text/javascript" src="/scripts/bioinfo.js"></script>
    <script type="text/javascript" src="/example_web_server/js/script.js"></script>   
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
   <h1 id="title">Web server</h1>                 
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
	<td class="label">Enter a <b>graph composition</b> for the NRP : 
	  <input id="decompo" type="text" name="decompo" size="200" />
	</td>
      </tr>
      <tr>
	<td><input id="dec" type="submit" name="submit" value="Submit" /></td>
      </tr>
    </table>
  </div>

  <div class="center">
    <input type="submit" id="reset" name="reset" value="Reset" /> 
    <input type="submit" id="run" name="button" value="Run Example" />
    <input type="hidden" name="command" value="request" /> 
  </div>

</form>

</div><!--bloc -->
</div><!-- main-->

<!-- chargement de la librairie php lib.inc -->
   <?php require("../lib.inc")?>
<!-- appel de la fonction footer qui permet d'afficher au bas de la page (nom du logiciel, un lien vers le mail, la date de modif -->
<!-- A modifier en fonction de votre logiciel -->
   <?php footer("NRP2Act","NRP2Act", "alan.lahure@univ-lille1.fr","2015"); ?>
                                                                                


</body>                                        
</html>        

