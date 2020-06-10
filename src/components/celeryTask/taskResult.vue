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
                <el-row>
                    <el-col :span="3">
                    <div class="block">
                        <el-date-picker
                          v-model="queryForm.choice_date"
                          type="date"
                          placeholder="可选择日期">
                        </el-date-picker>
                    </div>
                    </el-col>
                    <el-col :span="3" style="margin-left: 20px">
                    <el-select v-model="queryForm.choice_tester" placeholder="可选择负责人"
                               style="margin-left: 10px" >
                        <el-option v-for="item in tester_list" :key="item.id" :label="item.name" :value="item.name">
                        </el-option>
                    </el-select>
                    </el-col>
                    <el-col :span="3" style="margin-left: 10px">
                    <el-button type="primary"
                               icon="el-icon-zoom-in" @click="searchResult()">
                        查询
                    </el-button>
                    </el-col>
                </el-row>
            </el-card>
            <el-card>
                <!-- 表单区域 -->
                <el-table :data="task_result_list" border stripe
                          row-style="height: 0px"
                          v-loading="loading">
                    <el-table-column label="ID" type="index" width="40"></el-table-column>
                    <el-table-column label="任务名称" prop="task_name" width="200">
                    </el-table-column>
                    <el-table-column label="系统名称" prop="sys_name" width="200"></el-table-column>
                    <el-table-column label="模块名称" prop="sys_module" width="200">
                    </el-table-column>
                    <el-table-column label="接口名称" prop="sys_api" width="200">
                    </el-table-column>
                    <el-table-column label="响应码" prop="status" width="80"></el-table-column>
                    <el-table-column label="响应内容" prop="response"></el-table-column>
                    <el-table-column label="创建时间" prop="create_time" width="80"></el-table-column>
                    <el-table-column label="执行人" prop="operator" width="80"></el-table-column>
                    <el-table-column label="任务状态" prop="task_stat"
                                     width="90"
                                     :filters="[{ text: '创建', value: '创建' },
                                 { text: '运行', value: '运行' },
                                  {text: '成功', value: '成功' },
                                  {text: '失败', value: '失败' },]"
                                     :filter-method="filterTag1"
                                     filter-placement="bottom-end">
                        <template slot-scope="scope">
                            <el-tag :type="scope.row.task_stat === '创建' ? 'info' :
                                scope.row.task_stat === '运行'? 'primary':
                                scope.row.task_stat === '成功'? 'success':
                                scope.row.task_stat === '失败'? 'danger':'warning'"
                                    close-transition>{{scope.row.task_stat}}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column label="任务结果" prop="result"
                                     width="90"
                                     :filters="[{text: '成功', value: '1' },
                                  {text: '失败', value: '0' },]"
                                     :filter-method="filterTag2"
                                     filter-placement="bottom-end">
                        <template slot-scope="scope">
                            <el-tag :type="scope.row.result === '1' ? 'success' :
                                scope.row.result === '0'? 'danger': 'warning'"
                                    close-transition>{{scope.row.result}}
                            </el-tag>
                        </template>
                    </el-table-column>
                </el-table>
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
        }
    }
</script>

<style>
</style>
