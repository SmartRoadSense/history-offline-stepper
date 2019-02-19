<?php


define("PRINT_PID", true);

ob_implicit_flush(true);
if (ob_get_length()) ob_end_clean();

$values = explode(",", getenv('args'));

echo "Data received: ".str_replace(array("\r", "\n"), ' ', print_r($values, true)).PHP_EOL;

if (ob_get_length()) ob_end_clean();
