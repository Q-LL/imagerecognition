<template>
  <div class="header">
    <div class="tabs">
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane :label="$t('app.start')" name="first">
          <router-view />
        </el-tab-pane>
        <el-tab-pane :label="$t('app.about')" name="second">
          <router-view />
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="dropdown">
      <el-dropdown>
        <el-button type="primary">
          {{ $t('app.language') }}<el-icon class="el-icon--right">
            <ArrowDownBold />
          </el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="changeLanguage('zh-cn')">中文</el-dropdown-item>
            <el-dropdown-item @click="changeLanguage('en-us')">English</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
      <el-link icon="" href="https://github.com/your-project" target="_blank"></el-link>
    </div>
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
};
const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
  constructor(callback) {
    callback = debounce(callback, 16);
    super(callback);
  }
};

import { ref } from 'vue'
import { useI18n } from 'vue-i18n';
import router from './router'

export default {
  setup() {
    const { locale } = useI18n();
    const activeName = ref('first');

    //切换语言
    const changeLanguage = (lang) => {
      locale.value = lang;
    };

    // 切换路由
    const handleClick = (tab) => { // 删除类型注解
      //console.log(tab.props.name);
      switch (tab.props.name) {
        case 'first':
          router.push('/') // 跳转到主页
          break
        case 'second':
          router.push('/about') // 跳转到关于页面
          break
        default:
          break
      }
    }

    return {
      activeName, // 返回 activeName 变量
      changeLanguage, // 返回 changeLanguage 方法
      handleClick // 返回 handleClick 方法
    };
  }
};

</script>

<style>
* {
  margin: 0;
  padding: 0;
  border: 0
}

.header {
  width: 95vw;
  height: 4vh;
  padding-left: 1%;
  padding-top: 1vh;
  display: flex;
  justify-content: space-between;
}

.dropdown {
  position: absolute;
  right: 5%;
}

</style>
