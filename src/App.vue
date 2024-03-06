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
        <el-step title="标注图片及处理" />
        <el-step title="展示数据" />
        <el-step title="样品处理" />
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
        <el-card shadow="hover" style="margin-top: 20px; margin-bottom: 20px;" @click="choosemethod(1)"> 处理方式1 (默认)
        </el-card>
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
      <img ref="image" :src="showimg(proofImage)" v-if="Visible" @click="handleImageClick($event)" />
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
        <el-table-column label="操作">

          <template #default="scope"><el-button size="small" type="danger" :disabled="isDeleteDisabled(scope.row.id)"
              @click="delpoint(scope.row.id)">删除</el-button></template>
        </el-table-column>
        <el-table-column label="xValue">

          <template #default="scope"><el-input v-model="xValue[scope.row.id - 1]"
              placeholder="请输入xValue"></el-input></template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 用户输入数据 -->
    <div class="input" v-if="steps == 2" style="text-align: center; padding-top: 20px; padding-bottom: 20px;">
      <row style="padding-left: 10px; padding-bottom: 10px;">&nbsp;&nbsp;&nbsp;使用自动方程 <el-checkbox
          v-model="notAutoFunc"></el-checkbox></row>
      <row>&nbsp;&nbsp;&nbsp;Function:<el-input class="custom-input" :disabled="notAutoFunc" v-model="functions"
          placeholder="请输入 Function" style="width: 500px;"></el-input></row><br>
      <row v-if="notAutoFunc">&nbsp;&nbsp;&nbsp;请输入计算目标R^2:<el-input class="custom-input" v-model="Goal"
          placeholder="请输入 Goal(选填)"></el-input></row>
      <row v-if="notAutoFunc">&nbsp;&nbsp;&nbsp;请输入最大迭代次数:<el-input class="custom-input" v-model="iteration"
          placeholder="请输入 iteration(选填)"></el-input></row><br>
      <!-- <row v-if="notAutoFunc">&nbsp;&nbsp;&nbsp;<p>当前进度:{{ autoFuncProgress }}</p></row> -->
      <div v-if="notAutoFunc" style="width: 80%; margin: auto; padding-bottom: 10px;">
        <el-progress :percentage="Math.round(autoFuncProgress*100)" />
      </div>
      <div>
        <el-button @click="makedata()" :loading="loading" :disabled="loading || pointsid == 0" :type="buttontype">{{
          buttonText
        }}</el-button>
      </div>
    </div>

    <!-- 图表  -->
    <div class="charts" style="width: 80%; height:60vh; margin: auto; " v-if="steps == 3">
      <!-- <div id="chartpointsmap" style="width:90%;height:60vh;"></div> -->
      <chartpointsmap :ponints="chartsdatapoint" :linexy="chartresult" />
      <p id="lineFunc" style="text-align: center;">直线方程: y = {{ chartresult[0].toExponential(3) }}x{{ chartresult[1] >=
        0 ?
        ' + ' : '' }}{{ Math.abs(chartresult[1]).toFixed(3) }} ,R² = {{ chartresult[2].toFixed(3) }}</p><br>

        <div style="text-align: center;">
          <el-button type="primary" @click="dataDownload()">下载数据</el-button>
        </div>
    </div>

    <!-- 样品处理 -->
    <div class="sample" v-if="steps == 4" style="height: 90vh;">
      <div class="upload" style="text-align: center;">
        <el-upload list-type="text" action='' accept=".jpg, .png" :limit="1" :auto-upload="false" :on-change="getFile2"
          :on-preview="handlePictureCardPreview" :on-remove="handleUploadRemove2">
          <el-button type="primary">选择图片上传</el-button>
          <br>

          <template #tip>
            <div slot="tip" class="el-upload__tip">只能上传一张jpg/png文件</div>
          </template>
        </el-upload>
      </div>
      <div class="circle" v-if="steps == 4">
        <div class="silder"><el-slider v-model="circle" :min="5" :max="100" show-input /></div>
        <div class="circle-preview"
          :style="{ width: (2 * circle * this.scale2) + 'px', height: (2 * circle * this.scale2) + 'px' }"></div>
      </div>
      <div class="image-container">
        <img ref="image2" :src="proofImage2" v-if="Visible2" @click="handleImageClick2($event)" />
        <div v-for="(point, index) in scaledPoints2" :key="index" class="point"
          :style="{ left: point.x - (point.cir * this.scale2) + 'px', top: point.y - (point.cir * this.scale2) + 'px', width: (2 * point.cir * this.scale2) + 'px', height: (2 * point.cir * this.scale2) + 'px' }">
        </div>
      </div>
      <div class="sign">
        <el-table :data="points2" v-if="Visible2" style="width: 100%">
          <el-table-column prop="id" label="id" width="50" />
          <el-table-column prop="x" label="x轴坐标" width="180" />
          <el-table-column prop="y" label="y轴坐标" width="180" />
          <el-table-column prop="cir" label="半径" width="180" />
          <el-table-column label="操作">

            <template #default="scope"><el-button size="small" type="danger"
                @click="delpoint2(scope.row.id)">删除</el-button></template>
          </el-table-column>
          <el-table-column label="结果" v-if="!(sampleresult == null)">{{ sampleresult[0].toFixed(3) + '±' +
            sampleresult[1].toFixed(3)
          }}</el-table-column>
        </el-table>
      </div>
      <div style="text-align: center; padding-top: 15px;">
        <el-button @click="makedata2()" :loading="loading" :disabled="loading || !Visible2 || pointsid2 == 0"
          :type="buttontype">{{ buttonText
          }}</el-button>
      </div>
    </div>

    <!-- 步骤条 -->
    <div class="button"
      style="text-align: center; position: fixed; margin-top: 10px; bottom: 10px; width: 100%; z-index:10">
      <el-button @click="laststep()" :disabled="steps <= 0" type="warning">上一步</el-button>
      <el-button @click="nextstep()" v-if="steps < 4" :disabled="!Visible || (steps == 2 && chartpoints == null)"
        type="primary">下一步</el-button>
    </div>
  </div>
  <!-- 错误提示 -->
  <div v-if="errorMessage" class="error-message">
    {{ errorMessage }}
  </div>
</template>

<script>
import { connectWebSocket, sampleWebSocket } from '@/axios';
import chartpointsmap from '@/components/chartspoints.vue'

function getNumber(theNumber) {
  if (theNumber > 0) {
    return "+" + theNumber.toFixed(3);
  } else {
    return theNumber.toString();
  }
}
export default {
  components: {
    chartpointsmap,
  },

  data() {
    return {
      dialogVisible: false,
      Visible: false,
      dialogImageUrl: null,

      // 存储图片宽高
      localx: null,
      localy: null,

      scale: null, // 图片缩放比例，默认为1，即不缩放
      scaledPoints: [], // 保存根据缩放比例调整后的标点位置

      //传出参数
      proofImage: null,
      pointsid: 0,//点的个数
      points: [], // 存储标点的坐标
      circle: 5,//滑块半径
      functions: 'R/G',
      xValue: [],
      Goal: '0.95',
      iteration: '20000',
      methord: false,
      notAutoFunc: false,


      //axios
      pendingData: null, //待发送的数据
      message: null, //数据
      socket: null,
      statuss: '未连接',

      //结果数据
      chartresult: null,
      chartpoints: null,
      chartsdatapoint: null,
      autoFuncProgress: null,
      steps: 0,//步骤条

      //处理按钮
      buttontype: 'primary',
      loading: false,
      buttonText: '开始处理',

      // sample数据区
      proofImage2: null,
      localx2: null,
      localy2: null,
      Visible2: false,
      pointsid2: 0,
      points2: [],
      scale2: null,
      scaledPoints2: [],
      sampleresult: null,

      //下载数据
      downloaData:[],
      //错误处理
      errorMessage: null,
    }
  },

  mounted() {
  },

  methods: {
    //第一页
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
    //第二页
    getFile2(file, fileList) {
      this.getBase64(file.raw).then(res => {
        const params = res.split(',')
        //console.log(params, 'params')
        if (params.length > 0) {
          this.proofImage2 = params;
          const image = new Image();
          image.src = res;
          // 当图片加载完成后执行回调函数
          image.onload = () => {
            this.localx2 = image.width;
            this.localy2 = image.height;
          }
        }
      })
      this.Visible2 = true;
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
    // 替身
    handleUploadRemove2(file, fileList) {
      this.proofImage2 = '';
      this.pointsid2 = 0;
      this.points2 = [];
      this.scaledPoints2 = [];
      this.localx2 = null;
      this.localy2 = null;
      this.Visible2 = false;
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

    //自动触发一次图片点击以便于确认比例
    autoclick() {
      const img = this.$refs.image;
      img.click();
      this.delpoint(1);
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
      this.xValue.splice(index, 1);
      this.scaledPoints.splice(index, 1);
      this.pointsid = this.pointsid - 1;
      //console.log(this.pointsradios);
    },
    isDeleteDisabled(id) {//判断按钮
      const maxId = Math.max(...this.points.map(point => point.id));
      return id !== maxId;
    },
    // 替身
    handleImageClick2(event) {
      if (this.pointsid2 == 1) {
        this.points2.splice(0, 1);
        this.scaledPoints2.splice(0, 1);
        this.pointsid2 = this.pointsid2 - 1;
      }
      const imgWidth = event.target.width;
      const imgHeight = event.target.height;
      const img = event.target;
      const displayWidth = img.getBoundingClientRect().width;// 获取图片的显示宽度
      this.scale2 = displayWidth / this.localx2;
      const x = Math.round((event.offsetX / imgWidth) * this.localx2);
      const y = Math.round((event.offsetY / imgHeight) * this.localy2);
      this.pointsid2 = this.pointsid2 + 1;
      const id = this.pointsid2;
      const cir = this.circle;
      this.points2.push({ id, x, y, cir });
      const scaledX = Math.round(x * this.scale2);
      const scaledY = Math.round(y * this.scale2);
      this.scaledPoints2.push({ id, x: scaledX, y: scaledY, cir })
    },
    //删除某一标点
    delpoint2(id) {
      const index = this.points2.findIndex(point => point.id === id);
      this.points2.splice(index, 1);
      this.scaledPoints2.splice(index, 1);
      this.pointsid2 = this.pointsid2 - 1;
    },

    // 选择方法1，2
    choosemethod(num) {
      if (num == 1) {
        this.methord = false;
      }
      else if (num == 2) {
        this.methord = true;
      }
      else {
        // 抛出错误弹窗
      }
      this.steps = this.steps + 1;
      console.log(this.methord);
    },

    //处理发送数据
    makedata() {
      // 创建一个空对象
      const dataToSend = {};
      dataToSend.image = this.proofImage[0] + ',' + this.proofImage[1];
      dataToSend.circles = this.points.map(point => `${point.x},${point.y},${this.circle}`).join("\n");
      dataToSend.function = this.functions;
      console.log(this.xValue.length,this.points.length)
      if (this.xValue.length !== this.points.length) {
        ElNotification({
          title: 'Error',
          message: '请确保每一个Xvalue都有值',
          type: 'error',
        });
        return;
      }
      dataToSend.xValue = this.xValue.join("\n");
      dataToSend.Goal = this.Goal;
      dataToSend.methord = this.methord;
      dataToSend.notAutoFunc = this.notAutoFunc;
      dataToSend.iteration = this.iteration;
      const jsonToSend = JSON.stringify(dataToSend);
      this.pendingData = jsonToSend;
      // console.log(this.notAutoFunc);
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
            //console.log(event.data);
            this.message = JSON.parse(event.data);
            // console.log(this.message);
            //不同函数的方法
            if (this.notAutoFunc == false) {
              this.chartpoints = this.message.points;
              this.chartresult = this.message.result;
              this.errorchartdata(this.chartpoints);
            }
            else {
              if (this.message.status == 'busy') {
                this.autoFuncProgress = this.message.iteration / this.iteration;
                console.log(this.autoFuncProgress);
              }
              else if (this.message.status == 'done') {
                this.autoFuncProgress == 1;
                this.functions = this.message.Model;
              }
              if (this.message.status == "done") {
                //console.log(this.message.Model);

              }
              else if (this.message.status == "success") {
                this.chartresult = this.message.result;
                this.chartpoints = this.message.points;
                this.errorchartdata(this.chartpoints);
              }
            }
            //console.log(this.chartsdatapoint);
            //console.log(this.chartresult , this.chartpoints);
          }
          this.socket.onclose = () => {
            this.loading = false;
            this.buttontype = 'success';
            this.buttonText = '处理完成';
          }
        })
        .catch(error => {
          // 处理错误，这里只是简单地显示在页面上
          this.statuss = error.message;
        })
    },

    //选取样点
    makedata2() {
      const dataToSend = {};
      dataToSend.image = this.proofImage2[0] + ',' + this.proofImage2[1];
      let point = this.points2[0];
      let x = point.x; let y = point.y; let r = point.cir;
      console.log(x, y, r);
      dataToSend.circle = x + ',' + y + ',' + r;
      dataToSend.func = this.functions;
      dataToSend.intercept = this.chartresult[1];
      dataToSend.slope = this.chartresult[0];
      const jsonToSend = JSON.stringify(dataToSend);
      console.log(dataToSend);
      this.pointProcess(jsonToSend);
    },
    pointProcess(data) {
      sampleWebSocket(data)
        .then(socket => {
          this.socket = socket;
          this.loading = true;
          this.buttonText = '正在处理';
          this.buttontype = 'warning';
          this.socket.onmessage = event => {
            console.log(event.data);
            let message = JSON.parse(event.data);
            this.sampleresult = message.result;
          }
          this.socket.onclose = () => {
            this.loading = false;
            this.buttontype = 'success';
            this.buttonText = '处理完成';
          }
        })
        .catch(error => {
          this.sampleresult = error.message;
        })
    },

    //处理图表数据
    errorchartdata(data) {
      let x = [];
      let y = [];
      let error_y = [];
      for (let i = 0; i < data.length; i++) {
        x.push(data[i][0]);
        y.push(data[i][1]);
        error_y.push(data[i][2]);
      }
      //存入
      this.chartsdatapoint = [{
        x: x,
        y: y,
        error_y: {
          type: 'data',
          array: error_y,
          visible: true,
        },
        mode: 'markers',
        type: 'scatter',
        name: 'Data Points',
        line: {color : '#002f49'}
      },
      {
        x: [(x.at(0) - 0.1 * (x.at(-1) - x.at(0))), (x.at(-1) + 0.1 * (x.at(-1) - x.at(0)))],
        y: [(this.chartresult[0] * (x.at(0) - 0.1 * (x.at(-1) - x.at(0))) + this.chartresult[1]), (this.chartresult[0] * (x.at(-1) + 0.1 * (x.at(-1) - x.at(0))) + this.chartresult[1])],
        mode: 'lines',
        type: 'scatter',
        name: 'Fitting Line',
        line: {color : '#669bbb'}
      }];
      //console.log(this.chartsdatapoint);
    },

    //数据下载
    dataDownload(){
      let dataToDownload = '';
      let functionText = ('slope='+this.chartresult[0]+',intercept='+this.chartresult[1]+',r^2='+this.chartresult[2]);
      dataToDownload += functionText;
      dataToDownload += '\n';
      dataToDownload += 'x,y,error_y\n';
      for (let i = 0; i < this.message.points.length; i++) { // 遍历数据
        dataToDownload += this.message.points[i];
        dataToDownload += '\n';
      }
      // console.log(dataToDownload);
      const blob = new Blob([dataToDownload], { type: 'text/csv;charset=utf-8' });
      const link = document.createElement('a');
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', 'data.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
    //步骤
    nextstep() {
      this.buttontype = 'primary',
        this.loading = false,
        this.buttonText = '开始处理',
        this.steps = this.steps + 1;
      if (this.steps == 2 && this.scale == null) {
        this.$nextTick(() => {
          this.autoclick();
        });
      }
    },
    laststep() {
      this.buttontype = 'primary',
        this.loading = false,
        this.buttonText = '开始处理',
        this.steps = this.steps - 1;
    }

  },

  // 错误捕获钩子
  errorCaptured(err, vm, info) {
    // 在这里处理捕获到的错误
    console.error('错误信息:', err);
    console.error('Vue 实例:', vm);
    console.error('错误信息详情:', info);

    // 设置错误消息
    this.errorMessage = '捕获到错误：' + err.message;

    // 返回 true 表示错误已经处理，不会向上传播
    // 返回 false 或不返回任何值，错误会向上传播到全局错误处理器
    return true;
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

.error-message {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: red;
  color: white;
  padding: 10px;
  border-radius: 5px;
}
</style>