<template>
    <div>
        <el-backtop style="position: center"></el-backtop>

        <div>
            <!-- 面包屑-->
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>接口测试</el-breadcrumb-item>
                <el-breadcrumb-item>接口用例</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <!-- 新增用例区域 -->
        <el-card>
            <el-form ref="createCaseRef" :model="createCaseForm" :rules="createCaseRules">
                <el-row>
                    <el-col :span="5">
                        <el-form-item label="接口项目" prop="project_id">
                            <el-select v-model="createCaseForm.project_id" placeholder="请选择项目" @change="getSelected">
                                <el-option v-for="item in projectList" :key="item.id" :label="item.name" :value="item.id">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item style="margin-left: -30px">
                            <el-input placeholder="http://0.0.0.0:80" v-model="host" :disabled="true">
                                <template slot="prepend">HOST:</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item style="margin-left: 10px" prop="case_name">
                            <el-input placeholder="请输入用例名称" v-model="createCaseForm.test_case.case_name" clearable>
                                <template slot="prepend">用例名称:</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6" style="margin-left: 10px">
                        <el-button type="primary" @click="createTestCase">
                            提交用例
                        </el-button>
                    </el-col>
                </el-row>
                <!-- 动态输入框-->
                <el-card>
                    <div v-for="(item, index) in createCaseForm.test_step" :key="index">
                        <el-row>
                            <el-col :span="3">
                                <el-form-item>
                                    <el-input v-model="item.num" clearable :value="index" disabled>
                                        <template slot="prepend">序号:</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item style="margin-left: 10px"
                                              :prop="'test_step.' + index + '.name'"
                                              :rules="{ required: true, message: '请输入步骤名称', trigger: 'blur'}">
                                    <el-input v-model="item.name" clearable>
                                        <template slot="prepend">步骤名称:</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item style="margin-left: 10px">
                                    <el-input v-model="item.desc" clearable>
                                        <template slot="prepend">步骤描述:</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="前置函数" style="margin-left: 10px;border: 1px solid cornflowerblue">
                                <el-switch
                                  style="display: block; margin-left: 13px; margin-top: 8px"
                                  v-model="item.set_up"
                                  active-color="#13ce66"
                                  inactive-color="#ff4949"
                                  active-text="打开"
                                  inactive-text="关闭"
                                  active-value= 1
                                  inactive-value= 0>
                                </el-switch>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="后置函数" style="margin-left: 10px;border:1px solid cornflowerblue ">
                                    <el-switch
                                      style="display: block; margin-left: 13px; margin-top: 8px"
                                      v-model="item.tear_down"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949"
                                      active-text="打开"
                                      inactive-text="关闭"
                                      active-value= 1
                                      inactive-value= 0>
                                    </el-switch>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="3">
                                <el-form-item label="请求方式" :prop="'test_step.' + index + '.method'"
                                              :rules="{ required: true, message: '请选择请求方式', trigger: 'change'}">
                                    <el-select v-model="item.method" placeholder="请选择" style="width: 120px">
                                        <el-option label="GET" value="GET"></el-option>
                                        <el-option label="POST" value="POST"></el-option>
                                        <el-option label="PUT" value="PUT"></el-option>
                                        <el-option label="DELETE" value="DELETE"></el-option>
                                    </el-select>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item style="margin-left: 10px" :prop="'test_step.' + index + '.url'"
                                              :rules="{ required: true, message: '请输入路径', trigger: 'blur'}">
                                    <el-input v-model="item.url" clearable>
                                        <template slot="prepend">PATH</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item style="margin-left: 10px" :prop="'test_step.' + index + '.variable'"
                                              :rules="{ required: true, message: '请输入变量,格式:$variable$ $variable$ $variable$', trigger: 'blur'}">
                                    <el-input v-model="item.variable" clearable>
                                        <template slot="prepend">变量</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="启用断言" style="margin-left: 10px">
                                    <el-switch
                                      style="display: block; margin-left: 13px; margin-top: 8px"
                                      v-model="item.need_assert"
                                      active-color="#13ce66"
                                      inactive-color="#ff4949"
                                      active-text="打开"
                                      inactive-text="关闭"
                                      active-value= 1
                                      inactive-value= 0>
                                    </el-switch>
                                </el-form-item>
                            </el-col>
                            <el-col :span="2">
                                <el-button @click="deleteItem(item, index)" type="danger" round
                                           size="mini" style="margin-left: 20px">
                                    删除该步骤
                                </el-button>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-col :span="13">
                                <el-card>
                                    <el-tabs type="card">
                                        <el-tab-pane label="请求头部" name="first">
                                            <el-form-item label="请求头部">
                                                <el-input type="textarea" v-model="item.headers"
                                                          :autosize="{ minRows: 2, maxRows: 6}" clearable>
                                                </el-input>
                                            </el-form-item>
                                        </el-tab-pane>
                                        <el-tab-pane label="携带参数" name="second">
                                            <el-form-item label="携带参数">
                                                <el-input type="textarea" v-model="item.params"
                                                          :autosize="{ minRows: 2, maxRows: 6}" clearable>
                                                </el-input>
                                            </el-form-item>
                                        </el-tab-pane>
                                        <el-tab-pane label="参数体(DATA-FORM)" name="third">
                                            <el-form-item label="参数体(DATA-FORM)">
                                                <el-input type="textarea" v-model="item.form_data"
                                                          :autosize="{ minRows: 2, maxRows: 6}" clearable>
                                                </el-input>
                                            </el-form-item>
                                        </el-tab-pane>
                                        <el-tab-pane label="参数体(JSON-DATA)" name="fourth">
                                            <el-form-item label="参数体(JSON-DATA)">
                                                <el-input type="textarea" v-model="item.json_data"
                                                          :autosize="{ minRows: 2, maxRows: 6}" clearable>
                                                </el-input>
                                            </el-form-item>
                                        </el-tab-pane>
                                        <el-tab-pane label="预期响应码" name="five">
                                            <el-form-item label="预期响应码" :prop="'test_step.' + index + 'exp_statue'">
                                                <el-input v-model="item.exp_statue" clearable>
                                                </el-input>
                                            </el-form-item>
                                        </el-tab-pane>
                                        <el-tab-pane label="预期响应内容" name="six">
                                            <el-form-item label="预期响应内容">
                                                <el-input type="textarea" v-model="item.exp_extract"
                                                          :autosize="{ minRows: 2, maxRows: 6}" clearableclearable>
                                                </el-input>
                                            </el-form-item>
                                        </el-tab-pane>
                                    </el-tabs>
                                </el-card>
                            </el-col>
                            <el-col :span="8">
                                <el-card class="box-card" style="margin-left: 10px; height: 210px">
                                    <div slot="header" class="clearfix">
                                        <span>服务器返回内容</span>
                                    </div>
                                    <div v-model="response" class="text item">
                                        {{response}}
                                    </div>
                                </el-card>
                            </el-col>
                        </el-row>
                        <el-row>
                            <div>
                                <el-divider content-position="left" style="color: #528ce2"> 分割线</el-divider>
                            </div>
                        </el-row>
                    </div>
                    <el-button @click="addItem" type="primary" style="margin-left: 20px">增加下一步</el-button>
                    <el-button type="success" @click="testCase">测试</el-button>
                </el-card>
            </el-form>
        </el-card>
    </div>
</template>

<script>
    export default {
        name: "interfaceCase",
        data() {
            return {
                activeName2: 'first',
                response: '点击测试按钮后获取内容',
                // 项目列表缓存
                projectList: [],
                host: null,
                // 新增用例数据模型
                createCaseForm: {
                    operator: window.sessionStorage.getItem('user'),
                    project_id: null,
                    test_case: {
                        case_name: null,
                        desc: null
                    },
                    test_step: []
                },
                // 表单验证
                createCaseRules: {
                    project_id: [{ required: true, message: '请选择项目', trigger: 'change'}],
                    case_name: [{ required: true, message: '请输入用例名称', trigger: 'blur'}]
                }
            }
        },
        created() {
            this.getCreatePage()
            },
        methods: {

            getSelected(val) {
                for(let i=0;i<this.projectList.length;i++){
                    if(this.projectList[i].id===val){
                        this.host=this.projectList[i].host
                        console.log(this.host)
                    }
                }
            },
            addItem () {
                this.createCaseForm.test_step.push({
                    num: null,
                    name: null
                })
            },
            deleteItem (item, index) {
                this.createCaseForm.test_step.splice(index, 1)
            },
            async getCreatePage() {
                const {data: res} = await this.$http.get('interface/ready_create_case/')
                if (res.meta.status !== 200) {
                    return this.$message.error(res.meta.msg)
                }
                this.projectList = res.data.project_list
                // console.log(res)
            },
            createTestCase() {
                console.log(this.createCaseForm)
            },
            testCase() {
                this.$refs.createCaseRef.validate(async valid => {
                    if (!valid) {
                        return this.$message.error('缺少必填项!')
                    }
                    const {data: res} = this.$http.post('interface/test_step/', this.createCaseForm)
                    console.log(this.createCaseForm)

                })
            }

        }
    }
</script>

<style>
</style>
