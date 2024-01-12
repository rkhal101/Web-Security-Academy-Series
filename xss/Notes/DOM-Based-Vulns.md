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

### Common sources

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

## DOM-based XSS
