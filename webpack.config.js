const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin")

// check if we are running in production, make sure you use the same env var for both django and webpack
const isDevelopment = (process.env.DEBUG || "false").toLowerCase() == "true";

module.exports =
{
  target: 'web',
  context: path.resolve(),
  mode: isDevelopment ? "development" : "production",
  entry: {
      main: './assets/js/index.js',
  },
  output: {
      path: path.resolve('./static/webpack_bundles/'),
      filename: "[name]-[fullhash].js",
      clean: true,
      publicPath: isDevelopment ? 'http://localhost:9091/' : undefined,
  },
  devServer: {
      port: 9091,
      headers: {
          "Access-Control-Allow-Origin": "*",
      }
  },
  devtool: isDevelopment ? "eval" : "source-map",
  plugins: [
      new BundleTracker({ filename: './webpack-stats.json' }),
      new MiniCssExtractPlugin({
          filename: "[name]-[fullhash].css",
          chunkFilename: "[id]-[fullhash].css",
      }),
  ],
  module: {
      rules: [
        {
          test: /\.js$/,
          include: path.resolve(__dirname, '*'),
          loader: 'babel-loader',
        },
          {
              test: /\.s[ac]ss$/i,
              use: [
                  isDevelopment ? "style-loader" : MiniCssExtractPlugin.loader,
                  {
                      loader: 'css-loader',
                      options: {
                          sourceMap: isDevelopment
                      }
                  },
                  {
                      loader: 'sass-loader',
                      options: {
                          sourceMap: isDevelopment
                      }
                  },
              ],
          },
          {
              test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
              type: 'asset',
              generator: {
                  filename: 'fonts/en/[hash][ext][query]',
              },
          }
      ]
  }
}
