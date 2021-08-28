const PATH = require('path');
const webpack = require('webpack');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
const CompressionWebpackPlugin = require('compression-webpack-plugin');

const SRC_PATH = PATH.resolve(__dirname, './src/static/js');
const DIST_PATH = PATH.resolve(__dirname, './src/static/js/dist');

module.exports = {
    entry: {
        main: {
            import: SRC_PATH + '/main.js',
            dependOn: 'editor',
        },
        component: {
            import: SRC_PATH + '/component.js',
            dependOn: 'editor',
        },
        editor: '@editorjs/editorjs',
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
    // 生成为生产环境优化的文件
    // devtool: 'source-map',
    // plugins: [
    //     new UglifyJSPlugin({
    //         sourceMap: true
    //     }),
    //     new CompressionWebpackPlugin({
    //         test: /\.js$|\.css$/,
    //         threshold: 10240,
    //     }),
    // ]
}