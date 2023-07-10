# Experimental/example project 

## Goal: Async singleton repository

The main idea is to have the asynchronous repository as a singleton (to avoid constructing the repository instance for every request) and the connection will be passed through a ContextVar.

This repo contains that repository and it works well. The unit of work has been given the responsibility to set the DB session in the ContexVar. So every repo used inside unit of work context will be share on db session. 

This is a simple budget assistant app that allows you to add info about receipt and then show a list of your receipts.

## About application

The project uses a clean architecture, so the project structure is almost standard.

No DI here. And entrypoints layer is some experiments with aiohttp.


## How to run

add `.env` file like `.env.example`

run this command to start app in docker:

```commandline
make run
```
