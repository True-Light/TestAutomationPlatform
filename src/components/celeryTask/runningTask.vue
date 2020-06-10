<template>
    <div>
        <el-backtop style="position: center"></el-backtop>

        <div>
            <!-- 面包屑-->
            <el-breadcrumb separator-class="el-icon-arrow-right">
                <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item>任务管理</el-breadcrumb-item>
                <el-breadcrumb-item>运行状态</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <!-- 状态区域 -->
        <div>
        </div>

    </div>
</template>

<script>
    export default {
        name: "running_task",
        data() {
            return {
                loading: false,
            }
        },
        created() {
        },
        methods: {

        }
    }
</script>

<style>
</style>
