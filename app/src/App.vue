<template>
  <div id="app">
    <el-container class="home-container">
      <el-header>
        <div>
          <span>test Report</span>
        </div>
        <el-button type="info" @click="logout">Exit</el-button>
      </el-header>

      <el-container>
        <el-aside width="200px" class="sidebar" style="border: none;">
          <el-menu default-active="1" class="menu" background-color="#333744" text-color="#fff" active-text-color="#409EFF">
            <el-menu-item index="3" @click="switchComponent('Movie')">
              <el-icon><document /></el-icon>
              <span>Movie</span>
            </el-menu-item>
            <el-menu-item index="1" @click="switchComponent('HelloWorld')">
              <el-icon><location /></el-icon>
              <span>HelloWorld</span>
            </el-menu-item>
            <el-menu-item index="2" @click="switchComponent('BarChart')">
              <el-icon><icon-menu /></el-icon>
              <span>BarChart</span>
            </el-menu-item>
            <el-menu-item index="3" @click="switchComponent('TableV')">
              <el-icon><document /></el-icon>
              <span>TableV</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="content">
          <component :is="currentComponent" :msg="content" />
          
        </el-main>
      </el-container>
      
    </el-container>
    
  </div>
</template>

<script>
import Movie from './components/Movie.vue'
import HelloWorld from './components/HelloWorld.vue'
import BarChart from './components/BarChart.vue'
import TableV from './components/TableV.vue'

export default {
  components: {
    Movie,
    HelloWorld,
    BarChart,
    TableV
  },
  methods: {
    switchComponent(componentName) {
      this.currentComponent = componentName
    },
    logout() {
      // 退出登录逻辑
    }
  },
  data() {
    return {
      content: '',
      currentComponent: 'Movie'
    }
  }
}
</script>

<style>
/* 全局樣式表 */
body {
  margin: 0;
}

.el-aside .el-menu {
  border-right: solid 1px #333744;
}

.home-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-header {
  background-color: #373d41;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
  font-size: 20px;
  padding: 0 20px;
}

.el-header>div {
  display: flex;
  align-items: center;
}

.el-header>div>span {
  margin-left: 15px;
}

.el-aside {
  background: #333744;
  flex: 0 0 200px;
}

.el-main {
  background-color: #eaedf1;
  flex: 1;
}

.sidebar {
  padding: 20px;
}

.navigation {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.navigation li {
  margin-bottom: 10px;
}

.content {
  padding: 20px;
}</style>