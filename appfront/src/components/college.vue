<template>
  <div>
     <bk-compose-form-item class="select-demo">
       <div>&nbsp;</div>
        <bk-select v-model="value1" style="width: 140px" size="large" :clearable="false">
          <bk-option id="1" name="学院名称" @click="option_college"></bk-option>
          <bk-option id="2" name="院长名称" @click="option_dean"></bk-option>
          <bk-option id="3" name="简介信息" @click="option_infor"></bk-option>
        </bk-select>
        <bk-input style="width: 400px" size="large" v-model=textcontent v-if="value1 === '1'" key:1 placeholder="请输入学院名称" :left-icon="'bk-icon icon-search'"></bk-input>
        <bk-input style="width: 400px" size="large" v-model=textcontent v-if="value1 === '2'" key:2 placeholder="请输入院长名称" :left-icon="'bk-icon icon-search'"></bk-input>
        <bk-input style="width: 400px" size="large" v-model=textcontent v-if="value1 === '3'" key:3 placeholder="请输入简介信息" :left-icon="'bk-icon icon-search'"></bk-input>
       <bk-button type="search" @click="search_data" size="large">search</bk-button>
    </bk-compose-form-item>
    <div style="float:right;" class="container">
      <div>&nbsp;</div>
      <bk-button theme="primary" @click="toggleTableSize">样式设置</bk-button>
      <span class="ml10">当前尺寸：{{ size }} &nbsp;&nbsp;&nbsp;</span>
      <div>&nbsp;</div>
      <div class="inner">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<bk-button theme="primary" @click="addData">添加</bk-button>
      </div>
      &nbsp;
    </div>
    <div style="float:left;">
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      <div>&nbsp;</div>
      &nbsp;<bk-icon type="upload" />&nbsp;<bk-button theme="success" @click="load_excel"> 数据导出</bk-button>
    </div>
    <bk-table style="margin-top: 15px;"
        :data="data"
        :size="size"
        :pagination="pagination"
        @row-mouse-enter="handleRowMouseEnter"
        @row-mouse-leave="handleRowMouseLeave"
        @page-change="handlePageChange"
        @page-limit-change="handlePageLimitChange">
      <bk-table-column type="selection" width="60"></bk-table-column>
      <bk-table-column type="index" label="序列" width="60"></bk-table-column>
      <bk-table-column label="学院名称" prop="ip"></bk-table-column>
      <bk-table-column label="院长名称" prop="source"></bk-table-column>
      <bk-table-column label="学院简介" prop="content"></bk-table-column>
      <bk-table-column label="操作" width="150">
        <template slot-scope="props">
          <bk-button class="mr10" theme="primary" text :disabled="status === 'USER'" @click="changeData(props.row.ip)">
            修改</bk-button>
          <bk-button class="mr10" theme="primary" text :disabled="status === 'USER'" @click="removeData(props.row.ip)">
            删除</bk-button>
          <bk-popover class="dot-menu" placement="bottom-start" theme="dot-menu light"
                      :trigger="props.$index % 2 === 0 ? 'click' : 'mouseenter'" :arrow="false" offset="15"
                      :distance="0">
            <span class="dot-menu-trigger"></span>
            <ul class="dot-menu-list" slot="content">
              <li class="dot-menu-item">导入</li>
              <li class="dot-menu-item">导出</li>
            </ul>
          </bk-popover>
        </template>
      </bk-table-column>
    </bk-table>
  </div>
</template>

<script>
import {bkTable, bkTableColumn, bkButton, bkPopover, bkComposeFormItem, bkInput, bkSelect, bkOption, bkColorPicker,
  bkIcon} from 'bk-magic-vue'
// import axios from "axios";
// import {host} from "../../static/js/host";

export default {
  name: 'college',
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
    bkIcon
  },
  data () {
    return {
      textcontent: '', // 搜索框输入内容
      size: 'small',
      data: [
        {
          ip: '数学与统计学院',
          source: 'XXX',
          content: '最强大脑'
        },
        {
          ip: '管理学院',
          source: 'HHH',
          content: '肩比光华'
        }
      ],
      pagination: {
        current: 1,
        count: 100,
        limit: 10
      },
      value1: '1',
      token: localStorage.token || sessionStorage.token,
      username: localStorage.username || sessionStorage.username,
      status: sessionStorage.status
    }
  },
  mounted () {
    this.getData()
  },
  methods: {
    getData () {
      // 获取data列表中的数据
    },
    addData () {
      // 添加数据
    },
    changeData (name) {
      // 修改数据
    },
    removeData (name) {
      // 删除数据
    },
    search_data () { // 通过v-model绑定的textcontent获取文本内容，通过下滑框对应的value1获取下拉框选择的对象
      // 搜索数据
    },
    load_excel () {
      // 导出成excel格式
    },
    option_college () { // 根据下化框选择学院
      this.value1 = 1
    },
    option_dean () { // 根据下化框选择院长
      this.value1 = 2
    },
    option_infor () { // 根据下化框选择信息
      this.value1 = 3
    },
    handlePageLimitChange () {
      console.log('handlePageLimitChange', arguments)
    },
    toggleTableSize () { // 调整尺寸函数
      const size = ['small', 'medium', 'large']
      const index = (size.indexOf(this.size) + 1) % 3
      this.size = size[index]
    },
    handlePageChange (page) {
      this.pagination.current = page
    }
  }
}
</script>

<style>

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
