// webpack.config.js
const path = require('path');
const webpack = require('webpack');

module.exports = {
  entry: './static/main.js',
  output: {
    path: path.resolve(__dirname, './static'),
    filename: 'app.js'
  },
  module: {
    loaders: [{
      test: /\.js$/,
      exclude: /node_modules/,
      loader: 'babel-loader'
    }]
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin({
      compress: { warnings: false, },
      output: { comments: false, },
    }),
  ]
};
