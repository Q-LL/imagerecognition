<template>
  <div>
    <row>开始使用</row>
  </div>
  <div>
    <el-dialog :visible.sync="dialogVisible" append-to-body>
      <img width="100%" :src="dialogImageUrl" alt />
    </el-dialog>
    <el-upload list-type="picture" action='' accept=".jpg, .png" :limit="1" :auto-upload="false" :file-list="fileList"
      :on-change="getFile" :on-preview="handlePictureCardPreview" :on-remove="handleUploadRemove">
      <el-button size="small" type="primary">选择图片上传</el-button>
      <div slot="tip" class="el-upload__tip">只能上传一张jpg/png文件</div>
    </el-upload>
    

  </div>
</template>

<script>
export default {
  data() {
    return {
      dialogVisible:false,
      dialogImageUrl:null,
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
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },

    
  },
}
</script>

<style scoped>

</style>
