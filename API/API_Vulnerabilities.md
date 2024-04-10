#  [OWASP API Security Top Ten - 2023](https://owasp.org/API-Security/editions/2023/en/0x00-header/)

# Mass Assignment Attacks

## [Mass Assignment: OWASP](https://owasp.org/API-Security/editions/2019/en/0xa6-mass-assignment/)


### Mass Assignment vulnerabilities are present when an attacker is able to overwrite object properties that they should not be able to. 
A few things need to be in play for this to happen. An API must have requests that accept user input, these requests must be able to alter values not available to the user, 
and the API must be missing security controls that would otherwise prevent the user input from altering data objects. 
The classic example of a mass assignment is when an attacker is able to add parameters to the user registration process that escalate their account from a basic user to an administrator. 
The user registration request may contain key-values for username, email address, and password. 
An attacker could intercept this request and add parameters like "isadmin": "true". 
If the data object has a corresponding value and the API provider does not sanitize the attacker's input then there is a chance that the attacker could register their own admin account.

### Finding Mass Assignment Vulnerabilities

One of the ways that you can discover mass assignment vulnerabilities by finding interesting parameters in API documentation and then adding those parameters to requests. 
Look for parameters involved in user account properties, critical functions, and administrative actions.

Additionally, make sure to use the API as it was designed so that you can study the parameters that are used by the API provider. 
Doing this will help you understand the names and spelling conventions of the parameters that your target uses. 
If you find parameters used in some requests, you may be able to leverage those in your mass assignment attacks in other requests. 

You can also test for mass assignment blind by fuzzing parameter values within requests. 
Mass assignment attacks like this will be necessary when your target API does not have documentation available. 
Essentially, you will need to capture requests that accept user input and use tools to brute force potential parameters. 
I recommend starting out your search for mass assignment vulnerabilities by testing your target's account registration process if there is one. 
Account registration is normally one of the first components of an API that accept user input. 
Once registration has been tested then you will need to target other requests that accept user input. 


The challenge with mass assignment attacks is that there is very little consistency in the parameters used between API providers. 
That being said, if the API provider has some method for, say, designating accounts as administrators, they may also have some convention for creating or updating variables to make a user an administrator. 
Fuzzing can speed up your search for mass assignment vulnerabilities, but unless you understand your target’s variables, this technique can be a shot in the dark. 

## You can use [Param Miner](https://portswigger.net/bappstore/17d2949a985c4b7ca092728dba871943) to fuzz for Mass Assignment 
**See the [Documentation](https://github.com/nikitastupin/param-miner-doc) for additional explanation.**

 <br>

# Broken Object Level Authorization(BOLA)
## This is number One on [OWASP Top 10 API Security Risks – 2023](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/)

When authorization controls are lacking or missing, UserA will be able to request UserB’s (along with many other) resources. APIs use values, such as names or numbers, to identify various objects. When we discover these object IDs, we should test to see if we can interact with the resources of other users when unauthenticated or authenticated as a different user. The first step toward exploiting BOLA is to seek out the requests that are the most likely candidates for authorization weaknesses. 

 When hunting for BOLA there are three ingredients needed for successful exploitation.

1.  Resource ID: a resource identifier will be the value used to specify a unique resource. This could be as simple as a number, but will often be more complicated.
2.  Requests that access resources. In order to test if you can access another user's resource, you will need to know the requests that are necessary to obtain resources that your account should not be authorized to access.
3.  Missing or flawed access controls. In order to exploit this weakness, the API provider must not have access controls in place. This may seem obvious, but just because resource IDs are predictable, does not mean there is an authorization vulnerability present.

The third item on the list is something that must be tested, while the first two are things that we can seek out in API documentation and within a collection of requests. Once you have the combination of these three ingredients then you should be able to exploit BOLA and gain unauthorized access to resources. 

 <br>

## Finding Resource IDs and Request

You can test for authorization weaknesses by understanding how an API’s resources are structured and then attempting to access resources you shouldn’t be able to access. By detecting patterns within API paths and parameters, you might be able to predict other potential resources. The bold resource IDs in the following API requests should catch your attention:

```
GET /api/resource/1
GET /user/account/find?user_id=15
POST /company/account/Apple/balance
POST /admin/pwreset/account/90
```


In these instances, you can probably guess other potential resources, like the following, by altering the bold values:

```
GET /api/resource/**3**
GET /user/account/find?user_id=**23**
POST /company/account/**Google**/balance
POST /admin/pwreset/account/**111**
```

In these simple examples, you’ve performed an attack by merely replacing the bold items with other numbers or words. If you can successfully access the information you shouldn’t be authorized to access, you have discovered an authorization vulnerability.

 <br>

 # Broken Function Level Authorization  
 ## This is number 5 on [OWASP Top 10 API Security Risks – 2023](https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/)
 ### BFLA is performing unauthorized actions

Where BOLA is all about accessing resources that do not belong to you, BFLA is all about performing unauthorized actions. BFLA vulnerabilities are common for requests that perform actions of other users. These requests could be lateral actions or escalated actions. Lateral actions are requests that perform actions of users that are the same role or privilege level. Escalated actions are requests that perform actions that are of an escalated role like an administrator. The main difference between hunting for BFLA is that you are looking for functional requests. This means that you will be testing for various HTTP methods, seeking out actions of other users that you should not be able to perform.

If you think of this in terms of a social media platform, an API consumer should be able to delete their own profile picture, but they should not be able to delete other users' profile pictures. The average user should be able to create or delete their own account, but they likely shouldn't be able to perform administrative actions for other user accounts. For BFLA we will be hunting for very similar requests to BOLA.

1.  Resource ID: a resource identifier will be the value used to specify a unique resource. 
2.  Requests that perform authorized actions. In order to test if you can access another update, delete, or otherwise alter other the resources of other users.
3.  Missing or flawed access controls. In order to exploit this weakness, the API provider must not have access controls in place. 

Notice that the hunt for BFLA looks familiar, the main difference is that we will be seeking out functional requests. When we are thinking of CRUD (create, read, update, and delete), BFLA will mainly concern requests that are used to update, delete, and create resources that we should not be authorized to. For APIs that means that we should scrutinize requests that utilize POST, PUT, DELETE, and potentially GET with parameters.  We will need to search through the API documentation and/or collection for requests that involve altering the resources of other users. So, if we can find requests that create, update, and delete resources specified by a resource ID then we will be on the right track. If the API you are attacking includes administrative requests or even separate admin documentation, then those will be key to see if you are able to successfully request those admin actions as a non-admin user. 
