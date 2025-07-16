<template>
    <div style="text-align: center;background-color: #f1f1f3;height: 100%;padding: 0px;margin: 0px;">
        <h1 style="font-size: 50px;">{{ '欢迎你！' + user.username }}</h1>
        <el-descriptions title="个人中心" :column="2" size="40" border>
            <el-descriptions-item>
                <template slot="label">
                    <i class="el-icon-s-custom"></i>
                    用户名
                </template>
                {{ user.username }}
            </el-descriptions-item>
             <el-descriptions-item>
                <template slot="label">
                    <i class="el-icon-tickets"></i>
                    角色
                </template>
                <el-tag type="success"
                    disable-transitions>{{ user.role_id == 1 ? "管理员" : (user.role_id == 2 ? "教师" : "学生") }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item>
                <template slot="label">
                    <i class="el-icon-s-promotion"></i>
                    邮箱地址
                </template>
                {{ user.email }}
            </el-descriptions-item>
            <el-descriptions-item>
                <template slot="label">
                    <i class="el-icon-location-outline"></i>
                    IP地址
                </template>
                {{ user.ip }}
            </el-descriptions-item>
        </el-descriptions>

        <DateUtils></DateUtils>
    </div>
</template>

<script>
import DateUtils from "./DateUtils";
export default {
    name: "Hinfo",
    components: { DateUtils },
    data() {
        return {
            user: {}
        }
    },
    computed: {
    },
    methods: {
        init() {
            this.user = JSON.parse(sessionStorage.getItem('CurUser'))
        }
    },
    created() {
        this.init()
    }
}
</script>

<style scoped>
.el-descriptions {
    width: 90%;

    margin: 0 auto;
    text-align: center;
}
</style>