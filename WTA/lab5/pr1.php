<html>
	<head>
		<title>Hello world!</title>
	</head>
	<body>
		<?php
			date_default_timezone_set('America/Chicago'); // CDT
			echo "Time right now: ";
			$current_date = date('H:i:s');
			echo $current_date;
			$greeting = array();
			$greeting[0] = "hi";
			$greeting[1] = "hello";
			$greeting[2] = "How are you?";
			$greeting[3] = "Have a nice day";
			$greeting[4] = "Happy morning";
			echo "<br>";
			mt_srand((double)microtime()*10000);
			$n = mt_rand(0,4);
			if ($n==0)
				print $greeting[0];
			else if ($n==1)
				print $greeting[1];
			else if ($n==2)
				print $greeting[2];
			else if ($n==3)
				print $greeting[3];
			else 
				print $greeting[4];
			?>
	</body>
</html>