Lab #4 – DOM-based open redirection

Target Goal - Exploit the DOM-based open redirection vulnerability to redirect the victim to the exploit server.

Analysis:

<a href='#' onclick='returnUrl = /url=(https?:\/\/.+)/.exec(location); if(returnUrl)location.href = returnUrl[1];else location.href = "/"'>Back to Blog</a>

returnUrl = /url=(https?:\/\/.+)/.exec(location);
if(returnUrl)
    location.href = returnUrl[1];
else 
    location.href = "/"



url=http(s)://