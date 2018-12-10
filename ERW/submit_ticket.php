<?php

$name = $_GET['name'];
$phone = $_GET['pnum'];
$addr =$_GET['addr'];
$sdisc =$_GET['sdisc'];
$ldisc =$_GET['ldisc'];
$time = date('Y-m-d H:i:s');
$id = mt_rand(100000,999999);
$directions = exec("get_directions.py -addr $addr")

# Print the ticket
echo "Your submitted ticket:</br></br>";
echo "Submitted: $time</br>";
echo "Ticket ID: $id</br></br>";
echo "Name: $name</br>";
echo "Phone number: $phone</br>";
echo "Address: $addr</br>";
echo "Description: $sdisc</br>";
echo "Additional information: $ldisc</br>";
echo "Directions: $directions</br>";

exec("touch tickets/$id.tic");

# Actually make the ticket
$file = fopen("tickets/$id.tic", "w") or die("</br>ERROR CREATING TICKET!");
fwrite($file, "Your submitted ticket:</br></br>");
fwrite($file, "Submitted: $time</br>");
fwrite($file, "Ticket ID: $id</br>");
fwrite($file, "Name: $name</br>");
fwrite($file, "Phone number: $phone</br>");
fwrite($file, "Address: $addr</br>");
fwrite($file, "Description: $sdisc</br>");
fwrite($file, "Additional information: $ldisc</br>");
fwrite($file, "Directions: $directions</br>");
fclose($file);

?>
