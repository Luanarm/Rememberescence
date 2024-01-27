import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';



class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
      </div>
    );
  }
}

export default App;




// import React from 'react';
// import NavigationBar from './NavigationBar';

// import './App.css';  // Make sure to import the CSS file

// const Content = () => (
//     <div className="content">
//         <h1>Welcome to our website!</h1>
//         {/* Add more content here */}
//     </div>
// );

// const App = () => {
//     return (
//         <div>
//             <NavigationBar />
//             <Content />
//         </div>
//     );
// };

// export default App;

