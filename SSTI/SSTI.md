
# Server Side Template Injection

## What is SSTI ?
Server-side template injection is when an attacker is able to use native template syntax to inject a malicious payload into a template, which is then executed server-side.

Template engines are designed to generate web pages by combining fixed templates with volatile data. Server-side template injection attacks can occur when user input is concatenated directly into a template, rather than passed in as data. This allows attackers to inject arbitrary template directives in order to manipulate the template engine, often enabling them to take complete control of the server. As the name suggests, server-side template injection payloads are delivered and evaluated server-side, potentially making them much more dangerous than a typical client-side template injection.

<br>

## SSTI impact ?
Server-side template injection vulnerabilities can expose websites to a variety of attacks depending on the template engine in question and how exactly the application uses it. In certain rare circumstances, these vulnerabilities pose no real security risk. However, most of the time, the impact of server-side template injection can be catastrophic.

At the severe end of the scale, an attacker can potentially achieve remote code execution, taking full control of the back-end server and using it to perform other attacks on internal infrastructure.

Even in cases where full remote code execution is not possible, an attacker can often still use server-side template injection as the basis for numerous other attacks, potentially gaining read access to sensitive data and arbitrary files on the server.

<br>

## How SSTI Vulns arise
Server-side template injection vulnerabilities arise when user input is concatenated into templates rather than being passed in as data.

Static templates that simply provide placeholders into which dynamic content is rendered are generally not vulnerable to server-side template injection. The classic example is an email that greets each user by their name, such as the following extract from a Twig template used with PHP

```PHP
$output = $twig->render("Dear {first_name},", array("first_name" => $user.first_name) );
```

**Here's a breakdown of what the code does:**

1. `$output`: This variable is being assigned the result of rendering a template using the Twig templating engine. Twig is a popular templating engine for PHP that allows developers to separate the presentation layer from the business logic.
    
2. `$twig->render()`: This method is called on a Twig instance (`$twig`) to render a template. The first argument is the template string, which may contain placeholders or variables enclosed in curly braces `{}`. In this case, the template string is "Dear {first_name},".
    
3. `array("first_name" => $user.first_name)`: This is an associative array passed as the second argument to the `render()` method. It provides values for the variables used in the template. In this case, it assigns the value of `$user.first_name` to the variable `first_name` in the template.
    

Overall, this code is using Twig to render a template string with dynamic content, where the first name of a user (`$user.first_name`) is inserted into the template.
This is not vulnerable to server-side template injection because the user's first name is merely passed into the template as data.

However, as templates are simply strings, web developers sometimes directly concatenate user input into templates prior to rendering. Let's take a similar example to the one above, but this time, users are able to customize parts of the email before it is sent. For example, they might be able to choose the name that is used:
```PHP
`$output = $twig->render("Dear " . $_GET['name']);`
```

This code snippet seems to be rendering a template using the Twig templating engine in PHP. Let's break it down:

1. `$output`: This variable is being assigned the result of rendering a template using Twig.
    
2. `$twig->render()`: This method is called on a Twig instance (`$twig`) to render a template. The first argument is a string containing the template to be rendered. In this case, the template string appears to be "Dear " followed by a variable placeholder.
    
3. `"Dear " . $_GET['name']`: This concatenates the string "Dear " with the value of the 'name' parameter from the URL query string (accessed via `$_GET['name']`). This suggests that the intention is to greet the user by name in the template.
    

However, this code is incomplete because the template string provided to the `render()` method is missing the necessary Twig syntax for placeholders or variables. In Twig, variables are typically enclosed in double curly braces, like `{{ variable_name }}`. So, the template string should be something like `"Dear {{ name }}"`, assuming 'name' is the variable being passed from the query string.

If you're trying to safely incorporate user input from the query string into your template, it's important to sanitize and validate the input to prevent security vulnerabilities such as Cross-Site Scripting (XSS) attacks.

**Vulerable code**
```PHP
`$output = $twig->render("Dear " . $_GET['name']);`
```

**Exploiting it**
```HTTP
http://vulnerable-website.com/?name={{bad-stuff-here}}
```

In this example, instead of a static value being passed into the template, part of the template itself is being dynamically generated using the `GET` parameter `name`. As template syntax is evaluated server-side, this potentially allows an attacker to place a server-side template injection payload inside the `name` parameter.


## Constructing a server-side template injection attack
![ssti-methodology-diagram](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/ffd0699b-049a-490d-abbc-d38aaee179d6)

<br>

## Detect
As with any vulnerability, the first step towards exploitation is being able to find it. Perhaps the simplest initial approach is to try fuzzing the template by injecting a sequence of special characters commonly used in template expressions, such as `${{<%[%'"}}%\`. If an exception is raised, this indicates that the injected template syntax is potentially being interpreted by the server in some way. This is one sign that a vulnerability to server-side template injection may exist.
#### Plaintext context
Most template languages allow you to freely input content either by using HTML tags directly or by using the template's native syntax, which will be rendered to HTML on the back-end before the HTTP response is sent. For example, in Freemarker, the line `render('Hello ' + username)` would render to something like `Hello Carlos`.

This can sometimes be exploited for [XSS](https://portswigger.net/web-security/cross-site-scripting) and is in fact often mistaken for a simple XSS vulnerability. However, by setting mathematical operations as the value of the parameter, we can test whether this is also a potential entry point for a server-side template injection attack.

For example, consider a template that contains the following vulnerable code:
`render('Hello ' + username)`

During auditing, we might test for server-side template injection by requesting a URL such as:
`http://vulnerable-website.com/?username=${7*7}`

If the resulting output contains `Hello 49`, this shows that the mathematical operation is being evaluated server-side. This is a good proof of concept for a server-side template injection vulnerability.

Note that the specific syntax required to successfully evaluate the mathematical operation will vary depending on which template engine is being used. We'll discuss this in more detail in the [Identify](https://portswigger.net/web-security/server-side-template-injection#identify) step.

## Code context
In other cases, the vulnerability is exposed by user input being placed within a template expression, as we saw earlier with our email example. This may take the form of a user-controllable variable name being placed inside a parameter, such as:
`greeting = getQueryParameter('greeting') engine.render("Hello {{"+greeting+"}}", data)`

On the website, the resulting URL would be something like:

`http://vulnerable-website.com/?greeting=data.username`

This would be rendered in the output to `Hello Carlos`, for example.
This context is easily missed during assessment because it doesn't result in obvious XSS and is almost indistinguishable from a simple hashmap lookup. One method of testing for server-side template injection in this context is to first establish that the parameter doesn't contain a direct XSS vulnerability by injecting arbitrary HTML into the value:
`http://vulnerable-website.com/?greeting=data.username<tag>`

In the absence of XSS, this will usually either result in a blank entry in the output (just `Hello` with no username), encoded tags, or an error message. The next step is to try and break out of the statement using common templating syntax and attempt to inject arbitrary HTML after it:
`http://vulnerable-website.com/?greeting=data.username}}<tag>`

If this again results in an error or blank output, you have either used syntax from the wrong templating language or, if no template-style syntax appears to be valid, server-side template injection is not possible. Alternatively, if the output is rendered correctly, along with the arbitrary HTML, this is a key indication that a server-side template injection vulnerability is present:
`Hello Carlos<tag>`

## Identify
 After identification, the next step is to identify the template engine many of
 Many Template Engines use very similar syntax that is specifically chosen not to clash with HTML
 characters. As a result, it can be relatively simple to create probing payloads
 to test which template engine is being used.
Simply submitting invalid syntax is often enough because the resulting error
message will tell you exactly what the template engine is, and sometimes even
which version. For example, the invalid expression `<%=foobar%>`
```Ruby
<%=foobar%>
```
 triggers the following response from the Ruby-based ERB engine:
```Ruby
(erb):1:in `<main>': undefined local variable or method `foobar' for main:Object (NameError) from /usr/lib/ruby/2.5.0/erb.rb:876:in `eval' from /usr/lib/ruby/2.5.0/erb.rb:876:in `result' from -e:4:in `<main>'
```

-  Use process of elimination based on which syntax appears to be valid or invalid
- Do this by injection arbitrary math ops using syntax from different template engines
- Then observe if they are successfully evaluated.

### SSTI  decision tree
![template-decision-tree](https://github.com/LinuxUser255/Web-Security-Academy-Series/assets/46334926/4858a03f-14a4-48ec-b8b9-806736094769)


## Exploit

### Learn the basic template syntax

Learning the basic syntax is obviously important, along with key functions and handling of variables. Even something as simple as learning how to embed native code blocks in the template can sometimes quickly lead to an exploit. For example, once you know that the Python-based Mako template engine is being used, achieving remote code execution could be as simple as:

```Ruby
# basic template syntax
<% 
		import os 
		x=os.popen('id').read() 
		%> 
		${x}
```
Embedded Ruby (ERB) template, which is often used in web development frameworks like Ruby on Rails to embed Ruby code within HTML templates. Let's break down what it's doing:

1. `<% import os x=os.popen('id').read() %>`: This line starts with `<%`, which is the opening tag for embedded Ruby code in an ERB template. The code inside the tag is executed on the server side when the template is rendered. 

   In this line, it seems to be attempting to execute a system command using Python's `os` module. However, the syntax `import os` is incorrect for Ruby. It resembles Python's syntax for importing modules. In Ruby, you typically require external libraries using `require`. Also, `os.popen('id').read()` is a Python command to execute the `id` command in the shell and read its output. It tries to capture the result of running the `id` command (which usually returns user and group information in Unix-like operating systems).

2. `${x}`: This is likely meant to output the value of the variable `x` within the HTML content. In ERB syntax, `${...}` is used to interpolate Ruby variables or expressions into the HTML output.

Overall, this code snippet appears to be attempting to execute a shell command (`id`) using Python syntax within an ERB template, and then outputting the result in the HTML content. However, it's mixing Python and Ruby syntax incorrectly, and it could potentially lead to security vulnerabilities if executed in a web application due to command injection risks.


In an unsandboxed environment, achieving remote code execution and using it to read, edit, or delete arbitrary files is similarly as simple in many common template engines.

<br>

## Steps to take in to exploit SSTI
- Read about the security implications
In addition to providing the fundamentals of how to create and use templates, the documentation may also provide some sort of "Security" section. The name of this section will vary, but it will usually outline all the potentially dangerous things that people should avoid doing with the template. This can be an invaluable resource, even acting as a kind of cheat sheet for which behaviors you should look for during auditing, as well as how to exploit them.
## [HackTricks-SSTI](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
## [SwissKey Repo-SSTI](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md)

# Documentation for various templates
### [ERB-Ruby Documentation](https://docs.ruby-lang.org/en/2.3.0/ERB.html)
### [Tornado](https://www.tornadoweb.org/en/stable/)
### [Jinja](https://jinja.palletsprojects.com/en/3.1.x/)
### [Mako](https://docs.makotemplates.org/en/latest/)
### [NunJucks](https://mozilla.github.io/nunjucks/getting-started.html)
### [Pug](https://pugjs.org/api/getting-started.html)
### [Razor](https://learn.microsoft.com/en-us/aspnet/core/razor-pages/?view=aspnetcore-8.0&tabs=visual-studio)
### [GOMPLATE](https://docs.gomplate.ca/)

Even if there is no dedicated "Security" section, if a particular built-in object or function can pose a security risk, there is almost always a warning of some kind in the documentation. The warning may not provide much detail, but at the very least it should flag this particular built-in as something to investigate.

For example, in ERB, the documentation reveals that you can list all directories and then read arbitrary files as follows:
```Ruby
<%= Dir.entries('/') %> <%= File.open('/example/arbitrary-file').read %>
```

<br>

## Look for known exploits
Another key aspect of exploiting server-side template injection vulnerabilities is being good at finding additional resources online. Once you are able to identify the template engine being used, you should browse the web for any vulnerabilities that others may have already discovered.

## Explore
At this point, you might have already stumbled across a workable exploit using the documentation. If not, the next step is to explore the environment and try to discover all the objects to which you have access.

Many template engines expose a "self" or "environment" object of some kind, which acts like a namespace containing all objects, methods, and attributes that are supported by the template engine. If such an object exists, you can potentially use it to generate a list of objects that are in scope. For example, in Java-based templating languages, you can sometimes list all variables in the environment using the following injection:
```Java
`${T(java.lang.System).getenv()}`
```
This code is retrieving an environment variable using Java's built-in functionality within a Java Server Page (JSP) or similar environment where Java code can be embedded within the HTML. Let's break it down:

1. `${...}`: This syntax is used in JSP to embed Java code within HTML content.

2. `T(java.lang.System)`: This part of the code is invoking the `T` operator, which is a type operator in Spring Expression Language (SpEL). It's used to specify the type of an object.

3. `.getenv()`: This is calling the `getenv()` method of the `java.lang.System` class. In Java, `getenv()` is a method used to retrieve environment variables.

Overall, this code snippet is retrieving environment variables using Java's `System.getenv()` method within a JSP or a similar Java environment that supports embedded Java code. It's a way to access environment variables dynamically within the application.

<br>

## Developer-supplied objects

It is important to note that websites will contain both built-in objects provided by the template and custom, site-specific objects that have been supplied by the web developer. You should pay particular attention to these non-standard objects because they are especially likely to contain sensitive information or exploitable methods. As these objects can vary between different templates within the same website, be aware that you might need to study an object's behavior in the context of each distinct template before you find a way to exploit it.

<br>

## Create a custom attack
For example, you might find that the template engine executes templates inside a sandbox, which can make exploitation difficult, or even impossible.

After identifying the attack surface, if there is no obvious way to exploit the vulnerability, you should proceed with traditional auditing techniques by reviewing each function for exploitable behavior. By working methodically through this process, you may sometimes be able to construct a complex attack that is even able to exploit more secure targets.

<br>

## Constructing a custom exploit using an object chain

As described above, the first step is to identify objects and methods to which you have access. Some of the objects may immediately jump out as interesting. By combining your own knowledge and the information provided in the documentation, you should be able to put together a shortlist of objects that you want to investigate more thoroughly.

When studying the documentation for objects, pay particular attention to which methods these objects grant access to, as well as which objects they return. By drilling down into the documentation, you can discover combinations of objects and methods that you can chain together. 
**Chaining together the right objects and methods sometimes allows you to gain access to dangerous functionality and sensitive data that initially appears out of reach.**

For example, in the Java-based template engine Velocity, you have access to a `ClassTool` object called `$class`. Studying the documentation reveals that you can chain the `$class.inspect()` method and `$class.type` property to obtain references to arbitrary objects. In the past, this has been exploited to execute shell commands on the target system as follows:
```Java
$class.inspect("java.lang.Runtime").type.getRuntime().exec("bad-stuff-here")
```

The code: mix of pseudo-code attempting to execute malicious code using the Java Runtime class.

Let's break it down:

1. `$class.inspect("java.lang.Runtime")`: This part seems to be using some form of a dynamic language where `$class` is a variable representing a class. It's inspecting the "java.lang.Runtime" class, likely to interact with it.

2. `.type.getRuntime()`: This part is trying to access the `Runtime` object from the inspected class. `Runtime` is a Java class that provides access to the Java Virtual Machine (JVM) runtime environment. 

3. `.exec("bad-stuff-here")`: Finally, the `exec()` method is being called on the `Runtime` object. In legitimate use cases, this method executes the specified command in a separate process. However, in this context, "bad-stuff-here" suggests that the intention is to execute malicious commands or code.

Overall, this code appears to be an attempt to exploit the Java Runtime environment to execute potentially harmful actions. It's important to note that executing arbitrary commands like this can lead to severe security vulnerabilities and should never be done in production or on any system where security is a concern.

<br>

## Constructing a custom exploit using developer-supplied objects

Some template engines run in a secure, locked-down environment by default in order to mitigate the associated risks as much as possible. Although this makes it difficult to exploit such templates for remote code execution, developer-created objects that are exposed to the template can offer a further, less battle-hardened attack surface.

However, while substantial documentation is usually provided for template built-ins, site-specific objects are almost certainly not documented at all. Therefore, working out how to exploit them will require you to investigate the website's behavior manually to identify the attack surface and construct your own custom exploit accordingly.

<br>

