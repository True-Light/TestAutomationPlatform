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
                    <el-button type="primary" @click="loginCheck">Login</el-button>
                    <el-button type="info" @click="resetLoginForm">Reset</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
    export default {
        name: "login",
        data(){
            return{
                loginFrom: {
                    username: 'admin',
                    password: '123456'
                },
                loginFromRules: {
                    username:[
                        { required: true, message: '请输入username', trigger: 'blur' },
                        { min: 3, max: 10, message: '长度在 3 到 10 个字符', trigger: 'blur' }
                    ],
                    password:[
                        { required: true, message: '请输入password', trigger: 'blur' },
                        { min: 6, max: 15, message: '长度在 6 到 15 个字符', trigger: 'blur' }
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
                    const {data: res} = await this.$http.post('api/token/', this.loginFrom);
                    // console.log(res.code)
                    if (res.code === -1 ) return this.$message.error('error')
                    this.$message.success('success')
                    window.sessionStorage.setItem('token', res.access)
                    this.$router.push('/home');
                })
            }
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