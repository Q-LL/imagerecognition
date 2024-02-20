<template>
  <div class="header">
    <router-link to="/">主页</router-link> |
    <router-link to="/">开始使用</router-link> |
    <router-link to="/about">关于项目</router-link>
  </div>
  <div>
    <router-view/>
  </div>
  <div class="footer">

  </div>
</template>

<style>
.header{
  text-align: center;
  
}
</style>
