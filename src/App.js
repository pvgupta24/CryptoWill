import {Table, Grid, Button, Form } from 'react-bootstrap';

import React, { Component } from 'react';
//import logo from './logo.svg';
import './App.css';
import web3obj from './web3';
import ipfs from './ipfs';
import storehash from './storehash';

class App extends Component {
 
    state = {
      ipfsHash:null,
      buffer:'',
      ethAddress:'',
      blockNumber:'',
      transactionHash:'',
      gasUsed:'',
      txReceipt: '',
      textToSave: 'Enter Text here',
      account: '',
      balance: '' ,
      bob_pub_key: '',
      alice_is_alive: true  
    };

    


    // componentDidMount() {
    //   // if not using store
    //   setTimeout(() => {
    //     if (window.web3) {
    //       web3obj.web3.eth.getAccounts().then(accounts => {
    //         this.setState({ account: accounts[0] })
    //         return null
    //       })
    //     }
    //   }, 1000)
    //   return null
    // }
  
    // componentDidUpdate(prevProps, prevState) {
    //   if (this.state.account && this.state.account !== '' && prevState.account !== this.state.account) {
    //     web3obj.web3.eth.getBalance(this.state.account).then(balance => {
    //       this.setState({ balance: web3obj.web3.utils.fromWei(balance) })
    //       return null
    //     })
    //   }
    //   return null
    // }
  
    // enableTorus = () => {
    //     web3obj.initialize()
    // }
  
    // importTorus = () => {
    //   import('@toruslabs/torus-embed').then(this.enableTorus)
    // }


  //   onClick = async () => {

  //     try{
  //         this.setState({blockNumber:"waiting.."});
  //         this.setState({gasUsed:"waiting..."});

  //         // get Transaction Receipt in console on click
  //         // See: https://web3js.readthedocs.io/en/1.0/web3-eth.html#gettransactionreceipt
  //         await web3obj.eth.getTransactionReceipt(this.state.transactionHash, (err, txReceipt)=>{
  //           console.log(err,txReceipt);
  //           this.setState({txReceipt});
  //         }); //await for getTransactionReceipt

  //         await this.setState({blockNumber: this.state.txReceipt.blockNumber});
  //         await this.setState({gasUsed: this.state.txReceipt.gasUsed});    

  //         fetch('http://127.0.0.1:8000/', {
  //           // crossDomain:true,
  //           mode: 'no-cors',
  //           method: 'POST',
  //           headers: {'Content-Type':'application/json'},
  //           body: JSON.stringify({
  //             hash: this.state.txReceipt,
  //           })
  //         })

  //       } //try
  //     catch(error){
  //         console.log(error);
  //     } //catch
  // } //onClick



  captureFile =(event) => {
    event.stopPropagation()
    event.preventDefault()
    const file = event.target.files[0]
    let reader = new window.FileReader()
    reader.readAsArrayBuffer(file)
    reader.onloadend = () => this.convertToBuffer(reader)    
  };

convertToBuffer = async(reader) => {
  //file is converted to a buffer to prepare for uploading to IPFS
    const buffer = await Buffer.from(reader.result);
  //set this buffer -using es6 syntax
    this.setState({buffer});
};

onClick = async () => {

try{
    this.setState({blockNumber:"waiting.."});
    this.setState({gasUsed:"waiting..."});

    // get Transaction Receipt in console on click
    // See: https://web3js.readthedocs.io/en/1.0/web3-eth.html#gettransactionreceipt
    await web3obj.web3.eth.getTransactionReceipt(this.state.transactionHash, (err, txReceipt)=>{
      console.log(err,txReceipt);
      this.setState({txReceipt});
    }); //await for getTransactionReceipt

    await this.setState({blockNumber: this.state.txReceipt.blockNumber});
    await this.setState({gasUsed: this.state.txReceipt.gasUsed});    

    fetch('http://127.0.0.1:8000/', {
      // crossDomain:true,
      mode: 'no-cors',
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({  
        type: "upload",
        hash: this.state.txReceipt.transactionHash,
        block_hash: this.state.txReceipt.blockHash,
        alice_pub_key: this.state.account,
        bob_pub_key: this.state.bob_pub_key
      })
    })
  } //try
  catch(error){
      console.log(error);
    } //catch
} //onClick

  onSubmit = async (event) => {
    event.preventDefault();

    //bring in user's metamask account address
    const accounts = await web3obj.web3.eth.getAccounts();
  
    console.log('Sending from Metamask account: ' + accounts[0]);

    //obtain contract address from storehash.js
    const ethAddress= await storehash.options.address;
    this.setState({ethAddress});
    this.setState({account: accounts[0]});

  //save document to IPFS,return its hash#, and set hash# to state
  //https://github.com/ipfs/interface-ipfs-core/blob/master/SPEC/FILES.md#add 
    await ipfs.add(this.state.buffer, (err, ipfsHash) => {
      console.log(err,ipfsHash);
      //setState by setting ipfsHash to ipfsHash[0].hash 
      this.setState({ ipfsHash:ipfsHash[0].hash });

      // call Ethereum contract method "sendHash" and .send IPFS hash to etheruem contract 
      //return the transaction hash from the ethereum contract
      //see, this https://web3js.readthedocs.io/en/1.0/web3-eth-contract.html#methods-mymethod-send
      
      storehash.methods.sendHash(this.state.ipfsHash).send({
        from: accounts[0] 
      }, (error, transactionHash) => {
        console.log(transactionHash);
        this.setState({transactionHash});
      }); //storehash 
    }) //await ipfs.add 
  }; //onSubmit 


  handleChange(e) {
    this.setState({ bob_pub_key: e.target.value });
  }

  sendHeartBeat = (event) => {
    console.log("Sending HeartBeat")
  }

  killAlice = (event) => {
    console.log("Killing Alice");
    this.setState({alice_is_alive: false});

    fetch('http://127.0.0.1:8000/', {
      // crossDomain:true,
      mode: 'no-cors',
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({
        type: "kill_alice",
        hash: this.state.txReceipt.transactionHash,
        block_hash: this.state.txReceipt.blockHash,
        alice_pub_key: this.state.account,
        bob_pub_key: this.state.bob_pub_key
      })
    })
  }

  getKey = (event) => {
    if(this.state.alice_is_alive){
      console.log("Alice is still alive. Bob does not have access");
    }
    else{
      fetch('http://127.0.0.1:8000/', {
      // crossDomain:true,
      mode: 'no-cors',
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({  
        type: "get_key  ",
        hash: this.state.txReceipt.transactionHash,
        block_hash: this.state.txReceipt.blockHash,
        alice_pub_key: this.state.account,
        bob_pub_key: this.state.bob_pub_key
      })
    })
    }
  }

    render() {
      
      return (
        <div className="App">
          <header className="App-header">
            <h1> Nu-Will</h1>
          </header>
          
          <hr />
          
        <h2>Alice </h2>

        <Grid>
          <h3> Choose file to send to IPFS </h3>
          <Form onSubmit={this.onSubmit}>
            <input 
              type = "file"
              onChange = {this.captureFile}
            />
             <Button 
             bsStyle="primary" 
             type="submit"> 
             Encrypt and Upload 
             </Button>
          </Form>
          <Form>
            <input type="text" placeholder="Enter Bob public key" 
                value={this.state.bob_pub_key} 
                onChange={ this.handleChange.bind(this) } 
            />
            <Button bsStyle="success" onClick = {this.onClick}>Create Policy</Button>
          </Form>

          <Button bsStyle="danger" onClick={this.sendHeartBeat}>Send Alice Heartbeat</Button>
          <Button bsStyle="danger" onClick={this.killAlice}>Kill Alice</Button>

              <Table bordered responsive>
                <thead>
                  <tr>
                    <th>Tx Receipt Category</th>
                    <th>Values</th>
                  </tr>
                </thead>
               
                <tbody>
                  <tr>
                    <td>IPFS Hash # stored on Eth Contract</td>
                    <td>{this.state.ipfsHash}</td>
                  </tr>
                  <tr>
                    <td>Ethereum Contract Address</td>
                    <td>{this.state.ethAddress}</td>
                  </tr>

                  <tr>
                    <td>Tx Hash # </td>
                    <td>{this.state.transactionHash}</td>
                  </tr>

                  <tr>
                    <td>Block Number # </td>
                    <td>{this.state.blockNumber}</td>
                  </tr>

                  <tr>
                    <td>Gas Used</td>
                    <td>{this.state.gasUsed}</td>
                  </tr>                
                </tbody>
            </Table>
        </Grid>

        <hr/>

        <h2>Bob</h2>
          <Button bsStyle="info" onClick={this.getKey}>Get Alice Key</Button>

     </div>
      );
    } //render
}

export default App;
