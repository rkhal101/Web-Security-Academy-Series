
# Mass Assignment Attacks

## [Mass Assignment: OWASP](https://owasp.org/API-Security/editions/2019/en/0xa6-mass-assignment/)
## [Mass Assignment: PortSwigger](https://portswigger.net/web-security/api-testing#mass-assignment-vulnerabilities)

# Intro 

#### Mass Assignment vulnerabilities are present when an attacker is able to overwrite object properties that they should not be able to. 
A few things need to be in play for this to happen. An API must have requests that accept user input, these requests must be able to alter values not available to the user, 
and the API must be missing security controls that would otherwise prevent the user input from altering data objects. 
The classic example of a mass assignment is when an attacker is able to add parameters to the user registration process that escalate their account from a basic user to an administrator. 
The user registration request may contain key-values for username, email address, and password. 
An attacker could intercept this request and add parameters like "isadmin": "true". 
If the data object has a corresponding value and the API provider does not sanitize the attacker's input then there is a chance that the attacker could register their own admin account.

# Finding Mass Assignment Vulnerabilities

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
