# Prudget

[![Build Status](https://travis-ci.org/thyagostall/prudget.svg?branch=master)](https://travis-ci.org/thyagostall/prudget)

Simple way for tracking every penny. Prudget relies on abstracting all money from your accounts into what is called **buckets**, in order to remove the complexity of managing your money, checking and savings account, credit card, and others.

Buckets are virtual accounts, similar to envelopes on the [Envelope Budgeting System](https://www.moneycrashers.com/envelope-budgeting-system/). Also, Prudget's goal is to make you understand what every penny you have must do.

## Setup

It requires python3 and pip to be installed. To set it up for development, you must:

- Install the dependencies; `pip install -r requirements.txt`
- Create an file called `.env` at the root directory of the project, following the examples on `env.sample`.

## Contributing

Pull requests must target `master` and must not break any tests and keep the app working.
