var path = require("path")
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  context: __dirname,

  entry: './frontend/src/index', // entry point of our app. assets/js/index.js should require other js modules and dependencies it needs

  output: {
      path: path.resolve('./frontend/bundles/'),
      filename: "[name]-[fullhash].js",
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
  ],

  module: {
      rules: [
          {
              use: [
                  'babel-loader',
              ]
          }
      ],
    // use: [
    //   { test: /\.jsx?$/, exclude: /node_modules/, loader: 'babel-loader'}, // to transform JSX into JS
    // ],
  },

  resolve: {
    // modulesDirectories: ['node_modules', 'bower_components'],
    extensions: ['', '.js', '.jsx']
  },
}

// var path = require('path');
// var webpack = require('webpack');
// var BundleTracker = require('webpack-bundle-tracker');

// module.exports = {
//   context: __dirname,
//   entry: './frontend/src/index',
//   output: {
//       path: path.resolve('./frontend/bundles/'),
//       filename: "[name]-[hash].js"
//   },

//   plugins: [
//     new BundleTracker({filename: './webpack-stats.json'})
//   ]
// }