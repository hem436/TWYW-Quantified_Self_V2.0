const {
  defineConfig
} = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: process.env.NODE_ENV === "production" ? "/TWYW/" : "/",
  pwa: {
    name: 'Quantified self',
    iconPaths: {
      favicon32: "./img/icons/favicon-32x32.png",
      favicon16: "./img/icons/favicon-16x16.png",},
      manifestOptions: {
        name: "Quantified self",
        short_name: "Quantified self",
        theme_color: "#4DBA87",
        icons: [{
          src: "./img/icons/android-chrome-192x192.png",
          sizes: "192x192",
          type: "image/png"
        },{
          src: "./img/icons/android-chrome-512x512.png",
          sizes: "512x512",
          type: "image/png"
        }],
        start_url: ".",
        display: "standalone",
        background_color: "#000000"
      }


  }

})
