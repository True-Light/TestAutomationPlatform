<template>
    <div>
        <el-button type="info" @click="logout">
            logout
        </el-button>
    </div>
</template>

<script>
    export default {
        name: "home",
        methods: {
            logout() {
                window.sessionStorage.clear();
                this.$router.push('/login');
            }
        }
    }
</script>

<style scoped>

</style>