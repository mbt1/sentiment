export PATH=$PATH:$(dirname $(which npm))
npm install
npm install -g react react-dom 
npm install -g webpack webpack-dev-server webpack-cli
npm install -g @babel/core @babel/preset-env @babel/preset-react babel-webpack-plugin babel-loader
npm install -g express
npm update webpack
npm install -g copy-webpack-plugin