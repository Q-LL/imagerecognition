<template>
  <div class="header">
    <el-row style="margin: auto; width: 180px;">
      <router-link to="/">主页</router-link> |
      <router-link to="/start">开始使用</router-link> |
      <router-link to="/about">关于项目</router-link>
    </el-row>
    <el-row style="margin-left: 90%; padding: 0;">
      <el-dropdown>
        <el-button type="primary">
          选择语言<el-icon class="el-icon--right">
            <ArrowDownBold />
          </el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item>中文</el-dropdown-item>
            <el-dropdown-item>English</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-row>

  </div>
  <div>
    <router-view />
  </div>
  <div class="footer">

  </div>
</template>

<script>
//修复element-UI引起的ResizeObserver报错
const debounce = (fn, delay) => {
  let timer = null;
  return function () {
    let context = this;
    let args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  }
}
const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
  constructor(callback) {
    callback = debounce(callback, 16);
    super(callback);
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  border: 0
}

.header {
  background-color: #81c5f6be;
  width: 100vw;
  height: 4vh;
  padding-top: 1vh;
}
</style>
