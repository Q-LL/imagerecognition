<template>
  <div>
    <h1>开始使用</h1>
  </div>
  <div>
    <div class="upload">
      <el-upload list-type="text" action='' accept=".jpg, .png" :limit="1" :auto-upload="false" :file-list="fileList"
        :on-change="getFile" :on-preview="handlePictureCardPreview" :on-remove="handleUploadRemove">
        <el-button size="small" type="primary">选择图片上传</el-button>
        <br>
        <template #tip>
          <div slot="tip" class="el-upload__tip">只能上传一张jpg/png文件</div>
        </template>
      </el-upload>
    </div>

    <!-- 半径滑块 -->
    <div class="circle">
      <el-slider v-model="circle" :min="5" :max="100" show-input />
    </div>

    <div class="img">
      <!-- 展示图片 -->
      <el-image style="" :src="showimg(proofImage)" :v-if="Visible" fit="fit" loading="lazy"
        @click="handleImageClick($event)">
        <template #error>
          <div class="image-slot">
            <el-icon><icon-picture /></el-icon>
          </div>
        </template>
      </el-image>
    </div>

    <!-- 展示标注数据 -->
    <div class="sign">
      <el-table :data="points" v-if="Visible" style="width: 100%">
        <el-table-column prop="id" label="id" width="50" />
        <el-table-column prop="x" label="x轴坐标" width="180" />
        <el-table-column prop="y" label="y轴坐标" width="180" />
        <el-table-column prop="cir" label="半径" width="180" />
        <el-table-column label="操作"><template #default="scope"><el-button size="small" type="danger"
              :disabled="isDeleteDisabled(scope.row.id)" @click="delpoint(scope.row.id)">删除</el-button></template>
        </el-table-column>
        <el-table-column label="xValue"><template #default="scope"><el-input v-model="xValue[scope.row.id-1]" placeholder="请输入xValue"></el-input></template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 用户输入数据 -->
    <div class="input">
      Function:<el-input v-model="functions" class="custom-input" placeholder="请输入 Function"></el-input>
    </div>

    <!-- 开始处理 -->
    <el-button @click="makedata()">开始处理</el-button>
  </div>

  <!-- test show -->
  <div>
    {{ message }}
  </div>
</template>

<script>
import { connectWebSocket } from '@/axios';
import cv from '@/opencv';

export default {
  data() {
    return {
      dialogVisible: false,
      Visible: false,
      dialogImageUrl: null,
      proofImage: null,
      pointsid: 0,//点的个数
      points: [], // 存储标点的坐标
      circle: 5,//滑块半径
      // 存储图片宽高
      localx: null,
      localy: null,

      //用户输入数据
      functions: null,
      xValue: [],

      //axios
      pendingData: null, //待发送的数据
      message: 'Connecting...',
      socket: null,
    }
  },

  mounted() {

  },

  methods: {
    getFile(file, fileList) {
      this.getBase64(file.raw).then(res => {
        const params = res.split(',')
        //console.log(params, 'params')
        if (params.length > 0) {
          this.proofImage = params;
          const image = new Image();
          image.src = res;
          // 当图片加载完成后执行回调函数
          image.onload = () => {
            this.localx = image.width;
            this.localy = image.height;
            //console.log(this.localx, this.localy);
          }
        }
        this.Visible = true;
      })
    },


    // 获取图片转base64
    getBase64(file) {
      return new Promise(function (resolve, reject) {
        const reader = new FileReader()
        let imgResult = ''
        reader.readAsDataURL(file)
        reader.onload = function () {
          imgResult = reader.result
        }
        reader.onerror = function (error) {
          reject(error)
        }
        reader.onloadend = function () {
          resolve(imgResult)
        }
      })
    },
    handleUploadRemove(file, fileList) {
      this.proofImage = '';
      this.pointsid = 0;
      this.points = [];
      this.localx = null;
      this.localy = null;
      this.Visible = false;
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },

    //显示图片
    showimg(img) {
      let url;
      url = img;
      return url;
    },

    // 处理图片点击
    handleImageClick(event) {
      const imgWidth = event.target.width;
      const imgHeight = event.target.height;
      const x = Math.round((event.offsetX / imgWidth) * this.localx);
      const y = Math.round((event.offsetY / imgHeight) * this.localy);
      // 添加到points数组中
      this.pointsid = this.pointsid + 1;
      const id = this.pointsid;
      const cir = this.circle;
      this.points.push({ id, x, y, cir })
    },
    //删除某一标点
    delpoint(id) {
      const index = this.points.findIndex(point => point.id === id);
      this.points.splice(index, 1);
      this.pointsid = this.pointsid - 1;
      //console.log(this.pointsradios);
    },
    isDeleteDisabled(id) {//判断按钮
      const maxId = Math.max(...this.points.map(point => point.id));
      return id !== maxId;
    },

    //处理数据
    makedata() {
      // 创建一个空对象
      const dataToSend = {};
      dataToSend.image = this.proofImage[0] + ',' + this.proofImage[1];
      dataToSend.circles = this.points.map(point => `${point.x},${point.y},${this.circle}`).join("\n");
      dataToSend.function = this.functions;
      dataToSend.xValue = this.xValue.join("\n");
      const jsonToSend = JSON.stringify(dataToSend);
      this.pendingData = jsonToSend;
      console.log(this.pendingData);
      //发送数据
      this.handleProcess(this.pendingData);
    },
    //按按钮发送数据
    handleProcess(data) {
      // 定义处理方法，调用connectWebSocket函数，返回一个promise对象
      // 把你的图片和标注数据作为参数传给connectWebSocket函数
      connectWebSocket(data)
        .then(socket => {
          this.socket = socket
          this.message = 'Connected'
          this.socket.onmessage = event => {
            this.message = event.data
          }
          this.socket.onclose = () => {
            this.message = 'Disconnected'
          }
        })
        .catch(error => {
          // 处理错误，这里只是简单地显示在页面上
          this.message = error.message
        })
    }

  },
}
</script>

<style scoped>
.circle {
  margin: auto;
  margin-bottom: 10px;
  width: 80%;
}

.custom-input {
  padding-left: 10px;
  padding-bottom: 10px;
  width: 180px;
}
</style>