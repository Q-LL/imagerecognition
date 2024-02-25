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
        <el-table-column label="半径"> <template #default="scope"><el-input v-model="pointsradios[scope.row.id - 1]" placeholder="请输入半径" size="small"></el-input></template></el-table-column>
        <el-table-column label="操作"><template #default="scope"><el-button size="small" type="danger" :disabled="isDeleteDisabled(scope.row.id)" @click="delpoint(scope.row.id)">删除</el-button></template></el-table-column>
      </el-table>
    </div>

    <!-- 开始处理 -->
    <el-button>开始处理</el-button>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  data() {
    return {
      dialogVisible: false,
      Visible: false,
      dialogImageUrl: null,
      proofImage: null,
      pointsid: 0,//点的个数
      points: [], // 存储标点的坐标
      pointsradios: [],//储存标点半径
      // 存储图片宽高
      localx: null,
      localy: null,
    }
  },

  methods: {
    getFile(file, fileList) {
      this.getBase64(file.raw).then(res => {
        const params = res.split(',')
        //console.log(params, 'params')
        if (params.length > 0) {
          this.proofImage = params[1];
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
      url = 'data:image/png;base64,' + img;
      return url;
    },

    // 处理图片点击
    handleImageClick(event) {
      const imgWidth = event.target.width;
      const imgHeight = event.target.height;
      const x = (event.offsetX / imgWidth) * this.localx;
      const y = (event.offsetY / imgHeight) * this.localy;
      // 添加到points数组中
      this.pointsid = this.pointsid + 1;
      const id = this.pointsid;
      this.points.push({ id, x, y })
    },
    //删除某一标点
    delpoint(id) {
      const index = this.points.findIndex(point => point.id === id);
      this.points.splice(index, 1);
      this.pointsradios.splice(index, 1);
      this.pointsid = this.pointsid - 1;
      //console.log(this.pointsradios);
    },
    isDeleteDisabled(id) {//判断按钮
      const maxId = Math.max(...this.points.map(point => point.id));
      return id !== maxId;
    }

  },
}
</script>

<style scoped></style>