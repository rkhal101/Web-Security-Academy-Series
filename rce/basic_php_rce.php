<?php
  // Vulnerable code that dynamically includes a file based on user input
  $page = $_GET['page']; // User-controlled input

  // Vulnerable include statement
  include($page . '.php');
?>
