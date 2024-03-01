// 导入axios库
import axios from 'axios'

// 创建一个axios实例，设置基本的配置
const instance = axios.create({
  baseURL: 'http://localhost:8000', // 你的后端地址
  timeout: 10000 // 请求超时时间
})

// 定义一个函数，用于建立websocket连接
// 定义一个函数，用于建立websocket连接，并发送数据
function connectWebSocket (data) {
  return new Promise((resolve, reject) => {
    // 直接使用websocket的URL创建一个WebSocket对象
    const socket = new WebSocket('ws://127.0.0.1:8000/standard') // 修改这里
    // 设置websocket的事件监听器
    socket.onopen = () => {
      // 连接成功后，发送数据
      socket.send(data)
      resolve(socket)
    }
    socket.onerror = error => {
      reject(error)
    }
  })
}


// 导出connectWebSocket函数，供其他模块使用
export { connectWebSocket }
