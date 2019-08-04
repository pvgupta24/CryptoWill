//https://github.com/facebook/create-react-app/blob/master/packages/react-scripts/template/README.md#adding-a-stylesheet
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
import React from 'react';
import ReactDOM from 'react-dom';
// import '@toruslabs/torus-embed'
import './index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

// import web3obj from './web3'

// const isTorus = sessionStorage.getItem('pageUsingTorus')

// if (isTorus === 'true') {
//   import('@toruslabs/torus-embed').then(() => {
//     console.log('rehydrated Torus')
//     web3obj.initialize()
//     // set store accounts from here ideally
//   })
// }

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();
