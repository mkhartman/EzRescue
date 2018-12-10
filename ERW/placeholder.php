<?php


$temp = exec("python3 placeholder.py")
header( "Location: $temp" );
die();


?>
