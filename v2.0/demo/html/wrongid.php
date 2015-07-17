<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
<link title="test" type="text/css" rel="stylesheet" href="/RNA/rna.css" />
<title>
CARNAC
</title>
</head>
<body>
<? include '/bio1/www/html/Style/lib.inc'; ?>

<? entete("CARNAC","retrieve result with an ID"); ?>
<? menu_central("RNA/carnac"); ?>
    <div class="section">

<div class="error">
This is not a valid ID !
</div>

<div class="bande_formulaire">
<form method="post" action="/cgi-bin/RNA/carnac/result.pl">
<p>The ID remains valid 24 hours after sequence submission.</p>
<p>
<b>  Enter the ID :</b>  
<input type="text" name="ident" size="20" />
<input type="submit" value="Go" /></p>
</form>
</div>

  </div><!-- section -->
<? footer("CARNAC","carnac","carnac@lifl.fr"); ?>
