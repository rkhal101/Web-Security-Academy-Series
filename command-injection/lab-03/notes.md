# Lab 3 - Blind OS command injection with output redirection

**YouTube video & lab links below:**

[Command Injection - Lab #3 Blind OS command injection with output redirection | Long Version](https://youtu.be/Gf2_UWsYrpM?list=PLuyTk2_mYISK9ywsFZZOT1LuO3Eb7Wq5q)

[Lab: Blind OS command injection with output redirection](https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection)

```
This lab contains a blind OS command injection vulnerability in the feedback function.

The application executes a shell command containing the user-supplied details. The output from the command is not returned in the response. However, you can use output redirection to capture the output from the command. There is a writable folder at:
/var/www/images/

The application serves the images for the product catalog from this location. You can redirect the output from the injected command to a file in this folder, and then use the image loading URL to retrieve the contents of the file.

To solve the lab, execute the whoami command and retrieve the output.

```

### Target Goal - Exploit the blind command injection and redirect the output from the whoami command to the `/var/www/images`


#### Analysis:

**1. Confirm blind command injection: Email Field**

**2. Check where images are store**

**3. Redirect output to file**

**4. Check if file was created**

 
