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
      <el-image style="width: 100%; height: 100%;" :src="showimg(proofImage)" :v-if="Visible" fit="scale-down"
        loading="lazy" @click="handleImageClick($event)">
        <template #error>
          <div class="image-slot">
            <el-icon><icon-picture /></el-icon>
          </div>
        </template>
      </el-image>
    </div>

    <!-- 标注数据 -->
    <div class="sign">
      <ul>
        <li v-for="(point, index) in points" :key="index">点{{index + 1}}: ({{point.x.toFixed(2)}}, {{point.y.toFixed(2)}})</li>
      </ul>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogVisible: false,
      Visible: false,
      dialogImageUrl: null,
      proofImage: null,
      points: [] // 存储标点的坐标
    }
  },
  methods: {
    getFile(file, fileList) {
      this.getBase64(file.raw).then(res => {
        const params = res.split(',')
        console.log(params, 'params')
        if (params.length > 0) {
          this.proofImage = params[1]
        }
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
      this.Visible = false;
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
      this.Visible = true;
    },

    //显示图片
    showimg(img) {
      let url;
      url = 'data:image/png;base64,' + img;
      return url;
    },

    // 处理图片点击
    handleImageClick(event) {
      // 获取图片的宽度和高度
      const imgWidth = event.target.width
      const imgHeight = event.target.height
      // 获取点击的位置相对于图片左上角的坐标
      const x = event.offsetX / imgWidth
      const y = event.offsetY / imgHeight
      // 添加到points数组中
      this.points.push({x, y})
    }
  },
}
</script>

<style scoped>
.img {
  width: 100vw;
  height: 50vh;
  background-color: #b1adad;
}
</style>