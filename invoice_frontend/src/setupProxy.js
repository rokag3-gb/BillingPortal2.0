const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = app => {
  app.use(
    "/api",
    createProxyMiddleware({
      // target: "http://localhost:8000",
      target: "https://dev.bill.cloudmt.co.kr/",
      changeOrigin: true
    })
  )
}