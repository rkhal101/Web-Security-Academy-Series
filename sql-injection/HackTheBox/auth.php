<?php

mysql_connect("localhost", "db_username", "db_password"); # Connection to the SQL
Database.
mysql_select_db("users"); # Database table where user information is stored.

$username=$_POST['username']; # User-specified username.
$password=$_POST['password']; #User-specified password.

$sql="SELECT * FROM users WHERE username='$username' AND password='$password'";
# Query for user/pass retrieval from the DB.

$result=mysql_query($sql);
# Performs query stored in $sql and stores it in $result.

$count=mysql_num_rows($result);
# Sets the $count variable to the number of rows stored in $result.


if ($count==1){
    # Checks if there's at least 1 result, and if yes:
    $_SESSION['username'] = $username; # Creates a session with the specified $username.
    $_SESSION['password'] = $password; # Creates a session with the specified $password.
    header("location:home.php"); # Redirect to homepage.
}

else { # If there's no singular result of a user/pass combination:
 header("location:login.php");
 # No redirection, as the login failed in the case the $count variable is not equal to 1,
HTTP Response code 200 OK.
}

else { # If there's no singular result of a user/pass combination:
 header("location:login.php");
 # No redirection, as the login failed in the case the $count variable is not equal to 1,
HTTP Response code 200 OK.
}

?>
