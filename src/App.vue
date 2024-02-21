<template>
  <div class="header">
    <router-link to="/">主页</router-link> |
    <router-link to="/start">开始使用</router-link> |
    <router-link to="/about">关于项目</router-link>
  </div>
  <div>
    <router-view/>
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
.header{
  text-align: center;
  
}
</style>
