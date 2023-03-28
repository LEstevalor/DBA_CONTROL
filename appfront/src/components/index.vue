<template>
  <div class="monitor-navigation">
    <bk-navigation
      :header-title="nav.id"
      :side-title="nav.title"
      :default-open="false"
      :navigation-type="curNav.nav"
      :need-menu="curNav.needMenu"
      @toggle="handleToggle">
      <template slot="header">
        <div class="monitor-navigation-header">
          <div class="header-title">
            <span class="header-title-icon">
              <svg class="icon" style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4756"><path d="M416 480h320v64H416l96 96-48 48-176-176 176-176 48 48-96 96z" p-id="4757"></path></svg>
            </span>
            {{nav.id}}
          </div>
          <bk-select class="header-select" :class="{ 'is-left': curNav.nav === 'left-right' }" v-model="header.bizId" :clearable="false" searchable>
            <bk-option v-for="option in header.selectList"
              :key="option.id"
              :id="option.id"
              :name="option.name">
            </bk-option>
          </bk-select>
          <bk-popover theme="light navigation-message" placement="bottom" :arrow="false" offset="0, 5" trigger="mouseenter" :tippy-options="{ 'hideOnClick': false }">
            <div class="header-mind" :class="{ 'is-left': curNav.nav === 'left-right' }">
              <span class="bk-icon icon-chinese lang-icon"></span>
            </div>
            <template slot="content">
              <ul class="monitor-navigation-admin">
                <li class="nav-item" v-for="langItem in lang.list" :key="langItem.id">
                  <i :class="`bk-icon icon-${langItem.id} lang-icon`"></i>{{langItem.name}}
                </li>
              </ul>
            </template>
          </bk-popover>
          <bk-popover theme="light navigation-message" :arrow="false" offset="-150, 5" trigger="mouseenter" :tippy-options="{ 'hideOnClick': false }">
            <div class="header-mind" :class="{ 'is-left': curNav.nav === 'left-right' }">
              <svg style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 64 64" version="1.1" xmlns="http://www.w3.org/2000/svg">
                <path d="M32,56c-1.3,0-2.6-0.6-3.4-1.6h-4.5c0.5,1.5,1.4,2.7,2.6,3.7c3.1,2.5,7.5,2.5,10.6,0c1.2-1,2.1-2.3,2.6-3.7h-4.5C34.6,55.4,33.3,56,32,56z"></path>
                <path d="M53.8,49.1L50,41.5V28c0-8.4-5.8-15.7-14-17.6V8c0-2.2-1.8-4-4-4s-4,1.8-4,4v2.4c-8.2,1.9-14,9.2-14,17.6v13.5l-3.8,7.6c-0.3,0.6-0.3,1.3,0.1,1.9c0.4,0.6,1,1,1.7,1h40c0.7,0,1.3-0.4,1.7-1C54,50.4,54.1,49.7,53.8,49.1z"></path>
              </svg>
              <span class="header-mind-mark" :class="{ 'is-left': curNav.nav === 'left-right' }"></span>
            </div>
            <template slot="content">
              <div class="monitor-navigation-message">
                <h5 class="message-title">消息中心</h5>
                <ul class="message-list">
                  <li class="message-list-item" v-for="(item,index) in message.list" :key="index">
                    <span class="item-message">{{item.message}}</span>
                    <span class="item-date">{{item.date}}</span>
                  </li>
                </ul>
                <div class="message-footer">进入消息中心</div>
              </div>
            </template>
          </bk-popover>
          <bk-popover theme="light navigation-message" :arrow="false" offset="-20, 10" placement="bottom-start" :tippy-options="{ 'hideOnClick': false }">
            <div class="header-help" :class="{ 'is-left': curNav.nav === 'left-right' }">
              <svg class="bk-icon" style="width: 1em; height: 1em;vertical-align: middle;fill: currentColor;overflow: hidden;" viewBox="0 0 64 64" version="1.1" xmlns="http://www.w3.org/2000/svg">
                <path d="M32,4C16.5,4,4,16.5,4,32c0,3.6,0.7,7.1,2,10.4V56c0,1.1,0.9,2,2,2h13.6C36,63.7,52.3,56.8,58,42.4S56.8,11.7,42.4,6C39.1,4.7,35.6,4,32,4z M31.3,45.1c-1.7,0-3-1.3-3-3s1.3-3,3-3c1.7,0,3,1.3,3,3S33,45.1,31.3,45.1z M36.7,31.7c-2.3,1.3-3,2.2-3,3.9v0.9H29v-1c-0.2-2.8,0.7-4.4,3.2-5.8c2.3-1.4,3-2.2,3-3.8s-1.3-2.8-3.3-2.8c-1.8-0.1-3.3,1.2-3.5,3c0,0.1,0,0.1,0,0.2h-4.8c0.1-4.4,3.1-7.4,8.5-7.4c5,0,8.3,2.8,8.3,6.9C40.5,28.4,39.2,30.3,36.7,31.7z"></path>
              </svg>
            </div>
            <template slot="content">
              <ul class="monitor-navigation-admin">
                <div class="nav-item" v-for="name in help.list" :key="name">
                  {{ name }}
                </div>
              </ul>
            </template>
          </bk-popover>
          <bk-popover theme="light navigation-message" :arrow="false" offset="-20, 10" placement="bottom-start" :tippy-options="{ 'hideOnClick': false }">
            <div class="header-user" :class="{ 'is-left': curNav.nav === 'left-right' }">
              {{username_realname}}
              <i class="bk-icon icon-down-shape"></i>
            </div>
            <template slot="content">
              <ul class="monitor-navigation-admin">
<!--                <div class="nav-item" v-for="userItem in user.list" :key="userItem">-->
<!--                  <div id='self-information' @click="information">个人信息</div>-->
<!--                </div>-->
<!--                <div class="nav-item" v-for="userItem in user.list" :key="userItem">-->
<!--                  <div id='control' @click="control">权限中心</div>-->
<!--                </div>-->
                <div class="nav-item" v-for="userItem in user.list" :key="userItem">
                  <div id='login-out' @click="login_out">退出登录</div>
                </div>
              </ul>
            </template>
          </bk-popover>
        </div>
      </template>
      <template slot="menu">
        <bk-navigation-menu
          ref="menu"
          @select="handleSelect"
          :default-active="nav.id"
          :before-nav-change="beforeNavChange"
          :toggle-active="nav.toggle">
          <bk-navigation-menu-item
            v-for="item in nav.list"
            :key="item.name"
            :group="item.group"
            :icon="item.icon"
            :disabled="item.disabled"
            :url="item.url"
            :id="item.name"
          v-on:click="checkout(item.name)">
<!--            :@click="checkout(item.name)">  &lt;!&ndash;通过ID绑定函数，遍历绑定id&ndash;&gt;-->
            <span>{{item.name}}</span>
          </bk-navigation-menu-item>
        </bk-navigation-menu>
      </template>
      <router-view class="monitor-navigation-content"></router-view>
      <fx67ll-binary-clock :isShowTime="true" :zoomSize="1"></fx67ll-binary-clock>
    </bk-navigation>
  </div>
</template>

<script>
import { bkNavigation, bkNavigationMenu, bkNavigationMenuItem, bkSelect, bkOption, bkPopover, bkButton } from 'bk-magic-vue'
import axios from 'axios'
import {host} from '../../static/js/host'

export default {
  name: 'monitor-navigation',
  components: {
    bkNavigation,
    bkNavigationMenu,
    bkNavigationMenuItem,
    bkSelect,
    bkOption,
    bkPopover,
    bkButton
  },
  data () {
    return {
      username_realname: 'USER',
      status: 'USER',
      username: localStorage.username || sessionStorage.username,
      token: localStorage.token || sessionStorage.token,
      nav: {
        list: [
          {
            name: '首页',
            icon: 'icon-tree-application-shape',
            url: '/overview/',
            open: true,
            group: true
            // children: [
            //   {
            //     name: '首页',
            //     active: true
            //   }
            // ]
          },
          {
            name: '学院',
            icon: 'icon-tree-group-shape',
            url: '/bp/'
          },
          {
            name: '专业',
            icon: 'icon-tree-module-shape',
            url: '/component/'
          },
          {
            name: '教师',
            icon: 'icon-tree-process-shape',
            url: '/uptime_check/summary/'
          },
          {
            name: '学生信息',
            icon: 'icon-qq-shape',
            url: '/operation_monitor/'
            // children: [
            //   {
            //     name: '学生信息'
            //   },
            //   {
            //     name: '课程信息'
            //   }
            // ]
          },
          {
            name: '班级',
            icon: 'icon-clock-shape',
            url: '/datasource/'
          },
          {
            name: '课程信息',
            icon: 'icon-clock-shape',
            url: '/datasource/'
          },
          {
            name: '教研室',
            icon: 'icon-empty-shape',
            url: '/biz_manage/',
            group: true
          },
          // {
          //   name: '一级菜单',
          //   icon: 'icon-tree-process-shape',
          //   url: '/config/',
          //   disabled: true,
          //   children: [
          //     {
          //       name: '二级菜单1'
          //     },
          //     {
          //       name: '二级菜单2',
          //       children: [
          //         {
          //           name: '监控配置22'
          //         },
          //         {
          //           name: '监控配置23'
          //         }
          //       ]
          //     },
          //     {
          //       name: '二级菜单3'
          //     },
          //     {
          //       name: '二级菜单4'
          //     },
          //     {
          //       name: '二级菜单5'
          //     }
          //   ]
          // },
          {
            name: '账户信息',
            icon: 'icon-apps-shape',
            url: '/dashboard/',
            disabled: true
          },
          {
            name: '设置',
            icon: 'icon-apps-shape',
            url: '/dashboard/'
          },
          {
            name: '操作日志',
            icon: 'icon-weixin-shape',
            url: '/blank/'
          }
        ],
        id: '首页',
        toggle: false,
        submenuActive: false,
        title: 'GDUT-DBA教务平台'
      },
      header: {
        selectList: [
          {
            name: '学院信息',
            id: 1
          },
          {
            name: '专业信息',
            id: 2
          },
          {
            name: '教师信息',
            id: 3
          },
          {
            name: '学生课程',
            id: 4
          },
          {
            name: '班级信息',
            id: 5
          },
          {
            name: '课程信息',
            id: 6
          },
          {
            name: '教研室信息',
            id: 7
          }
        ],
        active: 2,
        bizId: 1
      },
      message: {
        list: [
          {
            message: '暂无信息'
            // date: '12月14日'
          }
        ]
      },
      user: {
        list: [
          '个人信息管理'
        ]
      },
      help: {
        list: [
          '问题反馈',
          '权限请求'
        ]
      },
      lang: {
        list: [
          {
            name: '中文',
            id: 'chinese'
          }
        ]
      }
    }
  },
  computed: {
    curNav () {
      return {
        nav: 'left-right',
        needMenu: true,
        name: '左右结构导航'
      }
    }
  },
  mounted () {
    // 未登录跳转回登录页面逻辑
    this.username = localStorage.username || sessionStorage.username // 注意取的是Storage的信息
    this.token = localStorage.token || sessionStorage.token
    console.log(this.username)
    console.log(this.token)
    if (this.username && this.token) {
      // 判断登录状态，通过JWT，判断username是否有效，token是否有效
      axios.get(host + '/check_user/', {
        // 向后端传递JWT token的方法
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
      })
        .then(response => {
          console.log('登录状态正确')
        }).catch(error => {
          console.log(error.response.data)
          this.$router.push('/login')
        })
    } else {
      this.$router.push('/login')
    }
    if (this.username === 'admin') {
      this.username_realname = 'ADMIN超级管理员'
      for (let i = 0; i < this.nav.list.length; i++) {
        if (this.nav.list[i].name === '账户信息') {
          this.nav.list[i].disabled = false
        }
      }
    } else {
      axios.get(host + '/get_username_realname/', {responseType: 'json',
        params: {username: this.username}}).then(
        response => {
          this.username_realname = response.data.username_realname
          console.log('Your name:' + this.username_realname)
        }).catch(error => {
        if (error.response.status === 400) {
          this.errorInfoBox(error.response.data.message)
        } else {
          console.log(error.response.data)
        }
      })
    }
    this.get_status() // 获取权限级别
    /* 以下代码是为了自适应例子父级的宽高而设置 */
    this.handleResize()
    window.addEventListener('resize', this.handleResize)
    /* 以上代码是为了自适应例子父级的宽高而设置 */
  },
  beforeDestroy () {
    /* 以下代码是为了自适应例子父级的宽高而设置 */
    window.removeEventListener('resize', this.handleResize)
    /* 以上代码是为了自适应例子父级的宽高而设置 */
  },
  methods: {
    get_status () { // 返回权限状态
      axios.get(host + '/status/', {
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json',
        params: {username: this.username}
      })
        .then(response => {
          this.status = response.data.status
          console.log('获取到权限状态:' + this.status)
          sessionStorage.status = this.status // 后端必须加判断，否则有风险
        }).catch(error => {
          console.log('获取不到权限状态')
          console.log(error.response.data)
        })
    },
    checkout (obj) {
      console.log(obj)
      if (obj === '首页') {
        this.$router.push('/top')
      } else if (obj === '学院' || obj === '学院信息') {
        this.$router.push('/college')
      } else if (obj === '专业' || obj === '专业信息') {
        this.$router.push('/major')
      } else if (obj === '教师' || obj === '教师信息') {
        this.$router.push('/teacher')
      } else if (obj === '学生信息') {
        this.$router.push('/student')
      } else if (obj === '班级' || obj === '班级信息') {
        this.$router.push('/grade')
      } else if (obj === '课程信息') {
        this.$router.push('/course')
      } else if (obj === '教研室' || obj === '教研室信息') {
        this.$router.push('/teach_student_class')
      } else if (obj === '账户信息') {
        this.$router.push('/user')
      } else if (obj === '设置') {
        this.$router.push('/setting')
      } else if (obj === '操作日志') {
        this.$router.push('/log')
      }
    },
    login_out () {
      // 清除客户端信息
      sessionStorage.clear()
      localStorage.clear()
      this.$router.push('/login') // 刷新一下
    },
    handleSelect (id, item) {
      this.nav.id = id
      console.info(`你选择了${id}`)
    },
    handleNavSelect (id, item) {
      this.nav.navId = id
      console.info(`你选择了${id}`)
    },
    handleToggle (v) {
      this.nav.toggle = v
    },
    beforeNavChange (newId, oldId) {
      console.info(newId, oldId)
      return true
    },
    handleResize (e) {
      if (window.innerWidth > 1615) {
        this.header.list.forEach(item => (item.show = true))
      } else if (window.innerWidth > 1515) {
        this.header.list[0].show = false
      } else if (window.innerWidth > 1415) {
        this.header.list[0].show = false
        this.header.list[1].show = false
      } else if (window.innerWidth > 1315) {
        this.header.list[0].show = false
        this.header.list[1].show = false
        this.header.list[2].show = false
      }
    }
  }
}
</script>

<style>
  @import '../../static/css/index.css';
</style>
