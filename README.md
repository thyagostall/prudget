# Prudget

[![Build Status](https://travis-ci.org/thyagostall/prudget.svg?branch=master)](https://travis-ci.org/thyagostall/prudget)

Simple way for tracking every penny. Prudget relies on abstracting all money from your accounts into what is called **buckets**, in order to remove the complexity of managing your money, checking and savings account, credit card, and others.

Buckets are virtual accounts, similar to envelopes on the [Envelope Budgeting System](https://www.moneycrashers.com/envelope-budgeting-system/). Also, Prudget's goal is to make you understand what every penny you have must do.

## Setup

The current version of Prudget is made using Elixir. To set it up:

  * Install dependencies with `mix deps.get`
  * Create and migrate your database with `mix ecto.create && mix ecto.migrate`
  * Install Node.js dependencies with `cd assets && npm install`
  * Start Phoenix endpoint with `mix phx.server`

Now you can visit [`localhost:4000`](http://localhost:4000) from your browser.

## Contributing

Pull requests must target `master` and must not break any tests and keep the app working.
