<?php
echo "Your requested information: ";
echo shell_exec("cd python; python3 management.py > temp.txt; cat temp.txt");

?>

