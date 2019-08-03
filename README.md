# CryptoWill
Decentralised application made during ETHIndia 2.0

## Setup
* Install truffle suite: `npm install -g truffle`
* Install Metamask browser extension
* Install Ganache-Cli: `npm install -g ganache-cli`

## Running the application
* Start the local blockchain for testing: `ganache-cli 7545`
* Change the network to Localhost in Metamask and add accounts if needed
* Compile the solidity contracts: `truffle compile`
* Deploy the compiled contracts on the blockchain (as given in the truffle config file):
 `truffle migrate --network development`
* Start the dev server: `npm run dev`

## References
> [Truffle basics](https://www.trufflesuite.com/boxes/pet-shop)


# Running Django Backend App

`cd backend`

* Install dependencies

> `pip install -r requirements.txt`

* Create local settings by copying example-production.py

> `cp example-production.py local.py`

* Run server

> `python manage.py runserver`
