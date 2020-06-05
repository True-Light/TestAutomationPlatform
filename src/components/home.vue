<template>
        <el-container class="home-container">
            <el-header>
                <div>
                    <img src="../assets/logo.png" alt="">
                    <span>自动化测试</span>
                </div>
                <div style="margin-right: -60%">
                    <el-dropdown @command="handleCommand">
                          <span class="el-dropdown-link">
                            {{userName}}<i class="el-icon-arrow-down el-icon--right"></i>
                          </span>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item disabled>个人中心</el-dropdown-item>
                            <el-dropdown-item disabled>未读消息</el-dropdown-item>
                            <el-dropdown-item disabled>后台任务</el-dropdown-item>
                            <el-dropdown-item command="a">退出登陆</el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </div>
                <el-button type="info" size="mini">
                标准位
                </el-button>
            </el-header>
            <el-container>
                <!-- 侧边栏 -->
                <el-aside :width="isCollapse ? '64px' : '200px'">
                    <div class="toggle-button" @click="toggleCollapse"><i class="iconfont icon-moshi"></i></div>
                    <el-menu background-color="#022053" text-color="#fff" active-text-color="#ffd04b"
                             :unique-opened="true" :collapse="isCollapse" :collapse-transition="false"
                    :router="true">

                        <el-menu-item index="welcome">
                            <i class="iconfont icon-tongjifenxi"></i>
                            <span slot="title">数据面板</span>
                        </el-menu-item>

                        <!-- 一级菜单 -->
                        <el-submenu :index="item.id + ''" v-for="item in menuList" :key="item.id">
                            <!-- 一级菜单模板区域 -->
                            <template slot="title">
                                <!-- 图标 -->
                                <i :class="iconsObj[item.id]"></i>
                                <!-- 文本 -->
                                <span>{{ item.auth }}</span>
                                <!-- 二级菜单 -->
                            </template>
                                <el-menu-item :index="subItem.path" v-for="subItem in item.children" :key="subItem.id">

                                    <!-- 图标 -->
                                    <i class="iconfont icon-leixing"></i>
                                    <!-- 文本 -->
                                    <span @click="openFullScreen">{{ subItem.auth}}</span>
                                </el-menu-item>
                        </el-submenu>
                        <el-menu-item index="sysConfig" >
                            <i class="iconfont icon-shezhi_huaban1"></i>
                            <span slot="title">系统配置</span>
                        </el-menu-item>

                    </el-menu>
                </el-aside>
                <!-- 内容区域 -->
                <el-main>
                    <!-- 路由占位符 -->
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
</template>

<script>
    export default {
        name: "home",
        data() {
            return {
                userName: window.sessionStorage.getItem('user'),
                menuList: [],
                iconsObj :{
                    '2': 'iconfont icon-wodedaiban',
                    '3': 'iconfont icon-jinduchakan',
                    '4': 'iconfont icon-jianlibaogaobianji',
                    '5': 'iconfont icon-biangengjilu',
                    '6': 'iconfont icon-anquanyinhuanbaogaoguanli',
                },
                isCollapse: false
            }
        },
        created() {
            this.getMenuList()
        },
        methods: {
            handleCommand(command) {
                if (command === 'a'){
                window.sessionStorage.clear();
                this.$router.push('/login');
                }
            },
            //获取所有菜单
            async getMenuList() {
                var username = window.sessionStorage.getItem('user')
                //var token = window.sessionStorage.getItem('token')
                //console.log(username)
                var user_name = {'userName': username}
                const { data: res} = await this.$http.get('work/menu/', {params: user_name})
                if (res.meta.status !== 200) return this.$message.error(res.meta.msg)
                this.menuList = res.data
                //console.log(res)
            },
            // 配置折叠菜单
            toggleCollapse() {
                this.isCollapse = ! this.isCollapse
            },
            openFullScreen() {
                const loading = this.$loading({
                    lock: true,
                    text: 'Loading',
                    spinner: 'el-icon-loading',
                    background: 'rgba(0, 0, 0, 0.7)'
                });
                setTimeout(() => {
                    loading.close();
                }, 800);
            }
        }

    }
</script>

<style lang="less" scoped>
    .home-container {
        height: 100%;
    }
    .el-header {
        background-color: #ffffff;
        display: flex;
        justify-content: space-between;
        padding-left: 0;
        align-items: center;
        color: #528ce2;
        font-size: 20px;
        > div {
            display: flex;
            align-items: center;
            span {
                margin-left: 15px;
            }
        }
    }

    .el-aside {
        background-color: #022053;
        color: #333;
        text-align: left;
        line-height: 200px;
        .el-menu {
            border-right: none;
        }
    }

    .el-main {
        background-color: #eceef1;
        color: #333;
        text-align: center;
        line-height: 160px;
    }

    body > .el-container {
        margin-bottom: 40px;
    }

    .el-container:nth-child(5) .el-aside,
    .el-container:nth-child(6) .el-aside {
        line-height: 260px;
    }

    .el-container:nth-child(7) .el-aside {
        line-height: 320px;
    }
    .iconfont {
        margin-right: 15px;
        //display: inline-block;
    }
    .toggle-button {
        background-color: #032766;
        font-size: 10px;
        line-height: 24px;
        color: white;
        text-align: center;
        letter-spacing: 0.2em;
        cursor: pointer;
    }
</style>
