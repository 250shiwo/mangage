const { defineConfig } = require('@vue/cli-service')
let proxyObj = {};

module.exports = defineConfig({
  transpileDependencies: true
})


proxyObj['/api'] = {
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
    proxy: proxyObj,
    historyApiFallback: {
      rewrites: [
        // 将所有路径重定向到 index.html（关键）
        { from: /^\/.*$/, to: '/index.html' }
      ]
    }
  }
}


