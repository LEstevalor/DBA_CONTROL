<template>
  <div style="background-color: #e5f3e9">
    <img src="../assets/TEGNOLOGY2.jpg" style="float:left;"/>
    <bk-swiper :pics="pics" :loop-time="4000" class="swiper" style="float:right;"></bk-swiper>
    <h1>KEY: 数据库  存储  SQL  NOSQL  MYSQL  REDIS  安全  并发  缓存  内存  服务  集群</h1>
  </div>
</template>

<script>
import { bkSwiper } from 'bk-magic-vue'
import firstSwiper from '../assets/2023label.jpg'
import secondSwiper from '../assets/gdut_label.jpg'
import thirdSwiper from '../assets/db.jpg'
import fourthSwiper from '../assets/nosql.jpg'
import fifthSwiper from '../assets/machine.jpg'
import sixthSwiper from '../assets/dragonCenter.jpg'


export default {
  name: 'top',
  components: {
    bkSwiper // 轮播图
  },
  data () {
    return {
      pics: [
        // { url: firstSwiper, link: 'https://www.npmjs.com/package/bk-magic-vue' },
        {url: firstSwiper},
        {url: secondSwiper},
        {url: thirdSwiper},
        {url: fourthSwiper},
        {url: fifthSwiper},
        {url: sixthSwiper}
      ]
    }
  },
  mounted () {
    // 未登录跳转回登录页面逻辑
    var username = sessionStorage.username || localStorage.username // 注意取的是Storage的信息
    if (username && (sessionStorage.token || localStorage.token)) {
      console.log('登录了')
    } else {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.swiper {
  width: 76%;
  height: 75%; /* 600px; */
}
</style>
