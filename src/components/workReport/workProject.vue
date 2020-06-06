<template>
    <div>
        <!-- 面包屑-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>工作日报</el-breadcrumb-item>
            <el-breadcrumb-item>历史报告</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row :gutter="20">
                <el-col :span="6">
                    <el-input placeholder="请输入内容" v-model="queryInfo.query" clearable @clear="getProject">
                        <el-button slot="append" icon="el-icon-search" @click="getProject"></el-button>
                    </el-input>
                </el-col>

                <el-col :span="4">

                </el-col>
            </el-row>
        </el-card>
        <el-card>
            <!-- 表单区域 -->

            <el-table :data="workProjectList" border stripe v-loading="loading">
                <el-table-column label="ID" type="index"></el-table-column>
                <el-table-column label="项目名称" prop="project_name" width="200px"></el-table-column>
                <el-table-column label="测试类型" prop="test_type" width="90px"></el-table-column>
                <el-table-column label="测试状态" prop="test_state"
                                 width="100"
                                 :filters="[{ text: '测试中', value: '测试中' },
                                 { text: '测试完成', value: '测试完成' },
                                  {text: '测试停滞', value: '测试停滞' },
                                   {text: '未开始', value: '未开始' }]"
                                 :filter-method="filterTag"
                                 filter-placement="bottom-end">
                    <template slot-scope="scope">
                        <el-tag :type="scope.row.test_state === '测试中' ? 'primary' :
                                scope.row.test_state === '测试完成'? 'success':
                                scope.row.test_state === '测试停滞'? 'danger':
                                scope.row.test_state === '未开始'? 'info': 'warning'"
                                close-transition>{{scope.row.test_state}}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="测试负责人" prop="test_master" width="90px"></el-table-column>
                <el-table-column label="测试参与人" prop="tester" width="90px"></el-table-column>
                <el-table-column label="开发负责人" prop="development_manager" width="90px"></el-table-column>
                <el-table-column label="提交时间" prop="submission_time" width="90px"></el-table-column>
                <el-table-column label="预计上线时间" prop="online_time" width="100px"></el-table-column>
                <el-table-column label="操作" width="200">
                    <template slot-scope="scope">
                        <el-tooltip content="查看日报" placement="top" :enterable="false" effect="light">
                            <el-button type="primary"
                                       icon="el-icon-view"
                                       size="mini"
                                       round
                                       @click="showAllReport(scope.row.id)">

                            </el-button>
                        </el-tooltip>
                        <el-tooltip content="编辑此行" placement="top" :enterable="false" effect="light">
                            <el-button type="primary"
                                       icon="el-icon-edit"
                                       size="mini"
                                       round
                                       @click="showEditProject(scope.row.id)">

                            </el-button>
                        </el-tooltip>
                        <el-tooltip content="删除此行" placement="top" :enterable="false" effect="light">
                            <el-button type="primary"
                                       icon="el-icon-delete"
                                       size="mini"
                                       round
                                       @click="removeProject(scope.row.id)">

                            </el-button>
                        </el-tooltip>
                    </template>
                </el-table-column>
            </el-table>
            <!-- 分页 -->
            <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="queryInfo.pageNum"
                    :page-sizes="[5, 10, 25, 50]"
                    :page-size="queryInfo.pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
            </el-pagination>
            <!-- 对话框-查看本项目下所有日报 -->
            <el-dialog title="详细日报" :visible.sync="showAllReportVisible" width="60%"
                       @close="showAllReportVisibleClosed"
            style="text-align: center">
                <el-card>
                <el-table :data="workReportList" border stripe>
                    <el-table-column label="ID" type="index"></el-table-column>
                    <el-table-column label="项目名称" prop="project_name" width="160px"></el-table-column>
                    <el-table-column label="测试负责人" prop="test_master" width="90px"></el-table-column>
                    <el-table-column label="测试参与人" prop="tester" width="90px"></el-table-column>
                    <el-table-column label="工作内容" prop="today_work"></el-table-column>
                    <el-table-column label="提交问题" prop="today_problem"></el-table-column>
                    <el-table-column label="阻塞问题" prop="urgent_problem"></el-table-column>
                </el-table>
                </el-card>
            </el-dialog>

            <!-- 对话框-修改项目 -->
            <el-dialog title="修改项目" :visible.sync="editProjectVisible" @close="editProjectVisibleClosed" width="550px"
            style="text-align: center">
                <el-form :model="getEditForm" :rules="editProjectRules" ref="editProjectRef" label-width="140px"
                style="width: 500px">

                    <el-form-item label="项目名称" prop="project_name">
                        <el-input v-model="getEditForm.project_name" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="测试类型" prop="test_type">
                        <el-select v-model="getEditForm.test_type" placeholder="请选择测试类型">
                            <el-option label="系统测试" value="系统测试"></el-option>
                            <el-option label="数据测试" value="数据测试"></el-option>
                            <el-option label="模板测试" value="模板测试"></el-option>
                            <el-option label="页面测试" value="页面测试"></el-option>
                            <el-option label="接口测试" value="接口测试"></el-option>
                            <el-option label="性能测试" value="性能测试"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="测试状态" prop="test_state">
                        <el-select v-model="getEditForm.test_state" placeholder="请选择测试状态">
                            <el-option label="测试中" value="测试中"></el-option>
                            <el-option label="测试完成" value="测试完成"></el-option>
                            <el-option label="测试停滞" value="测试停滞"></el-option>
                            <el-option label="未开始" value="未开始"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="测试负责人" prop="test_master">
                        <el-input v-model="getEditForm.test_master" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="测试参与人" prop="tester">
                        <el-input v-model="getEditForm.tester" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="开发负责人" prop="development_manager">
                        <el-input v-model="getEditForm.development_manager" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="开发提交时间" prop="submission_time">
                        <el-date-picker
                                v-model="getEditForm.submission_time"
                                type="date"
                                placeholder="请选择提交时间">
                        </el-date-picker>
                    </el-form-item>

                    <el-form-item label="预期上线时间" prop="online_time">
                        <el-date-picker
                                v-model="getEditForm.online_time"
                                type="date"
                                placeholder="请选择上线时间">
                        </el-date-picker>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer" style="margin-top: -40px">
                    <el-button @click="editProjectVisible = false">取 消</el-button>
                    <el-button type="primary" @click="updateProject">确 定</el-button>
                </div>
            </el-dialog>

        </el-card>
    </div>
</template>

<script>
    export default {
        name: "allProject",
        data() {
            return {
                //获取项目列表参数
                queryInfo: {
                    userName: window.sessionStorage.getItem('user'),
                    query: null,
                    pageNum: 1,
                    pageSize: 5,
                },
                workProjectList: [],
                workReportList: [],
                total: 0,

                //控制详细项目的对话框显示
                showAllReportVisible: false,
                // 控制修改报表的显示
                editProjectVisible: false,
                // 获取待编辑的项目内容
                getEditForm:{},
                //新增日报的验证规则
                editProjectRules: {
                    project_name : [
                        { required: true, message: '请输入项目名称', trigger: 'blur'},
                        {min:1, max:50, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    test_type : [
                        { required: true, message: '请选择测试类型', trigger: 'change'},
                    ],
                    test_state : [
                        { required: true, message: '请选择测试状态', trigger: 'change'},
                    ],
                    test_master : [
                        { required: true, message: '请输入测试负责人', trigger: 'blur'},
                        {min:1, max:50, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    tester : [
                    ],
                    development_manager : [
                    ],
                    submission_time : [
                        { required: true, message: '请选择开发提交日期'},
                    ],
                    online_time : [
                        { required: true, message: '请选择预期上线日期'},
                    ],
                },
                loading: true
            }
        },
        created() {
            this.getProject()
        },
        methods: {
            async getProject() {
                const {data: res} = await this.$http.get('work/show_project/', {params: this.queryInfo})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                this.workProjectList = res.data.workProjectList
                this.total = res.data.total
                this.loading=false
                // console.log(res)
            },
            // 配置标签方法
            formatter(row, column) {
                return row.address;
            },
            filterTag(value, row) {
                return row.test_state === value;
            },
            // 监听分页数改变的事件
            handleSizeChange(newSize) {
                //console.log(newSize)
                this.queryInfo.pageSize = newSize
                this.getProject()
            },
            // 监听页码 变化的事件
            handleCurrentChange(newPage) {
                //console.log(newPage)
                this.queryInfo.pageNum = newPage
                this.getProject()
            },
            // 监听对话框关闭并重置
            showAllReportVisibleClosed() {
                this.workReportList = []
            },
            editProjectVisibleClosed() {
                //this.$refs.addWorkProjectRef.resetFields()
                this.$refs.editProjectRef.resetFields()
            },
            //获取需要修改的内容
            async showEditProject(id) {
                //console.log(id)
                const check = {'id': id}
                const {data: res} = await this.$http.get('work/get_edit_project/', {params: check})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                // console.log(res)
                this.getEditForm = res.data.edit_project
                // console.log(this.getEditForm)
                this.editProjectVisible = true
            },
            //提交更新日报
            updateProject() {
                this.$refs.editProjectRef.validate(async valid => {
                    if (!valid) return
                    const editFrom = {
                        'project_name': this.getEditForm.project_name,
                        'test_type': this.getEditForm.test_type,
                        'test_state': this.getEditForm.test_state,
                        'test_master': this.getEditForm.test_master,
                        'tester': this.getEditForm.tester,
                        'development_manager': this.getEditForm.development_manager,
                        'submission_time': this.getEditForm.submission_time,
                        'online_time': this.getEditForm.online_time,
                        'id': this.getEditForm.id
                    }
                    const {data: res} = await this.$http.post('work/update_project/', editFrom)
                    if (res.meta.status !== 200) {
                        return this.$message.error(res.meta.msg)
                    }
                    this.editProjectVisible = false
                    this.$message.success('更新日报成功！')
                    this.getProject()
                })
            },
            // 根据ID获取相关的工作日报
            async showAllReport(id) {
                const check_id = {'id': id}
                const {data: res} = await this.$http.get('work/show_under_project/', {params: check_id})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                this.workReportList = res.data.workReportList
                this.showAllReportVisible = true
            },
            //根据id删除此行
            async removeProject(id) {
                const delParams = {'id': id,
                }
                const res = await this.$confirm('此操作会永久删除该记录，是否继续？', '提示',
                    {
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning'
                    }).catch(err => err)
                //如果确认删除会返回  confirm
                //如果取消删除会返回  cancel
                // console.log(res)
                if (res !== 'confirm') {
                    return this.$message.info('已取消删除')
                }
                const {data: response} = await this.$http.get('work/delete_project/', {params: delParams})
                if (response.meta.status !== 200) {
                    return this.$message.error(response.meta.msg)
                }
                this.$message.success('删除项目成功')
                this.getProject()
            }

        }
    }
</script>

<style scoped>

</style>
