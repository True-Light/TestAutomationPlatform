<template>
  <div>
    <el-backtop style="position: center"></el-backtop>

    <div>
      <!-- 面包屑-->
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>任务管理</el-breadcrumb-item>
        <el-breadcrumb-item>任务结果</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 用例区域 -->
    <div>
      <el-card>
        <el-tabs v-model="activeName">
          <el-tab-pane label="自定义查询" name="first">
            <div>
              <el-row>
                <el-col :span="3">
                  <el-input>

                  </el-input>
                </el-col>
                <el-col :span="3" style="margin-left: 10px">
                  <el-button type="primary"
                             icon="el-icon-zoom-in" @click="searchResult()">
                    查询
                  </el-button>
                </el-col>
              </el-row>

            </div>
            <div>
            <el-table style="width: 100%" border :data="tableData" v-loading="loading">
              <template v-for="(item,index) in tableHead">
                <el-table-column :prop="item.column_name" :label="item.column_comment" :key="index" v-if="item.column_name != 'id'"></el-table-column>
              </template>
            </el-table>
            </div>
          </el-tab-pane>

          <el-tab-pane label="批量执行" name="second">
            <div>
              <el-button @click="toggleSelection()">开始执行</el-button>
              <el-button @click="toggleSelection()">取消选择</el-button>
            </div>
            <div>
              <el-table
                ref="multipleTable"
                :data="tableData"
                tooltip-effect="dark"
                style="width: 100%"
                @selection-change="handleSelectionChange">
                <el-table-column
                  type="selection"
                  width="55">
                </el-table-column>
                <el-table-column
                  label="日期"
                  width="120">
                  <template slot-scope="scope">{{ scope.row.date }}</template>
                </el-table-column>
                <el-table-column
                  prop="name"
                  label="姓名"
                  width="120">
                </el-table-column>
                <el-table-column
                  prop="address"
                  label="地址"
                  show-overflow-tooltip>
                </el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>
  </div>
</template>

<script>
  export default {
    name: "task_config",
    data() {
      return {
        loading: false,
        activeName: 'first',
        // 创建页面数据
        task_result_list: [],
        tester_list: [],

        queryForm: {
          choice_date: null,
          choice_tester: null,
        },
      }
    },
    created() {
      this.getPage()
    },
    methods: {
      // 配置标签方法
      filterTag1(value, row) {
        return row.task_stat === value;
      },
      // 配置标签方法
      filterTag2(value, row) {
        return row.result === value;
      },

      async getPage() {
        this.loading = true
        const {data: res} = await this.$http.get('task/get_result_page/')
        if (res.meta.status !== 200) {
          this.loading = false
          return this.$message.error(res.meta.msg)
        }
        this.task_result_list = res.data.task_result_list
        this.tester_list = res.data.tester_list
        this.loading = false
      },
      async searchResult() {
        this.loading = true
        const {data: res} = await this.$http.get('task/search_result/', {params:this.queryForm})
        if (res.meta.status !== 200) {
          this.loading = false
          return this.$message.error(res.meta.msg)
        }
        this.task_result_list = res.data.task_result_list
        this.loading = false
      },
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      }
    }
    }
  }
</script>

<style>
</style>
