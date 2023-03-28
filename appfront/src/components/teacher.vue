<template>
  <div>
     <bk-compose-form-item class="select-demo">
       <div>&nbsp;</div>
        <bk-select v-model="value1" style="width: 140px" size="large" :clearable="false">
          <bk-option id="id" name="教师工号" @click="option_id"></bk-option>
          <bk-option id="ip" name="教师名称" @click="option_college"></bk-option>
          <bk-option id="source" name="学院名称" @click="option_dean"></bk-option>
          <bk-option id="content" name="简介信息" @click="option_infor"></bk-option>
        </bk-select>
        <bk-input style="width: 400px" size="large" v-model=textcontent v-if="value1 === 'id'" key:1 placeholder="教师工号" :left-icon="'bk-icon icon-search'"></bk-input>
        <bk-input style="width: 400px" size="large" v-model=textcontent v-if="value1 === 'ip'" key:1 placeholder="请输入教师名称" :left-icon="'bk-icon icon-search'"></bk-input>
        <bk-input style="width: 400px" size="large" v-model=textcontent v-if="value1 === 'source'" key:2 placeholder="请输入学院名称" :left-icon="'bk-icon icon-search'"></bk-input>
        <bk-input style="width: 400px" size="large" v-model=textcontent v-if="value1 === 'content'" key:3 placeholder="请输入简介信息" :left-icon="'bk-icon icon-search'"></bk-input>
       <bk-button type="search" theme="warning" @click="search_data" size="large">search</bk-button>
     </bk-compose-form-item>
     <div style="float:right;" class="container">
      <div>&nbsp;</div>
      <bk-button theme="primary" @click="toggleTableSize">样式设置</bk-button>
      <span class="ml10">当前尺寸：{{ size }} &nbsp;&nbsp;&nbsp;</span>
      <div>&nbsp;</div>
      <div class="inner">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <bk-popconfirm trigger="click" :ext-cls="'asadsadsads'" width="288" @confirm="addData()">
          <div slot="content">
              <bk-compose-form-item>
                <h3>教师工号: <bk-input v-model='create_id' type='text'/></h3>
                <h3>教师名称: <bk-input v-model="create_teacher_name" type='text'/></h3>
                <h3>学院名称: <bk-input v-model='create_college_name' type='text'/></h3>
                <h3>教师简介: <bk-input v-model='create_content' type='text'/></h3>
              </bk-compose-form-item>
          </div>
          <bk-button theme="primary" :disabled="status === 'USER'">添加</bk-button>
        </bk-popconfirm>
      </div>
      &nbsp;
    </div>
    <div style="float:left;">
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      &nbsp;<bk-icon type="upload" />&nbsp;<bk-button theme="success" @click="load_excel()"> 数据导出</bk-button>
    </div>
    <bk-table style="margin-top: 15px;"
        :data="page_data"
        :size="size"
        :pagination="pagination"
        @page-change="handlePageChange"
        @page-limit-change="handlePageLimitChange"
        @select="curSelected"
        @select-all="curAllSelected">
      <bk-table-column type="selection" width="60"></bk-table-column>  <!--可选的地方-->
      <bk-table-column type="index" label="序列" width="60"></bk-table-column>
      <bk-table-column label="教师工号" prop="id"></bk-table-column>
      <bk-table-column label="教师名称" prop="ip"></bk-table-column>
      <bk-table-column label="学院名称" prop="source"></bk-table-column>
      <bk-table-column label="专业简介" prop="content"></bk-table-column>
      <bk-table-column label="操作" width="150">
        <template slot-scope="props">
          <bk-popconfirm trigger="click" :ext-cls="'asadsadsads'" width="288"
                         @confirm="changeData(props.row.id, props.row.ip)">
              <div slot="content">
                  <bk-compose-form-item>
                    <h3>教师工号: <bk-input v-model="props.row.id" type='text' disabled="true"/></h3>
                    <h3>教师名称: <bk-input v-model="props.row.ip" type='text' disabled="true"/></h3>
                    <h3>学院名称: <bk-input v-model='update_college_name' type='text'/></h3>
                    <h3>教师简介: <bk-input v-model='update_content' type='text'/></h3>
                  </bk-compose-form-item>
              </div>
              <bk-button class="mr10" theme="primary" text :disabled="status === 'USER'">修改</bk-button>
          </bk-popconfirm>
          <bk-popconfirm trigger="click" :ext-cls="'asadsadsads'" width="288" @confirm="removeData(props.row.id)">
              <div slot="content">
                  <div class="demo-custom">
                      <i class="bk-icon icon-info-circle-shape pr5 content-icon"></i>
                      <div class="content-text">确认删除？一旦删除不可回滚</div>
                  </div>
              </div>
              <bk-button class="mr10" theme="primary" text :disabled="status === 'USER'">删除</bk-button>
          </bk-popconfirm>
          <bk-popover class="dot-menu" placement="bottom-start" theme="dot-menu light"
                      :trigger="props.$index % 2 === 0 ? 'click' : 'mouseenter'" :arrow="false" offset="15"
                      :distance="0">
            <span class="dot-menu-trigger"></span>
          </bk-popover>
        </template>
      </bk-table-column>
    </bk-table>
  </div>
</template>

<script>
import {bkTable, bkTableColumn, bkButton, bkPopover, bkComposeFormItem, bkInput, bkSelect, bkOption, bkColorPicker,
  bkIcon, bkPopconfirm} from 'bk-magic-vue'
import axios from 'axios'
import {host} from '../../static/js/host'

export default {
  name: 'teacher',
  components: {
    bkTable,
    bkTableColumn,
    bkButton,
    bkPopover,
    bkComposeFormItem,
    bkInput,
    bkSelect,
    bkOption,
    bkColorPicker,
    bkIcon,
    bkPopconfirm
  },
  data () {
    return {
      textcontent: '', // 搜索框输入内容
      size: 'small',
      data: [
        {
          id: '6666660000',
          ip: '6老师',
          source: '数学与统计学院',
          content: '最强大脑'
        },
        {
          id: '0000000000',
          ip: '0老师',
          source: '数学与统计学院',
          content: '肩比光华'
        }
      ],
      page_data: [],
      pagination: {
        current: 1, // 首页
        count: 0, // 总数
        limit: 10 // 限制
      },
      page_data: [],
      value1: 'ip',
      token: localStorage.token || sessionStorage.token,
      username: localStorage.username || sessionStorage.username,
      status: sessionStorage.status,
      update_college_name: '',
      update_content: '',
      create_college_name: '',
      create_teacher_name: '',
      create_id: '',
      create_content: '',
      cur_getData: true,
      select_list: [], // 判断是否被选中的列表，被点后全部实时更新
      select_list_all: false // 判断是否被全选
    }
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData () {
      axios.get(host + '/teacher/', { // 获取data列表中的数据
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
      }).then(response => {
        console.log('教师信息' + response.data)
        this.data = response.data.teacher // 列表的数据和data是绑一起的
        this.pagination['count'] = this.data.length
        this.cur_getData = true
        this.getPageData()
      })
        .catch(error => {
          console.log(error.response.data)
        })
    },
    getPageData () { // 分页操作显示列表
      this.page_data = []
      let start = (this.pagination.current - 1) * this.pagination.limit
      for (let i = start; i < this.pagination.current * this.pagination.limit  && i < this.pagination.count; i++) {
          this.page_data.push(this.data[i]);
      }
    },
    addData () {
      if (this.create_college_name && this.create_id && this.create_teacher_name && this.create_content) {
        axios.post(host + '/teacher/', JSON.parse(JSON.stringify(
          {
            'id': this.create_id,
            'name': this.create_teacher_name,
            'college_name': this.create_college_name,
            'content': this.create_content
          })), {
          headers: {
            'Authorization': 'Bearer ' + this.token
          },
          responseType: 'json'
        }).then(response => {
          this.data.push({
            'id': this.create_id,
            'ip': this.create_teacher_name,
            'source': this.create_college_name,
            'content': this.create_content
          })
        }).catch(error => {
          alert(error.response.data.message)
          console.log(error.response.data.message)
        })
      } else {
        this.errorInfoBox('不能存在输入为空')
      }
    },
    changeData (id, ip) {
      if (this.update_content) {
        axios.put(host + '/teacher/' + id + '/', JSON.parse(JSON.stringify(
          {
            'id': id,
            'college_name': this.update_college_name,
            'content': this.update_content
          })), {
          headers: {
            'Authorization': 'Bearer ' + this.token
          },
          responseType: 'json'
        }).then(response => {
          for (let i = 0; i < this.data.length; i++) {
            if (this.data[i].id === id) { // 修改
              this.data[i].source = this.update_college_name
              this.data[i].content = this.update_content
              break
            }
          }
        }).catch(error => {
          alert(error.response.data.message)
          console.log(error.response.data.message)
        })
      } else {
        this.errorInfoBox('不能存在输入为空')
      }
    },
    removeData (id) {
      // 删除数据
      axios.delete(host + '/teacher/' + id + '/', {
        headers: {
          'Authorization': 'Bearer ' + this.token
        },
        responseType: 'json'
      }).then(response => {
        for (let i = 0; i < this.data.length; i++) {
          if (this.data[i].id === id) { // 从数组中移除地址
            this.data.splice(i, 1)
            break
          }
        }
      }).catch(error => {
        console.log(error.response.data)
      })
    },
    search_data () { // 通过v-model绑定的textcontent获取文本内容，通过下滑框对应的value1获取下拉框选择的对象  搜索数据
      if (!this.textcontent) {
        this.handleSingle('欢迎使用GDUT DBA', '龙洞小助手提醒您搜索内容请有所输入，否则还是原信息')
        if (!this.cur_getData) {
          this.getData()
        }
      } else {
        let param = ''
        if (this.value1 === 'ip') {
          param = {name: this.textcontent}
        } else if (this.value1 === 'source') {
          param = {college_name: this.textcontent}
        } else if (this.value1 === 'content') {
          param = {content: this.textcontent}
        } else if (this.value1 === 'id') {
          param = {id: this.textcontent}
        } else {
          alert('操作客户端变量被篡改的风险，请刷新页面')
        }

        axios.get(host + '/teacher/search/', { // 获取data列表中的数据
          headers: {
            'Authorization': 'Bearer ' + this.token
          },
          responseType: 'json',
          params: param
        }).then(response => {
          console.log('筛选的教师信息：' + response.data)
          this.data = response.data.teacher // 列表的数据和data是绑一起的
          this.pagination['count'] = this.data.length
          this.cur_getData = false
          this.getPageData()
        })
          .catch(error => {
            console.log(error.response.data)
          })
      }
    },
    load_excel () { // JSON格式
      if (!this.select_list_all && this.select_list == null) {
        return
      }
      this.to_excel(this.select_list_all ? this.data : this.select_list)
    },
    to_excel (data) { // 转化成excel
      let str = '<tr><td>教师工号</td><td>教师名称</td><td>学院名称</td><td>教师简介</td></tr>' // 列标题
      // 循环遍历，每行加入tr标签，每个单元格加td标签
      for (let i = 0; i < data.length; i++) {
        str += '<tr>'
        for (const key in data[i]) { // 增加' '为了不让表格显示科学计数法或者其他格式
          str += '<td>' + data[i][key] + ' ' + '</td>'
        }
        str += '</tr>'
      }
      const worksheet = 'Sheet1' // Worksheet名
      const uri = 'data:application/vnd.ms-excel;base64,'

      // 下载的表格模板数据
      const template = `<html xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:x="urn:schemas-microsoft-com:office:excel"
      xmlns="http://www.w3.org/TR/REC-html40">
      <head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>
      <x:Name>${worksheet}</x:Name>
      <x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet>
      </x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]-->
      </head><body><table>${str}</table></body></html>`
      // 下载模板
      window.location.href = uri + window.btoa(unescape(encodeURIComponent(template))) // +后是编码
    },
    option_college () { // 根据下化框选择学院
      this.value1 = 'ip'
    },
    option_dean () {
      this.value1 = 'source'
    },
    option_infor () {
      this.value1 = 'content'
    },
    option_id () {
      this.value1 = 'id'
    },
    toggleTableSize () { // 调整尺寸函数
      const size = ['small', 'medium', 'large']
      const index = (size.indexOf(this.size) + 1) % 3
      this.size = size[index]
    },
    handlePageChange (page) { // 回调当前页
      this.pagination.current = page
      this.getPageData()
    },
    handlePageLimitChange () { // 当用户切换表格每页显示条数时会出发的事件
      console.log('handlePageLimitChange', arguments)
      this.pagination.limit = arguments[0]
      this.getPageData()
    },
    curSelected (selection, row) { // 根据文档提示的回调函数及对应参数，（selection, row）其中row就可以把选中行所有数据取出来，但我们这里只需要从data把值该位selected
      console.log(selection)
      this.select_list = []
      for (let i = 0; i < selection.length; i++) {
        this.select_list.add(selection[i])
      }
    },
    curAllSelected (selection) { // 点首栏的选择全部才会进入这里
      this.select_list = [] // 清空select_list_id，以防突然地不勾选或勾选
      this.select_list_all = selection.length > 0
      console.log(selection)
      console.log(selection.length)
      console.log(this.select_list_all)
    },
    errorInfoBox (msg) {
      const a = this.$bkInfo({
        type: 'error',
        title: 'Fail:' + msg,
        subTitle: '窗口2秒后关闭',
        showFooter: false
      })
      let num = 2
      let t = setInterval(() => {
        a.subTitle = `此窗口${--num}秒后关闭`
        if (num === 0) {
          clearInterval(t)
          a.close()
        }
      }, 1000)
    },
    handleSingle (title, message) {
      let msg = {theme: 'warning'}
      msg.title = title
      msg.message = message
      msg.offsetY = 80
      msg.limitLine = 3
      this.$bkNotify(msg)
    }
  }
}
</script>

<style>
.demo-custom {
    font-size: 14px;
    line-height: 24px;
    color: #63656e;
    padding-bottom: 10px;
}
.content-icon {
    color: #ea3636;
    position: absolute;
    top: 20px;
}
.content-text {
    display: inline-block;
    margin-left: 20px;
}

.dot-menu {
    display: inline-block;
    vertical-align: middle;
}
.dot-menu-trigger {
    display: block;
    width: 30px;
    height: 30px;
    line-height: 30px;
    border-radius: 50%;
    text-align: center;
    font-size: 0;
    color: #979BA5;
    cursor: pointer;
}
.dot-menu-trigger:hover {
    color: #3A84FF;
    background-color: #EBECF0;
}
.dot-menu-trigger:before {
    content: "";
    display: inline-block;
    width: 3px;
    height: 3px;
    border-radius: 50%;
    background-color: currentColor;
    box-shadow: 0 -4px 0 currentColor, 0 4px 0 currentColor;
}
.dot-menu-list {
    margin: 0;
    padding: 5px 0;
    min-width: 50px;
    list-style: none;
}
.dot-menu-list .dot-menu-item {
    padding: 0 10px;
    font-size: 12px;
    line-height: 26px;
    cursor: pointer;
}
.dot-menu-list .dot-menu-item:hover {
    background-color: #eaf3ff;
    color: #3a84ff;
}
</style>
