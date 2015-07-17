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



<div class="error">program error ! </div>

<div class="dialog">
 Please report bug at <a href=mailto:carnac@lifl.fr>carnac@lifl.fr</a>
</div>


<div class="center">
  <input type="button" name="nom" value="Submit a new job"
onclick="window.location.href='../../carnac/carnac.php'" />
</div>

  </div><!-- section -->
<? footer("CARNAC","carnac","carnac@lifl.fr"); ?>