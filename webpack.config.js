const PATH = require('path');
const webpack = require('webpack');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const CompressionWebpackPlugin = require('compression-webpack-plugin');

const SRC_PATH = PATH.resolve(__dirname, './src/static/js');
const DIST_PATH = PATH.resolve(__dirname, './src/static/js/dist');

module.exports = {
    entry: {
        main: SRC_PATH + "/main.js",
        components: SRC_PATH + "/components.js",
    },
    output: {
        path: DIST_PATH,
        filename: '[name].bundle.js',
    },
    resolve: {
        extensions: ['', '.js', '.jsx']
    },
    module: {
        rules: [
            {
                test: /\.js|jsx$/,
                exclude: /(node_modules)/,  //对这个不做处理
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['env', 'react']    //在react环境下,也可以进行打包
                    }
                }
            }
        ]
    },
    optimization: {
        splitChunks: {
            chunks: 'all',
            minSize: 30000,
            minRemainingSize: 0,
            minChunks: 1,
            maxAsyncRequests: 30,
            maxInitialRequests: 30,
            enforceSizeThreshold: 50000,
            cacheGroups: {
                defaultVendors: {
                    name: "vendor",
                    test: /[\\/]node_modules[\\/]/,
                    priority: -10,
                    reuseExistingChunk: true,
                },
                default: {
                    minChunks: 2,
                    priority: -20,
                    reuseExistingChunk: true,
                },
            }
        },
    },
    // // 生产环境优化
    // devtool: 'source-map',
    // plugins: [
    //     // 生产环境优化
    //     new UglifyJSPlugin({
    //         sourceMap: true
    //     }),
    //     // 生产环境压缩
    //     new CompressionWebpackPlugin({
    //         test: /\.js$|\.css$/,
    //         threshold: 10240,
    //     }),
    // ]
}