var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: './static/js/index.js',
  output: {
      path: path.resolve('./static/webpack_bundles/'),
      filename: "[name]-[hash].js"
  },
  mode:'development',
  node: {
    fs: "empty"
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'})
  ]
}