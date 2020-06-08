<template>
    <div>
        <!-- 面包屑-->
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>接口测试</el-breadcrumb-item>
            <el-breadcrumb-item>接口项目</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row :gutter="20">
                <el-col :span="6">
                    <el-input placeholder="请输入项目关键字" v-model="queryInfo.query" clearable @clear="getProject">
                        <el-button slot="append" icon="el-icon-search" @click="getProject"></el-button>
                    </el-input>
                </el-col>

                <el-col :span="6">
                    <el-button type="primary" @click="addProjectVisible=true" round>新增项目</el-button>
                    <el-button type="success" round disabled>新增用例</el-button>
                </el-col>
            </el-row>
        </el-card>
        <el-card>
            <!-- 表单区域 -->

            <el-table :data="ProjectList" border stripe v-loading="loading">
                <el-table-column label="ID" type="index"></el-table-column>
                <el-table-column label="项目名称" prop="name" width="200"></el-table-column>
                <el-table-column label="负责人" prop="tester" width="90"></el-table-column>
                <el-table-column label="环境模式" prop="virtualenv"
                                 width="100"
                                 :filters="[{ text: '测试环境', value: '测试环境' },
                                 { text: '线上环境', value: '线上环境' },
                                  {text: '备用环境', value: '备用环境' },]"
                                 :filter-method="filterTag"
                                 filter-placement="bottom-end">
                    <template slot-scope="scope">
                        <el-tag :type="scope.row.virtualenv === '测试环境' ? 'primary' :
                                scope.row.virtualenv === '线上环境'? 'success':
                                scope.row.virtualenv === '备用环境'? 'danger':'warning'"
                                close-transition>{{scope.row.virtualenv}}
                        </el-tag>
                    </template>
                </el-table-column>
                <el-table-column label="公共HOST" prop="host" width="250"></el-table-column>
                <el-table-column label="公共请求头" prop="com_header"></el-table-column>
                <el-table-column label="操作" width="200">
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
                    :page-sizes="[10, 25, 50, 100]"
                    :page-size="queryInfo.pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="total">
            </el-pagination>
            <!-- 对话框-新增项目 -->
            <el-dialog title="新增接口测试项目" :visible.sync="addProjectVisible" @close="addDialogClosed"
                       style="text-align: center"
                       width="550px">
                <el-form :model="addProjectForm" :rules="addProjectFormRules" ref="addProjectRef"
                         label-width="140px"
                         style="width: 500px">

                    <el-form-item label="项目名称" prop="name">
                        <el-input v-model="addProjectForm.name" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="负责人" prop="tester">
                        <el-select v-model="addProjectForm.tester"
                                   placeholder="请选择负责人">
                            <el-option
                                    v-for="value in userList"
                                    :key="value.id"
                                    :label="value.name"
                                    :value="value.name">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="环境模式" prop="virtualenv">
                        <el-select v-model="addProjectForm.virtualenv" placeholder="请选择环境模式">
                            <el-option label="测试环境" value="测试环境"></el-option>
                            <el-option label="线上环境" value="线上环境"></el-option>
                            <el-option label="备用环境" value="备用环境"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="HOST" prop="host">
                        <el-input v-model="addProjectForm.host" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="公共请求头" prop="com_header">
                        <el-input v-model="addProjectForm.com_header" style="width: 225px"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer" style="margin-top: -40px">
                    <el-button @click="addProjectVisible = false">取 消</el-button>
                    <el-button type="primary" @click="addProjectCheck">确 定</el-button>
                </div>
            </el-dialog>
            <!-- 对话框-修改项目 -->
            <el-dialog title="修改项目" :visible.sync="editProjectVisible" @close="editProjectVisibleClosed"
                       style="text-align: center"
                       width="600px">
                <el-form :model="getEditForm" :rules="editProjectRules" ref="editProjectRef" label-width="150px"
                         style="width: 550px"
                         >

                    <el-form-item label="项目名称" prop="name">
                        <el-input v-model="getEditForm.name" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="负责人" prop="tester">
                        <el-select v-model="getEditForm.tester"
                                   placeholder="请选择负责人">
                            <el-option
                                    v-for="value in userList"
                                    :key="value.id"
                                    :label="value.name"
                                    :value="value.name">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="环境模式" prop="virtualenv">
                        <el-select v-model="getEditForm.virtualenv" placeholder="请选择环境模式">
                            <el-option label="测试环境" value="测试环境"></el-option>
                            <el-option label="线上环境" value="线上环境"></el-option>
                            <el-option label="备用环境" value="备用环境"></el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item label="HOST" prop="host">
                        <el-input v-model="getEditForm.host" style="width: 225px"></el-input>
                    </el-form-item>

                    <el-form-item label="公共参数" prop="com_header">
                        <el-input v-model="getEditForm.com_header" type="textarea"
                                  :autosize="{ minRows: 2, maxRows: 4}"
                                  style="width: 225px"></el-input>
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
        name: "interfaceProject",
        data() {
            return {
                //获取项目列表参数
                queryInfo: {
                    query: null,
                    page_num: 1,
                    page_size: 10,
                },
                // 默认获测试项目列表
                ProjectList: [],
                // select需要的数据-新增项目
                userList: [],
                // 测试用例的接受列表
                caseList: [],
                // 接口项目修改表单
                getEditForm: {},

                total: 0,

                //控制新增项目对话框显示
                addProjectVisible: false,
                // 控制查看用例的显示
                checkCaseVisible: false,
                // 控制修改接口项目的显示
                editProjectVisible: false,

                //新增接口项目表单
                addProjectForm: {
                    operator: window.sessionStorage.getItem('user'),
                    name: null,
                    tester: null,
                    virtualenv: null,
                    host: null,
                    com_header: null
                },
                //新增接口项目的验证规则
                addProjectFormRules: {
                    name : [
                        { required: true, message: '请输入项目名称', trigger: 'blur'},
                        {min:1, max:50, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    tester : [
                        { required: true, message: '请选择负责人', trigger: 'change'},
                    ],
                    virtualenv : [
                        { required: true, message: '请选择环境模式', trigger: 'change'},
                    ],
                    host : [
                        { required: true, message: '请输入基础网址', trigger: 'blur'},
                        {min:1, max:255, message: '基础网站长度需要大于1', trigger: 'blur'}
                    ],
                    com_header: [
                    ]
                },

                // 修改接口项目的验证规则
                editProjectRules: {
                    name : [
                        { required: true, message: '请输入项目名称', trigger: 'blur'},
                        {min:1, max:50, message: '项目名称长度需要大于1或者小于50', trigger: 'blur'}
                    ],
                    tester : [
                        { required: true, message: '请选择负责人', trigger: 'change'},
                    ],
                    virtualenv : [
                        { required: true, message: '请选择环境模式', trigger: 'change'},
                    ],
                    host : [
                        { required: true, message: '请输入基础网址', trigger: 'blur'},
                        {min:1, max:255, message: '基础网站长度需要大于1', trigger: 'blur'}
                    ],
                    com_header: [
                    ]
                },
                loading:true
            }
        },
        created() {
            this.getProject()
        },
        methods: {
            async getProject() {
                const {data: res} = await this.$http.get('interface/get_interface_project/', {params: this.queryInfo})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                this.ProjectList = res.data.project_list
                this.userList = res.data.choice_list
                this.total = res.data.total
                this.loading=false
                // console.log(res)
            },
            // 配置标签方法
            filterTag(value, row) {
                return row.virtualenv === value;
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
            // 监听新增项目对话框关闭并重置
            addDialogClosed() {
                this.$refs.addProjectRef.resetFields()
            },
            // 监听修改接口项目对话框关闭
            editProjectVisibleClosed() {
                this.$refs.editProjectRef.resetFields()
            },
            // 提交新增项目表单
            async addProjectCheck() {
                const {data: res} = await this.$http.post('interface/create_interface_project/', this.addProjectForm)
                if (res.meta.status !== 201) {
                    return this.$message.error(res.meta.msg)
                }
                this.$message.success(res.meta.msg)
                this.addProjectVisible = false
                this.getProject()

            },

            //获取需要修改的内容
            async showEditProject(id) {
                //console.log(id)
                const check = {'id': id}
                const {data: res} = await this.$http.get('interface/ready_to_edit_project/', {params: check})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                // console.log(res)
                this.getEditForm = res.data.get_edit_project
                // console.log(this.getEditForm)
                this.editProjectVisible = true
            },
            //提交更新接口项目
            updateProject() {
                this.$refs.editProjectRef.validate(async valid => {
                    if (!valid) return
                    const thisForm = {
                        operator: window.sessionStorage.getItem('user'),
                        id: this.getEditForm.id,
                        name: this.getEditForm.name,
                        tester: this.getEditForm.tester,
                        virtualenv: this.getEditForm.virtualenv,
                        host: this.getEditForm.host,
                        com_header: this.getEditForm.com_header

                    }
                    const {data: res} = await this.$http.post('interface/update_project/', thisForm)
                    if (res.meta.status !== 201) {
                        return this.$message.error(res.meta.msg)
                    }
                    this.editProjectVisible = false
                    this.$message.success(res.meta.msg)
                    this.getProject()
                })
            },
            // 根据ID获取相关的工作日报
            async showAllReport(id) {
                const check_id = {'id': id}
                const {data: res} = await this.$http.get('show_under_project/', {params: check_id})
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                this.workReportList = res.data.workReportList
                this.showAllReportVisible = true
            },
            //根据id删除此行
            async removeProject(id) {
                const delParams = {'id': id,
                    'user': window.sessionStorage.getItem('user'),
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
                const {data: response} = await this.$http.get('interface/delete_project/', {params: delParams})
                if (response.meta.status !== 201) {
                    return this.$message.error(response.meta.msg)
                }
                this.$message.success(response.meta.msg)
                this.getProject()
            }

        }
    }
</script>

<style scoped>

</style>
