const {defineConfig} = require('@vue/cli-service')

const AutoImport = require('unplugin-auto-import/webpack')
const Components = require('unplugin-vue-components/webpack')
const {ElementPlusResolver} = require('unplugin-vue-components/resolvers')

module.exports = defineConfig({
    configureWebpack: (config) => {
        if (!config.plugins) {
            config.plugins = []
        }
        config.plugins.push(
            AutoImport({
                resolvers: [ElementPlusResolver()]
            })
        )
        config.plugins.push(
            Components({
                resolvers: [ElementPlusResolver()]
            })
        )
    }
})