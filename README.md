# Prudget

[![Build Status](https://travis-ci.org/thyagostall/prudget.svg?branch=master)](https://travis-ci.org/thyagostall/prudget)
[![CircleCI](https://circleci.com/gh/thyagostall/prudget.svg?style=svg)](https://circleci.com/gh/thyagostall/prudget)

Simple way for tracking every penny. Prudget relies on abstracting all money from your accounts into what is called **buckets**, in order to remove the complexity of managing your money, checking and savings account, credit card, and others.

Buckets are virtual accounts, similar to envelopes on the [Envelope Budgeting System](https://www.moneycrashers.com/envelope-budgeting-system/). Also, Prudget's goal is to make you understand what every penny you have must do.

## Setup

Run `openssl req -x509 -out ./nginx/certs/prudget_local.crt -keyout ./nginx/certs/prudget_local.key -newkey rsa:2048 -nodes -sha256 -subj '/CN=localhost' -extensions EXT -config <(printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")` to create self signed certificates in order the run Prudget locally over HTTPS.

Run `docker-compose up` to create and run all containers needed for this project.

## Contributing

Pull requests must target `master` and must not break any tests and keep the app working.

