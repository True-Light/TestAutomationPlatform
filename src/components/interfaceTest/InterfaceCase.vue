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
        <el-card v-loading="loading">
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
                        <el-form-item style="margin-left: 10px">
                            <el-input placeholder="请输入用例名称" v-model="createCaseForm.test_case.case_name" clearable>
                                <template slot="prepend">用例名称:</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="6">
                        <el-form-item style="margin-left: 10px">
                            <el-input placeholder="请输入用例描述" v-model="createCaseForm.test_case.case_desc" clearable>
                                <template slot="prepend">用例描述:</template>
                            </el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <!-- 动态输入框-->
                <el-card>
                    <div v-for="(item, index) in createCaseForm.test_step" :key="index">
                        <el-row>
                            <el-col :span="1">
                                <el-form-item v-model="item.step_num=index">
                                    <el-tag>序号:{{index}}</el-tag>
<!--                                    <el-input v-model="item.step_num" clearable :value="index" disabled>-->
<!--                                        <template slot="prepend">序号:</template>-->
<!--                                    </el-input>-->
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item style="margin-left: 10px"
                                              :prop="'test_step.' + index + '.step_name'"
                                              :rules="{ required: true, message: '请输入步骤名称', trigger: 'blur'}">
                                    <el-input v-model="item.step_name" clearable>
                                        <template slot="prepend">步骤名称:</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item style="margin-left: 10px">
                                    <el-input v-model="item.step_desc" clearable>
                                        <template slot="prepend">步骤描述:</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="3">
                                <el-form-item label="前置函数" style="margin-left: 10px">
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
                                <el-form-item label="后置函数" style="margin-left: 10px">
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
                            <el-col :span="4">
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
                                <el-form-item style="margin-left: -40px" :prop="'test_step.' + index + '.url'"
                                              :rules="{ required: true, message: '请输入路径', trigger: 'blur'}">
                                    <el-input v-model="item.url" clearable>
                                        <template slot="prepend">PATH</template>
                                    </el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="6">
                                <el-form-item style="margin-left: 10px">
<!--                                              :prop="'test_step.' + index + '.variable'"-->
<!--                                              :rules="{ required: true, message: '请输入变量,格式:$variable$ $variable$ $variable$', trigger: 'blur'}">-->

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
                                            <el-form-item label="预期响应码" :prop="'test_step.' + index + 'exp_status'">
                                                <el-input v-model="item.exp_status" clearable>
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
                                        <template v-model="res_c">
                                            <el-tag
                                              :type="res_c === false ? 'danger' : 'success'"
                                              disable-transitions>状态码判定:{{res_c}}</el-tag>
                                        </template>
                                        <template v-model="res_r" style="margin-left: 10px">
                                            <el-tag
                                              :type="res_r === false ? 'danger' : 'success'"
                                              disable-transitions>响应内容判定:{{res_r}}</el-tag>
                                        </template>

                                        <el-button style="float: right; padding: 3px 0" type="text"
                                                   @click="drawer = true">
                                            显示更多
                                        </el-button>
                                    </div>
                                    <div v-model="response" class="text item">
                                        {{response}}
                                    </div>
                                </el-card>
                            </el-col>
                            <el-col :span="2">
                                <el-button type="success"
                                           style="margin-left: 20px; margin-top: 20px" round
                                           @click="testCase(index)">
                                    测试
                                </el-button>
                                <el-button @click="deleteItem(item, index)" type="danger" round
                                           style="margin-left: 20px; margin-top: 20px">
                                    删除该步骤
                                </el-button>
                            </el-col>
                        </el-row>
                        <el-row>
                            <div>
                                <el-divider content-position="left" style="color: #528ce2"> 分割线</el-divider>
                            </div>
                        </el-row>
                    </div>
                    <el-button @click="addItem" type="primary" style="margin-left: 20px">增加下一步</el-button>
                        <el-button type="primary" @click="createTestCase">
                            提交用例
                        </el-button>
                </el-card>
            </el-form>
        </el-card>
        <el-drawer
          title="我是标题"
          :visible.sync="drawer"
          :with-header="false">
            <span>{{response}}</span>
        </el-drawer>
    </div>
</template>

<script>
    export default {
        name: "interfaceCase",
        data() {
            return {
                activeName2: 'first',
                response: '点击测试按钮后获取内容',
                drawer: false,
                res_c: false,
                res_r: false,
                // 项目列表缓存
                projectList: [],
                host: null,
                // 新增用例数据模型
                createCaseForm: {
                    operator: window.sessionStorage.getItem('user'),
                    project_id: null,
                    test_case: {
                        case_name: null,
                        case_desc: null
                    },
                    test_step: []
                },
                // 表单验证
                createCaseRules: {
                    project_id: [{ required: true, message: '请选择项目', trigger: 'change'}],
                    case_name: [{ required: true, message: '请输入用例名称', trigger: 'blur'},
                        {min:1, max:255, message: '长度需要大于1或者小于250', trigger: 'blur'}]
                },
                loading: false
            }
        },
        created() {
            this.getCreatePage()
              this.addItem()
            },
        methods: {

            getSelected(val) {
                for(let i=0;i<this.projectList.length;i++){
                    if(this.projectList[i].id===val){
                        this.host=this.projectList[i].host
                        // console.log(this.host)
                    }
                }
            },
            addItem () {
                this.createCaseForm.test_step.push({
                    step_num: null,
                    step_name: null,
                    step_desc: null,
                    set_up: null,
                    tear_down: null,
                    method: null,
                    url: null,
                    variable: null,
                    need_assert: null,
                    assert_method: null,
                    headers: null,
                    params: null,
                    form_data: null,
                    json_data: null,
                    exp_status: null,
                    exp_extract: null
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
                this.$refs.createCaseRef.validate(async valid => {
                    if (!valid) {
                        return this.$message.error('缺少必填项!')
                    }
                    this.loading = true
                    const {data: res} = await this.$http.post('interface/create_case/', this.createCaseForm)
                    if (res.meta.status !== 200) {
                        this.loading = false
                        return this.$message.error(res.meta.msg)
                    }
                    this.getCreatePage()
                    // location.reload()
                    // this.$router.go(0)
                    // window.reload()
                    this.$refs.createCaseRef.resetFields()
                    this.loading = false
                    return this.$message.success(res.meta.msg)

            })
            },
            testCase(index) {
                this.$refs.createCaseRef.validate(async valid => {
                    if (!valid) {
                        return this.$message.error('缺少必填项!')
                    }
                    this.loading = true
                    const testData = {
                        project_id: this.createCaseForm.project_id,
                        host: this.host,
                        step_num: index,
                        step_name: this.createCaseForm.test_step[index].step_name,
                        step_desc: this.createCaseForm.test_step[index].step_desc,
                        set_up: this.createCaseForm.test_step[index].set_up,
                        tear_down: this.createCaseForm.test_step[index].tear_down,
                        url: this.createCaseForm.test_step[index].url,
                        method: this.createCaseForm.test_step[index].method,
                        variable: this.createCaseForm.test_step[index].variable,
                        headers: this.createCaseForm.test_step[index].headers,
                        params: this.createCaseForm.test_step[index].params,
                        form_data: this.createCaseForm.test_step[index].form_data,
                        json_data: this.createCaseForm.test_step[index].json_data,
                        need_assert: this.createCaseForm.test_step[index].need_assert,
                        exp_status: this.createCaseForm.test_step[index].exp_status,
                        exp_extract: this.createCaseForm.test_step[index].exp_extract
                    }
                    const {data: res} = await this.$http.post('interface/to_test_step/', testData)
                    if (res.meta.status !== 200) {
                        this.loading = false
                        return this.$message.error(res.meta.msg)
                    }
                    this.response = res.data
                    this.res_c = res.data.assert.code
                    this.res_r = res.data.assert.response
                    this.loading = false

                })
            }

        }
    }
</script>

<style>
</style>
