import React from 'react';
import ReactDOM from 'react-dom/client';


const App: React.FC = () => {
  return <h1>Hello, World!</h1>;
};

const root = document.getElementById('root');
if (root === null) {
  throw new Error("Root element not found");
}

const reactRoot = ReactDOM.createRoot(root);
reactRoot.render(<App />);

