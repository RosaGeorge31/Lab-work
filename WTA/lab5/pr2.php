<?php
	session_start(); 
	$val = session_id();
if(isset($_SESSION['page_count']))
{
     $_SESSION['page_count'] += 1;
}
else
{
     $_SESSION['page_count'] = 1;
}
 echo 'You are visitor number ' . $_SESSION['page_count'];
$cookie_name = 'user';
$cookie_value = 'values';
setcookie($cookie_name, $cookie_value, time() + (86400 * 30), '/'); // 86400 = 1 day

if(!isset($_COOKIE[$cookie_name])) {
  print '<br>Cookie with name "' . $cookie_name . '" does not exist...';
} else {
  print '<br>Cookie with name "' . $cookie_name . '" value is: ' . $_COOKIE[$cookie_name];
}
echo '<br>Session id: '. $val;
unset($_COOKIE[$cookie_name]);
// empty value and expiration one hour before
$res = setcookie($cookie_name, '', time() - 3600);
 //session_destroy();
    ?>