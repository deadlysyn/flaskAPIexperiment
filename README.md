# Coding Exercise

The goal is to build a simple "URL lookup service".  I chose to use this
as an opportunity to experiment with Flask!

# Service Description

We have an HTTP proxy that is scanning traffic looking for malware
URLs.  Before allowing HTTP connections to be made, this proxy asks
a service that maintains several databases of malware URLs if
the resource being requested is known to contain malware.

Write a small web service, in the language/framework of your choice,
that responds to GET requests where the caller passes in a URL and
the service responds with some information about that URL. The GET
requests look like this:

GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}

The caller wants to know if it is safe to access that URL or not.

As the implementor you get to choose the response format and
structure. These lookups are blocking users from accessing the URL
until the caller receives a response from your service.

# Setup

For a test environment... let's just use sqlite to immitate the
malware database. Feel free to generate your own malware.csv with some
real-world data vs my dummies.

- git clone this repo
- pyvenv opendns-exercise
- cd opendns-exercise
- source bin/activate
- pip install requirements.txt
- Setup the database (in venv dir)
    - sqlite3 malware.db
    - .mode csv malware
    - .import malware.csv malware
- Run websvc.py
- Connect to localhost:5000
    - /urlinfo/1 will return full list of urls in database
    - /urlinfo/1/{host:port}/{uri} will return reputation of host:port/uri
    - all output should be json

Traffic flow:

1. User initiates request
2. Proxy intercepts request, and forwards to web service
3. Web service looks for URL in malware database
4. Web service provides response to proxy
5. Based on response, proxy can pass or block website

```
   +-------------+
   |    USERS    |
   +-------------+
         |
         | (1)
         |
        \_/
   +-------------+   (5)   +-------------+
   |    PROXY    |---------|   WEBSITE   |
   +-------------+         +-------------+
      |     /-\
  (2) |      |
      |      | (4)
     \_/     |
   +-------------+
   | WEB SERVICE |
   +-------------+
         |
         | (3)
         |
        \_/
   +-------------+
   |  DATABASE   |
   +-------------+
```
