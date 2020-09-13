# User Microservice
This repository contains boilerplate code for setting up a secure users backend microservice in [Flask](https://flask.palletsprojects.com/en/1.1.x/). It utilizes Json Web Tokens (JWT) to establish permissions for requests to specified backend endpoints. The use of HTTP only cookies prevents XSS attacks and we use CSRF tokens to prevent CSRF attacks.

See [this](https://youtu.be/SLc3cTlypwM) great video on authentication using JWTs for a great overview of its use in a microservice architecture.
