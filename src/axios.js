import axios from 'axios';

const instance = axios.create({
  baseURL: 'https://api.example.com', // 根据你的实际情况修改 baseURL
  timeout: 5000, // 设置请求超时时间
  headers: {
    'Content-Type': 'application/json', // 设置请求头
  },
});

export default instance;