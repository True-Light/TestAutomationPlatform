<template>
    <div>
        <!-- 面包屑-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>工作日报</el-breadcrumb-item>
            <el-breadcrumb-item>本日报告</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card style="height: 60px">
            <el-row :gutter="20" style="margin-top: -70px">
                <el-col :span="6">
                    <el-input placeholder="请输入内容" v-model="queryInfo.query" clearable @clear="getWorkReport">
                        <el-button slot="append" icon="el-icon-search" @click="getWorkReport"></el-button>
                    </el-input>
                </el-col>

                <el-col :span="6">
                    <el-popover
                            ref="popover4"
                            placement="right"
                            width="260"
                            trigger="click">
                        <el-button type="primary" @click="addProject=true" round>新增项目</el-button>
                        <el-button type="success" @click="addReport=true" round>新增日报</el-button>
                    </el-popover>
                    <el-button v-popover:popover4 type="danger" round style="margin-left: -30px">选择操作</el-button>
                </el-col>
            </el-row>
        </el-card>
        <el-card>
            <!-- 表单区域 -->

            <el-table :data="workReportList" border stripe v-loading="loading">
                <el-table-column label="ID" type="index"></el-table-column>
                <el-table-column label="项目名称" prop="project_name"></el-table-column>
                <el-table-column label="测试类型" prop="test_type"></el-table-column>
                <el-table-column label="测试状态" prop="test_state"
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
                <el-table-column label="测试负责人" prop="test_master"></el-table-column>
                <el-table-column label="开发负责人" prop="development_manager"></el-table-column>
                <el-table-column label="提交时间" prop="submission_time"></el-table-column>
                <el-table-column label="预计上线时间" prop="online_time"></el-table-column>
                <el-table-column label="今日工作内容" prop="today_work"></el-table-column>
                <el-table-column label="今日提交问题" prop="today_problem"></el-table-column>
                <el-table-column label="影响进度的问题" prop="urgent_problem"></el-table-column>
                <el-table-column label="操作" width="120">
                    <template slot-scope="scope">
                        <el-tooltip content="编辑此行" placement="top" :enterable="false" effect="light">
                            <el-button type="primary"
                                       icon="el-icon-edit"
                                       size="mini"
                                       round
                                       @click="showEditReport(scope.row.id)">

                            </el-button>
                        </el-tooltip>
                        <el-tooltip content="删除此行" placement="top" :enterable="false" effect="light">
                            <el-button type="primary"
                                       icon="el-icon-delete"
                                       size="mini"
                                       round
                                       @click="removeWork(scope.row.id)">

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
            <!-- 对话框-新增项目 -->
            <el-dialog title="新增项目" :visible.sync="addProject" @close="addDialogClosed" width="550px">
                <el-form :model="addProjectForm" :rules="addProjectFormRules" ref="addWorkProjectRef"
                         label-width="140px" label-position="left"
                         style="margin-top: -70px; width: 500px">

                    <el-form-item label="项目名称" prop="projectName">
                        <el-input v-model="addProjectForm.projectName" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="测试类型" prop="testType">
                        <el-select v-model="addProjectForm.testType" placeholder="请选择测试类型">
                            <el-option label="系统测试" value="系统测试"></el-option>
                            <el-option label="数据测试" value="数据测试"></el-option>
                            <el-option label="模板测试" value="模板测试"></el-option>
                            <el-option label="页面测试" value="页面测试"></el-option>
                            <el-option label="接口测试" value="接口测试"></el-option>
                            <el-option label="性能测试" value="性能测试"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="测试状态" prop="testState">
                        <el-select v-model="addProjectForm.testState" placeholder="请选择测试状态">
                            <el-option label="测试中" value="测试中"></el-option>
                            <el-option label="测试完成" value="测试完成"></el-option>
                            <el-option label="测试停滞" value="测试停滞"></el-option>
                            <el-option label="未开始" value="未开始"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="测试负责人" prop="testMaster">
                        <el-input v-model="addProjectForm.testMaster" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="测试参与人" prop="tester">
                        <el-input v-model="addProjectForm.tester" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="开发负责人" prop="devMaster">
                        <el-input v-model="addProjectForm.devMaster" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="开发提交时间" prop="submissionDate">
                        <el-date-picker
                                v-model="addProjectForm.submissionDate"
                                type="date"
                                placeholder="请选择提交时间">
                        </el-date-picker>
                    </el-form-item>

                    <el-form-item label="预期上线时间" prop="onlineDate">
                        <el-date-picker
                                v-model="addProjectForm.onlineDate"
                                type="date"
                                placeholder="请选择上线时间">
                        </el-date-picker>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer" style="margin-top: -70px">
                    <el-button @click="addProject = false">取 消</el-button>
                    <el-button type="primary" @click="addProjectCheck">确 定</el-button>
                </div>
            </el-dialog>
            <!-- 对话框-新增日报 -->
            <el-dialog title="新增日报" :visible.sync="addReport" @close="addDialogClosed2" width="550px">
                <el-form :model="addReportForm" :rules="addReportFormRules" ref="addReportRef" label-width="140px"
                         style="margin-top: -70px; width: 500px">

                    <el-form-item label="测试项目" prop="projectName">
                        <el-select v-model="addReportForm.projectName"
                                   placeholder="请选择测试项目">
                            <el-option
                                    v-for="value in workProjectList"
                                    :key="value.id"
                                    :label="value.project_name"
                                    :value="value.id +',' + value.project_name">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="测试状态" prop="testState">
                        <el-select v-model="addReportForm.testState" placeholder="请选择测试状态">
                            <el-option label="测试中" value="测试中"></el-option>
                            <el-option label="测试完成" value="测试完成"></el-option>
                            <el-option label="测试停滞" value="测试停滞"></el-option>
                            <el-option label="未开始" value="未开始"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="工作内容" prop="todayWork">
                        <el-input type="textarea" v-model="addReportForm.todayWork"></el-input>
                    </el-form-item>

                    <el-form-item label="提交问题" prop="todayProblem">
                        <el-input type="textarea" v-model="addReportForm.todayProblem"></el-input>
                    </el-form-item>

                    <el-form-item label="阻塞进度的问题" prop="urgentProblem">
                        <el-input type="textarea" v-model="addReportForm.urgentProblem"></el-input>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer" style="margin-top: -70px">
                    <el-button @click="addReport = false">取 消</el-button>
                    <el-button type="primary" @click="addReportCheck">确 定</el-button>
                </div>
            </el-dialog>

            <!-- 对话框-修改日报 -->
            <el-dialog title="修改日报" :visible.sync="editReportVisible" @close="addDialogClosed3" width="550px">
                <el-form :model="getEditForm" :rules="editReportRules" ref="editReportRef" label-width="140px"
                         style="margin-top: -70px; width: 500px">

                    <el-form-item label="测试项目" prop="project_name">
                        <el-select v-model="getEditForm.project_name"
                                   placeholder="请选择测试项目">
                            <el-option
                                    v-for="value in editWorkList"
                                    :key="value.id"
                                    :label="value.project_name"
                                    :value="value.project_name">
                            </el-option>
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

                    <el-form-item label="工作内容" prop="today_work">
                        <el-input type="textarea" v-model="getEditForm.today_work"></el-input>
                    </el-form-item>

                    <el-form-item label="提交问题">
                        <el-input type="textarea" v-model="getEditForm.today_problem"></el-input>
                    </el-form-item>

                    <el-form-item label="阻塞进度的问题">
                        <el-input type="textarea" v-model="getEditForm.urgent_problem"></el-input>
                    </el-form-item>

                </el-form>
                <div slot="footer" class="dialog-footer" style="margin-top: -70px">
                    <el-button @click="editReportVisible = false">取 消</el-button>
                    <el-button type="primary" @click="editWorkReport">确 定</el-button>
                </div>
            </el-dialog>

        </el-card>
    </div>
</template>

<script>
    export default {
        name: "todayWork",
        data() {
            return {
                //获取日报列表参数
                queryInfo: {
                    userName: window.sessionStorage.getItem('user'),
                    query: null,
                    pageNum: 1,
                    pageSize: 5,
                },
                workReportList: [],
                workProjectList: [],
                total: 0,
                //控制新增项目的对话框显示
                addProject: false,
                //控制新增日报的对话框显示
                addReport: false,
                // 控制修改报表的显示
                editReportVisible: false,
                //新增项目表单
                addProjectForm: {
                    userName: window.sessionStorage.getItem('user'),
                    projectName: null,
                    testType: null,
                    testState: null,
                    testMaster: null,
                    tester: null,
                    devMaster: null,
                    submissionDate: null,
                    onlineDate: null
                },
                //新增项目的验证规则
                addProjectFormRules: {
                    projectName : [
                        { required: true, message: '请输入项目名称', trigger: 'blur'},
                        {min:1, max:50, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    testType : [
                        { required: true, message: '请选择测试类型', trigger: 'change'},
                    ],
                    testState : [
                        { required: true, message: '请选择测试状态', trigger: 'change'},
                    ],
                    testMaster : [
                        { required: true, message: '请输入测试负责人', trigger: 'blur'},
                        {min:1, max:50, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    tester : [
                    ],
                    devMaster : [
                    ],
                    submissionDate : [
                        { required: true, type: 'date', message: '请选择开发提交日期', trigger: 'change'},
                    ],
                    onlineDate : [
                        { required: true, type: 'date', message: '请选择预期上线日期', trigger: 'change'},
                    ],

                },
                //新增日报表单
                addReportForm: {
                    userName: window.sessionStorage.getItem('user'),
                    projectName: null,
                    testState: null,
                    todayWork: null,
                    todayProblem: null,
                    urgentProblem: null,
                },
                //新增日报的验证规则
                addReportFormRules: {
                    projectName : [
                        { required: true, message: '请输入项目名称', trigger: 'blur'},
                        {min:1, max:120, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    testState : [
                        { required: true, message: '请选择测试状态', trigger: 'change'},
                    ],
                    todayWork : [
                        { required: true, message: '请输入工作内容', trigger: 'blur'},
                        {min:1, message: '内容长度需要大于1', trigger: 'blur'}
                    ],
                    todayProblem : [
                    ],
                    urgentProblem : [
                    ],
                },
                // 获取待编辑的项目内容
                getEditForm:{},
                editWorkList: [],
                //新增日报的验证规则
                editReportRules: {
                    project_name : [
                        { required: true, message: '请输入项目名称', trigger: 'blur'},
                        {min:1, max:120, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    test_state : [
                        { required: true, message: '请选择测试状态', trigger: 'change'},
                    ],
                    today_work : [
                        { required: true, message: '请输入工作内容', trigger: 'blur'},
                        {min:1, message: '内容长度需要大于1', trigger: 'blur'}
                    ],
                },
                loading: true
            }
        },
        created() {
            this.getWorkReport()
        },
        methods: {
            async getWorkReport() {
                const {data: res} = await this.$http.get('work/workReport/', {params: this.queryInfo})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                this.workReportList = res.data.workReportList
                this.workProjectList = res.data.workProjectList
                this.total = res.data.total
                this.loading=false
                //console.log(res)
            },
            // 配置标签方法
            filterTag(value, row) {
                return row.test_state === value;
            },
            // 监听分页数改变的事件
            handleSizeChange(newSize) {
                //console.log(newSize)
                this.queryInfo.pageSize = newSize
                this.getWorkReport()
            },
            // 监听页码 变化的事件
            handleCurrentChange(newPage) {
                //console.log(newPage)
                this.queryInfo.pageNum = newPage
                this.getWorkReport()
            },
            // 监听对话框关闭并重置
            addDialogClosed() {
                this.$refs.addWorkProjectRef.resetFields()
                //this.$refs.addReportRef.resetFields()
            },
            addDialogClosed2() {
                //this.$refs.addWorkProjectRef.resetFields()
                this.$refs.addReportRef.resetFields()
            },
            addDialogClosed3() {
                //this.$refs.addWorkProjectRef.resetFields()
                this.$refs.editReportRef.resetFields()
            },

            // 提交验证
            addProjectCheck() {
                this.$refs.addWorkProjectRef.validate( async valid => {
                    if(!valid) return
                    //console.log(this.addProjectForm)
                    //发起添加请求
                    const {data: res} = await this.$http.post('work/createProject/', this.addProjectForm)
                    //console.log(res)

                    if (res.meta.status !== 201) return this.$message.error(res.meta.msg)
                    this.$message.success('新增项目成功')
                    this.addProject = false
                    // 重新获取列表
                    this.getWorkReport()
                })
            },
            //提交日报
            addReportCheck() {
                this.$refs.addReportRef.validate( async valid => {
                    if(!valid) return
                    //console.log(this.addReportForm)
                    //发起添加请求
                    const {data: res} = await this.$http.post('work/createReport/', this.addReportForm)
                    //console.log(res)
                    if (res.meta.status !== 201) return this.$message.error(res.meta.msg)
                    this.$message.success('新增日报成功')
                    this.addReport = false
                    this.getWorkReport()
                })
            },
            //获取需要修改的内容
            async showEditReport(id) {
                //console.log(id)
                const check = {'id': id,
                    'userName' : window.sessionStorage.getItem('user')
                }
                const {data: res} = await this.$http.get('work/get_edit_report', {params: check})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                // console.log(res)
                this.getEditForm = res.data.editWork
                this.editWorkList = res.data.projectList
                // console.log(this.getEditForm)
                this.editReportVisible = true
            },
            //提交更新日报
            editWorkReport() {
                this.$refs.editReportRef.validate(async valid => {
                    if (!valid) return
                    const editFrom = {
                        'userName': window.sessionStorage.getItem('user'),
                        'project_name': this.getEditForm.project_name,
                        'test_state': this.getEditForm.test_state,
                        'today_work': this.getEditForm.today_work,
                        'today_problem': this.getEditForm.today_problem,
                        'urgent_problem': this.getEditForm.urgent_problem,
                        'id': this.getEditForm.id
                    }
                    const {data: res} = await this.$http.post('work/update_report/', editFrom)
                    if (res.meta.status !== 200) {
                        return this.$message.error(res.meta.msg)
                    }
                    this.editReportVisible = false
                    this.$message.success('更新日报成功！')
                    this.getWorkReport()
                })
            },
            //根据id删除此行
            async removeWork(id) {
                const delParams = {'id': id,
                    'userName' : window.sessionStorage.getItem('user')
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
                const {data: response} = await this.$http.get('work/delete_report/', {params: delParams})
                if (response.meta.status !== 200) {
                    return this.$message.error(response.meta.msg)
                }
                this.$message.success('删除日报成功')
                this.getWorkReport()
            }

        }
    }
</script>

<style scoped>

</style>
