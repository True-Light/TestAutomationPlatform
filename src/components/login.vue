<template>
    <div class="login_container">
        <div class="login_box">
            <!-- touxiang -->
            <div class="avatar_box">
                <img src="../assets/logo.png">
            </div>
            <!--LOGIN FORM -->
            <el-form label-width="0px" class="login_from" :model="loginFrom" :rules="loginFromRules" ref="loginFormRef">
                <el-form-item prop="username">
                    <el-input prefix-icon="iconfont icon-huiyuan_huaban1" v-model="loginFrom.username">

                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input prefix-icon="iconfont icon-yanzhengma" v-model="loginFrom.password" type="password">

                    </el-input>
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="warning" @click="registeredVisible=true">注册</el-button>
                    <el-button type="primary" @click="loginCheck">登陆</el-button>
                    <el-button type="info" @click="resetLoginForm">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
        <!-- 对话框-注册用户 -->
        <el-dialog title="注册用户" :visible.sync="registeredVisible" @close="registeredVisibleClosed" width="400px">
            <el-form :model="registeredForm" :rules="registeredRules" ref="registeredRef">

                <el-form-item label="输入用户名" prop="username">
                    <el-input v-model="registeredForm.username"></el-input>
                </el-form-item>

                <el-form-item label="输入密码" prop="password">
                    <el-input v-model="registeredForm.password" type="password"></el-input>
                </el-form-item>

                <el-form-item label="再次输入密码" prop="password2">
                    <el-input v-model="registeredForm.password2" type="password"></el-input>
                </el-form-item>


                <el-form-item label="你的名字" prop="name">
                    <el-input v-model="registeredForm.name"></el-input>
                </el-form-item>


            </el-form>
            <div slot="footer" class="dialog-footer" style="margin-top: -30px">
                <el-button @click="registeredVisible = false">取 消</el-button>
                <el-button type="primary" @click="registeredSubmit">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "login",
        data(){
            return{
                loginFrom: {
                    username: '',
                    password: ''
                },
                loginFromRules: {
                    username:[
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
                    ],
                    password:[
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
                    ]
                },
                // 控制注册框显示
                registeredVisible: false,
                // 注册表单
                registeredForm: {
                    username: '',
                    password: '',
                    password2: '',
                    name: ''
                },
                // 注册验证
                registeredRules: {
                    username:[
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
                    ],
                    password:[
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
                    ],
                    password2:[
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
                    ],

                    name:[
                        { required: true, message: '请输入名字', trigger: 'blur' },
                        { min: 2, max: 30, message: '长度在 2 到 30 个字符', trigger: 'blur' }
                    ]

                }
            }
        },
        methods:{
            resetLoginForm(){
                this.$refs.loginFormRef.resetFields();
            },
            loginCheck(){
                this.$refs.loginFormRef.validate(async valid =>{
                    // console.log(valid)
                    if (!valid) return;
                    const submitLoginFrom = {
                        'username': this.loginFrom.username,
                        'password': '123456' + this.loginFrom.password + '.com'
                    }
                    const {data: res} = await this.$http.post('token/', submitLoginFrom);
                    //console.log(res)
                    if (res.status !== 200 ) return this.$message.error(res.msg)
                    this.$message.success('登陆成功')
                    window.sessionStorage.setItem('token', res.access)
                    window.sessionStorage.setItem('user', res.username)
                    await this.$router.push('/home');
                })
            },
            // 监听对话框关闭并重置
            registeredVisibleClosed() {
                this.$refs.registeredRef.resetFields()
            },
            // 提交验证
            registeredSubmit() {
                this.$refs.registeredRef.validate( async valid => {
                    if(!valid) return
                    //console.log(this.addProjectForm)
                    const subForm = {
                        'username': this.registeredForm.username,
                        'password': '123456' + this.registeredForm.password + '.com',
                        'password2': '123456' + this.registeredForm.password2 + '.com',
                        'name': this.registeredForm.name
                    }
                    //发起添加请求
                    const {data: res} = await this.$http.post('registered/', subForm)
                    //console.log(res)
                    if (res.meta.status !== 201) return this.$message.error(res.meta.msg)
                    this.$message.success(res.meta.msg)
                    this.registeredVisible = false
                })
            },
        }
    };
</script>

<style lang="less" scoped>
    .login_container{
        background-color: #53678d;
        height: 100%;
    }
    .login_box{
        width: 450px;
        height: 300px;
        background-color: white;
        border-radius: 3px;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
    }
    .avatar_box{
        height: 130px;
        width: 130px;
        border: 1px solid #eee;
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 0 10px #ddd;
        position: absolute;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #fff;
        img{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-color: #eee;
        }
    }
    .login_from{
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 0 20px;
        box-sizing: border-box;
    }
    .btns{
        display: flex;
        justify-content: flex-end;
    }
</style>
