<?php

$name = $_GET['name'];
$phone = $_GET['pnum'];
$addr =$_GET['addr'];
$sdisc =$_GET['sdisc'];
$ldisc =$_GET['ldisc'];
$time = date('Y-m-d H:i:s');
$id = mt_rand(100000,999999);


# Print the ticket
echo "Your submitted ticket:</br></br>";
echo "Submitted: $time</br>";
echo "Ticket ID: $id</br></br>";
echo "Name: $name</br>";
echo "Phone number: $phone</br>";
echo "Address: $addr</br>";
echo "Description: $sdisc</br>";
echo "Additional information: $ldisc</br>";

exec("bash mktic.sh $id");

exec("touch tickets/$id.tic; pwd");
echo exec("cd tickets; pwd");

# Actually make the ticket
#$file = fopen("tickets/$id.tic", "w") or die("</br>ERROR CREATING TICKET!");
#fwrite($file, "Something  here");
#fclose($file);



?>
