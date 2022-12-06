const path = require('path');

module.exports = {
    entry: './js/index.js',
    mode: 'development',
    output: {
        path: path.join(__dirname, 'build'),
        publicPath: "/build/",
        filename: 'index.js',
    },
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            }
        ]
    }
}