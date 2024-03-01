<template>
  <div style="display: flex; justify-content: center; padding-bottom: 20px; padding-top: 20px;">
    <h1>开始使用</h1>
  </div>
  <div style="padding-bottom: 30px;">
    <!-- 步骤 -->
    <div class="step">
      <el-steps :active="steps" finish-status="success" align-center>
        <el-step title="上传图片" />
        <el-step title="选择处理方法" />
        <el-step title="标注图片" />
        <el-step title="开始处理" />
      </el-steps>
    </div>

    <div class="upload" v-if="steps == 0" style="text-align: center;">
      <el-upload list-type="text" action='' accept=".jpg, .png" :limit="1" :auto-upload="false" :on-change="getFile"
        :on-preview="handlePictureCardPreview" :on-remove="handleUploadRemove">
        <el-button type="primary">选择图片上传</el-button>
        <br>
        <template #tip>
          <div slot="tip" class="el-upload__tip">只能上传一张jpg/png文件</div>
        </template>
      </el-upload>
      <img :src="showimg(proofImage)" class="image-container" v-if="Visible" />
    </div>

    <!-- 选择方法 -->
    <div class="card" v-if="steps == 1" style="width: 80%; margin: auto; padding: auto;">
      <div>
        <el-card shadow="hover" style="margin-top: 20px; margin-bottom: 20px;" @click="choosemethod(1)"> 处理方式1 (默认) </el-card>
      </div>
      <div>
        <el-card shadow="hover" @click="choosemethod(2)"> 处理方式2 </el-card>
      </div>
    </div>

    <!-- 半径滑块 -->
    <div class="circle" v-if="steps == 2">
      <div class="silder"><el-slider v-model="circle" :min="5" :max="100" show-input /></div>
      <div class="circle-preview"
        :style="{ width: (2 * circle * this.scale) + 'px', height: (2 * circle * this.scale) + 'px' }"></div>
    </div>

    <!-- 展示图片 -->
    <div class="image-container" v-if="steps == 2">
      <img :src="showimg(proofImage)" v-if="Visible" @click="handleImageClick($event)" />
      <div v-for="(point, index) in scaledPoints" :key="index" class="point"
        :style="{ left: point.x - (point.cir * this.scale) + 'px', top: point.y - (point.cir * this.scale) + 'px', width: (2 * point.cir * this.scale) + 'px', height: (2 * point.cir * this.scale) + 'px' }">
      </div>
    </div>

    <!-- 展示标注数据 -->
    <div class="sign" v-if="steps == 2">
      <el-table :data="points" v-if="Visible" style="width: 100%">
        <el-table-column prop="id" label="id" width="50" />
        <el-table-column prop="x" label="x轴坐标" width="180" />
        <el-table-column prop="y" label="y轴坐标" width="180" />
        <el-table-column prop="cir" label="半径" width="180" />
        <el-table-column label="操作"><template #default="scope"><el-button size="small" type="danger"
              :disabled="isDeleteDisabled(scope.row.id)" @click="delpoint(scope.row.id)">删除</el-button></template>
        </el-table-column>
        <el-table-column label="xValue"><template #default="scope"><el-input v-model="xValue[scope.row.id - 1]"
              placeholder="请输入xValue"></el-input></template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 用户输入数据 -->
    <div class="input" v-if="steps == 2" style="text-align: center; padding-top: 20px; padding-bottom: 20px;">
      notAutoFunc <el-checkbox v-model="notAutoFunc"></el-checkbox>
      <row v-if="!notAutoFunc">&nbsp;&nbsp;&nbsp;Function:<el-input class="custom-input"  v-model="functions" placeholder="请输入 Function"></el-input></row>
      &nbsp;&nbsp;&nbsp;Goal:<el-input class="custom-input" v-model="Goal" placeholder="请输入 Goal(选填)"></el-input>
      &nbsp;&nbsp;&nbsp;iteration:<el-input class="custom-input" v-model="iteration" placeholder="请输入 iteration(选填)"></el-input>
    </div>

    <!-- test show -->
    <div v-if="steps == 4">
      {{ message }}
      <br>
      {{ resultt }}
    </div>

    <!-- 开始处理 -->
    <div class="button" style="text-align: center; position: fixed; margin-top: 10px; bottom: 10px; width: 100%; z-index:10">
      <el-button @click="laststep()" :disabled="steps <= 0" type="warning">上一步</el-button>
      <el-button @click="nextstep()" v-if="steps < 3" :disabled="!Visible" type="primary">下一步</el-button>
      <!-- <el-button @click="makedata()" v-if="steps==3" >开始处理</el-button> -->
      <el-button @click="makedata()" v-if="steps == 3 || steps == 4" :loading="loading" :disabled="steps == 4 || loading "
        :type="buttontype">{{ buttonText }}</el-button>
    </div>
  </div>
</template>

<script>
import { connectWebSocket } from '@/axios';

export default {
  data() {
    return {
      dialogVisible: false,
      Visible: false,
      dialogImageUrl: null,
  
      // 存储图片宽高
      localx: null,
      localy: null,

      scale: 1, // 图片缩放比例，默认为1，即不缩放
      scaledPoints: [], // 保存根据缩放比例调整后的标点位置

      //传出参数
      proofImage: null,
      pointsid: 0,//点的个数
      points: [], // 存储标点的坐标
      circle: 5,//滑块半径
      functions: 'R/G',
      xValue: [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
      Goal:'',
      iteration:'',
      methord:false,
      notAutoFunc:false,


      //axios
      pendingData: null, //待发送的数据
      message: null, //数据
      socket: null,
      statuss: '未连接',

      //结果数据
      resultt: null,

      steps: 0,//步骤条

      //处理按钮
      buttontype: 'primary',
      loading: false,
      buttonText: '开始处理',
    }
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
      this.scaledPoints = [];
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
      const img = event.target;// 获取图片元素的引用
      const displayWidth = img.getBoundingClientRect().width;// 获取图片的显示宽度
      //console.log(displayWidth);
      this.scale = displayWidth / this.localx;
      //console.log(this.scale);
      const x = Math.round((event.offsetX / imgWidth) * this.localx);
      const y = Math.round((event.offsetY / imgHeight) * this.localy);
      // 添加到points数组中
      this.pointsid = this.pointsid + 1;
      const id = this.pointsid;
      const cir = this.circle;
      this.points.push({ id, x, y, cir });
      const scaledX = Math.round(x * this.scale);
      const scaledY = Math.round(y * this.scale);
      // 将调整后的标点位置保存到 scaledPoints 数组中
      this.scaledPoints.push({ id, x: scaledX, y: scaledY, cir })
      //console.log(this.scaledPoints);
    },
    //删除某一标点
    delpoint(id) {
      const index = this.points.findIndex(point => point.id === id);
      this.points.splice(index, 1);
      this.scaledPoints.splice(index, 1);
      this.pointsid = this.pointsid - 1;
      //console.log(this.pointsradios);
    },
    isDeleteDisabled(id) {//判断按钮
      const maxId = Math.max(...this.points.map(point => point.id));
      return id !== maxId;
    },

    // 选择方法1，2
    choosemethod(num){
      if(num == 1){
        this.methord = false;
      }
      else if (num == 2){
        this.methord = true;
      }
      else{
        // 抛出错误弹窗
      }
      this.steps = this.steps + 1;
      console.log(this.methord);
    },

    //处理数据
    makedata() {
      // 创建一个空对象
      const dataToSend = {};
      dataToSend.image = this.proofImage[0] + ',' + this.proofImage[1];
      dataToSend.circles = this.points.map(point => `${point.x},${point.y},${this.circle}`).join("\n");
      dataToSend.function = this.functions;
      dataToSend.xValue = this.xValue.join("\n");
      dataToSend.Goal = this.Goal;
      dataToSend.methord = this.methord;
      dataToSend.notAutoFunc = this.notAutoFunc;
      dataToSend.iteration = this.iteration;
      const jsonToSend = JSON.stringify(dataToSend);
      this.pendingData = jsonToSend;
      console.log(dataToSend);
      //发送数据
      this.handleProcess(this.pendingData);
    },
    //按按钮发送数据
    handleProcess(data) {
      connectWebSocket(data)
        .then(socket => {
          this.socket = socket;
          //按钮
          this.loading = true;
          this.buttonText = '正在处理';
          this.buttontype = 'warning';

          this.socket.onmessage = event => {
            this.message = JSON.parse(event.data);
            this.message = this.message.result;
            console.log(this.message);
            this.resultt = "y=" + this.message[0].toExponential(3) + "x+" + this.message[1].toFixed(3) + "R2=" + this.message[2].toFixed(3);
          }
          this.socket.onclose = () => {
            this.loading = false;
            this.buttontype = 'success';
            this.buttonText = '处理完成';
            this.steps = 4;
          }
        })
        .catch(error => {
          // 处理错误，这里只是简单地显示在页面上
          this.statuss = error.message;
        })
    },

    //步骤
    nextstep() {
      this.steps = this.steps + 1;
    },
    laststep() {
      if(this.steps == 4){
        this.steps = this.steps -2;
      }
      else{this.steps = this.steps - 1;}
    }

  },
}
</script>

<style scoped>
.circle {
  display: flex;
  align-items: center;
  margin: auto;
  width: 80%;
}

.circle .silder {
  padding-top: 15px;
  padding-bottom: 15px;
  width: 80%;
}

.circle .circle-preview {
  margin-left: 20px;
  margin-top: 10px;
  width: 30px;
  height: 30px;
  border: 1px solid rgb(215, 26, 26);
  border-radius: 50%;
}

.custom-input {
  padding-left: 10px;
  padding-bottom: 10px;
  width: 180px;
}

.image-container {
  position: relative;
}

.point {
  position: absolute;
  width: 10px;
  height: 10px;
  background-color: red;
  /* 可以根据需要修改标点的样式 */
  border-radius: 50%;
}

.step {
  align-items: center;
  width: 98vw;
  padding-bottom: 40px;
}
</style>

<style>
img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style>