// //overrides metamask v0.2 for our 1.0 version.  
//1.0 lets us use async and await instead of promises


// import Torus from "@toruslabs/torus-embed";
import Web3 from 'web3';
//overrides metamask v0.2 for our v 1.0
// const web3 = new Web3(window.web3.currentProvider);

// enableTorus =  

const web3obj = {
    web3: new Web3(window.web3.currentProvider),
    // initialize: async () => {
    //     try {
    //       const torus = new Torus();
    //       await torus.init();
    //       await torus.ethereum.enable();
    //       // const 
    //       web3obj.web3 = new Web3(torus.provider);
    //       web3obj.web3.eth.getAccounts().then(accounts => {
    //         web3obj.web3.eth.getBalance(accounts[0]).then(console.log)
    //       });
    //     } catch (error) {
    //       console.error(error);
    //     }
    //   }
  }

export default web3obj;