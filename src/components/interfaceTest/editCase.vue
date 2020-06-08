<template>
    <div>
        <el-backtop style="position: center"></el-backtop>

        <div>
            <!-- 面包屑-->
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>接口测试</el-breadcrumb-item>
                <el-breadcrumb-item>编辑用例</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <!-- 用例区域 -->
        <div>
            <el-tabs v-model="activeName">
                <el-tab-pane label="按项目查看" name="first">
                    <el-card>
                        <el-select v-model="queryProject.query" placeholder="请选择项目" @change="getProjectSelected">
                            <el-option v-for="item in project_list" :key="item.id" :label="item.name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-card>
                    <el-card>
                        <!-- 表单区域 -->
                        <el-table :data="project_case_list" border stripe v-loading="loading">
                            <el-table-column label="ID" type="index" width="40"></el-table-column>
                            <el-table-column label="用例名称" width="200">
                                <template slot-scope="scope">
                                    <el-popover trigger="hover" placement="top">
                                        <p>{{ scope.row.case_desc }}</p>
                                        <div slot="reference" class="name-wrapper">
                                            <el-tag size="medium">{{ scope.row.case_name }}</el-tag>
                                        </div>
                                    </el-popover>
                                </template>
                            </el-table-column>
                            <el-table-column label="步骤" prop="step_num" width="50"></el-table-column>
                            <el-table-column label="步骤名称" width="200">
                                <template slot-scope="scope">
                                    <el-popover trigger="hover" placement="top">
                                        <p>{{ scope.row.step_desc }}</p>
                                        <div slot="reference" class="name-wrapper">
                                            <el-tag size="medium">{{ scope.row.step_name }}</el-tag>
                                        </div>
                                    </el-popover>
                                </template>
                            </el-table-column>
                            <el-table-column label="前置函数" width="50">
                                <template slot-scope="scope">
                                <el-switch
                                  v-model="scope.row.set_up"
                                  active-color="#13ce66"
                                  inactive-color="#ff4949"
                                  active-value="1"
                                  inactive-value="0"
                                disabled>
                                </el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column label="后置函数" width="50">
                                <template slot-scope="scope">
                                    <el-switch
                                      v-model="scope.row.tear_down"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949"
                                      active-value="1"
                                      inactive-value="0"
                                      disabled>
                                    </el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column label="请求路径" prop="url" width="150"></el-table-column>
                            <el-table-column label="请求方式" prop="method" width="80"></el-table-column>
                            <el-table-column label="定义变量" prop="variable" width="150"></el-table-column>
                            <el-table-column label="请求头" prop="headers" width="150"></el-table-column>
                            <el-table-column label="参数(PARAM)" prop="params" width="150"></el-table-column>
                            <el-table-column label="请求体(FORM)" prop="form_data" width="150"></el-table-column>
                            <el-table-column label="请求体(JSON)" prop="json_data" width="150"></el-table-column>
                            <el-table-column label="是否断言" width="50">
                                <template slot-scope="scope">
                                    <el-switch
                                      v-model="scope.row.need_assert"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949"
                                      active-value="1"
                                      inactive-value="0"
                                      disabled>
                                    </el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column label="断言方式" prop="assert_method" width="100"></el-table-column>
                            <el-table-column label="预期响应码" prop="exp_statue" width="150"></el-table-column>
                            <el-table-column label="预期响应体" prop="exp_extract" width="150"></el-table-column>
                            <el-table-column label="操作" width="200" fixed="right">
                                <template slot-scope="scope">
                                    <el-tooltip content="查看详情" placement="top" :enterable="false" effect="light">
                                        <el-button type="primary"
                                                   icon="el-icon-view"
                                                   size="mini"
                                                   round
                                                   disabled>

                                        </el-button>
                                    </el-tooltip>
                                    <el-tooltip content="编辑此行" placement="top" :enterable="false" effect="light">
                                        <el-button type="primary"
                                                   icon="el-icon-edit"
                                                   size="mini"
                                                   round
                                                   @click="editRowP(scope.row.id)">
                                        </el-button>
                                    </el-tooltip>
                                    <el-tooltip content="删除此行" placement="top" :enterable="false" effect="light">
                                        <el-button type="primary"
                                                   icon="el-icon-delete"
                                                   size="mini"
                                                   round
                                                   @click="deleteRowP(scope.row.id)">
                                        </el-button>
                                    </el-tooltip>
                                </template>
                            </el-table-column>
                        </el-table>
                        <!-- 分页 -->
                        <el-pagination
                          @size-change="handleSizeChange"
                          @current-change="handleCurrentChange"
                          :current-page="queryProject.page_num"
                          :page-sizes="[10, 25, 50, 100]"
                          :page-size="queryProject.page_size"
                          layout="total, sizes, prev, pager, next, jumper"
                          :total="total">
                        </el-pagination>
                    </el-card>
                </el-tab-pane>
                <el-tab-pane label="按集合查看" name="second">
                    <el-card>
                        <el-select v-model="querySet.query" placeholder="请选择项目" @change="getSetSelected">
                            <el-option v-for="item in set_list" :key="item.id" :label="item.name" :value="item.id">
                            </el-option>
                        </el-select>
                    </el-card>
                    <el-card>
                        <!-- 表单区域 -->
                        <el-table :data="set_case_list" border stripe v-loading="loading">
                            <el-table-column label="ID" type="index" width="40"></el-table-column>
                            <el-table-column label="用例名称" width="200">
                                <template slot-scope="scope">
                                    <el-popover trigger="hover" placement="top">
                                        <p>{{ scope.row.case_desc }}</p>
                                        <div slot="reference" class="name-wrapper">
                                            <el-tag size="medium">{{ scope.row.case_name }}</el-tag>
                                        </div>
                                    </el-popover>
                                </template>
                            </el-table-column>
                            <el-table-column label="步骤" prop="step_num" width="50"></el-table-column>
                            <el-table-column label="步骤名称" width="200">
                                <template slot-scope="scope">
                                    <el-popover trigger="hover" placement="top">
                                        <p>{{ scope.row.step_desc }}</p>
                                        <div slot="reference" class="name-wrapper">
                                            <el-tag size="medium">{{ scope.row.step_name }}</el-tag>
                                        </div>
                                    </el-popover>
                                </template>
                            </el-table-column>
                            <el-table-column label="前置函数" width="50">
                                <template slot-scope="scope">
                                    <el-switch
                                      v-model="scope.row.set_up"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949"
                                      active-value="1"
                                      inactive-value="0"
                                      disabled>
                                    </el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column label="后置函数" width="50">
                                <template slot-scope="scope">
                                    <el-switch
                                      v-model="scope.row.tear_down"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949"
                                      active-value="1"
                                      inactive-value="0"
                                      disabled>
                                    </el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column label="请求路径" prop="url" width="150"></el-table-column>
                            <el-table-column label="请求方式" prop="method" width="80"></el-table-column>
                            <el-table-column label="定义变量" prop="variable" width="150"></el-table-column>
                            <el-table-column label="请求头" prop="headers" width="150"></el-table-column>
                            <el-table-column label="参数(PARAM)" prop="params" width="150"></el-table-column>
                            <el-table-column label="请求体(FORM)" prop="form_data" width="150"></el-table-column>
                            <el-table-column label="请求体(JSON)" prop="json_data" width="150"></el-table-column>
                            <el-table-column label="是否断言" width="50">
                                <template slot-scope="scope">
                                    <el-switch
                                      v-model="scope.row.need_assert"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949"
                                      active-value="1"
                                      inactive-value="0"
                                      disabled>
                                    </el-switch>
                                </template>
                            </el-table-column>
                            <el-table-column label="断言方式" prop="assert_method" width="100"></el-table-column>
                            <el-table-column label="预期响应码" prop="exp_statue" width="150"></el-table-column>
                            <el-table-column label="预期响应体" prop="exp_extract" width="150"></el-table-column>
                            <el-table-column label="操作" width="200" fixed="right">
                                <template slot-scope="scope">
                                    <el-tooltip content="查看详情" placement="top" :enterable="false" effect="light">
                                        <el-button type="primary"
                                                   icon="el-icon-view"
                                                   size="mini"
                                                   round
                                                   disabled>

                                        </el-button>
                                    </el-tooltip>
                                    <el-tooltip content="编辑此行" placement="top" :enterable="false" effect="light">
                                        <el-button type="primary"
                                                   icon="el-icon-edit"
                                                   size="mini"
                                                   round
                                                   @click="editRowS(scope.row.id)">
                                        </el-button>
                                    </el-tooltip>
                                    <el-tooltip content="删除此行" placement="top" :enterable="false" effect="light">
                                        <el-button type="primary"
                                                   icon="el-icon-delete"
                                                   size="mini"
                                                   round
                                                   @click="deleteRowS(scope.row.id)">
                                        </el-button>
                                    </el-tooltip>
                                </template>
                            </el-table-column>
                        </el-table>
                        <!-- 分页 -->
                        <el-pagination
                          @size-change="handleSizeChange1"
                          @current-change="handleCurrentChange1"
                          :current-page="queryProject.page_num1"
                          :page-sizes="[10, 25, 50, 100]"
                          :page-size="queryProject.page_size1"
                          layout="total, sizes, prev, pager, next, jumper"
                          :total="total1">
                        </el-pagination>
                    </el-card>
                </el-tab-pane>
            </el-tabs>
        </div>
    </div>
</template>

<script>
    export default {
        name: "interfaceCase",
        data() {
            return {
                loading: false,
                activeName: 'first',
                // 测试项目列表
                project_list: [],
                // 测试集合列表
                set_list: [],
                // 接收按项目分类的用例数据
                project_case_list: [],
                // 接收按集合分类的用例数据
                set_case_list: [],
                // 按项目请求
                total: 0,
                total1: 0,
                queryProject: {
                    query: null,
                    page_num: 1,
                    page_size: 10,
                },
                querySet: {
                    query: null,
                    page_num1: 1,
                    page_size1: 10,
                },

            }
            },
        created() {
            this.getPage()
        },
        methods: {
            async getPage() {
                this.loading = true
                const {data: res} = await this.$http.get('interface/create_edit_page/')
                if (res.meta.status !== 200) {
                    this.loading = false
                    return this.$message.error(res.meta.msg)
                }
                this.project_list = res.data.project_list
                this.set_list = res.data.set_list
                this.loading = false
            },
            async getProjectSelected() {
                this.loading = true
                const {data: res} = await this.$http.get('interface/query_project_case/', {params:this.queryProject})
                if (res.meta.status !== 200) {
                    this.loading = false
                    return this.$message.error(res.meta.msg)
                }
                this.project_case_list = res.data.project_case_list
                this.total = res.data.total
                this.loading = false
            },
            async getSetSelected() {
                this.loading = true
                const {data: res} = await this.$http.get('interface/query_set_case/', {params:this.querySet})
                if (res.meta.status !== 200) {
                    this.loading = false
                    return this.$message.error(res.meta.msg)
                }
                this.project_case_list = res.data.project_case_list
                this.total1 = res.data.total
                this.loading = false
            },
            // 监听分页数改变的事件
            handleSizeChange(newSize) {
                //console.log(newSize)
                this.queryInfo.page_size = newSize
                this.getProjectSelected()
            },
            // 监听页码 变化的事件
            handleCurrentChange(newPage) {
                //console.log(newPage)
                this.queryProject.page_num = newPage
                this.getProjectSelected()
            },
            // 监听分页数改变的事件
            handleSizeChange1(newSize) {
                //console.log(newSize)
                this.querySet.page_size1 = newSize
                this.getSetSelected()
            },
            // 监听页码 变化的事件
            handleCurrentChange1(newPage) {
                //console.log(newPage)
                this.querySet.page_num1 = newPage
                this.getSetSelected()
            },

            editRowP() {

            },
            deleteRowP() {

            },
            editRowS() {

            },
            deleteRowS() {

            },

        }
    }
</script>

<style>
</style>
