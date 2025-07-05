const { defineConfig } = require('@vue/cli-service')
let proxyObj = {};

module.exports = defineConfig({
  transpileDependencies: true
})


proxyObj['/'] = {
    ws: false,
    target: 'http://localhost:5000',
    changeOrigin: true,
    pathRewrite: {
        '^/': ''
    },
    logLevel: 'debug'
}

module.exports = {
  devServer: {
    proxy: proxyObj
  }
}


