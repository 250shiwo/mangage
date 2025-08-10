<template>
    <div>
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
                    <el-tag type="success" disable-transitions>{{ user.role_id == 1 ? "管理员" : (user.role_id == 2 ? "教师"
                        :
                        "学生") }}</el-tag>
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
        <div style="width: 100%;">
            <div style="margin: 30px 0; font-weight: bold; font-size:22px; text-align: center;"><span style="color: #dc3545;">系统公告</span>
            </div>
            <el-collapse v-model="activeName" accordion>
                <el-collapse-item v-for="item in tableData" :title="item.name" :name="item.id">
                    <div style="color:#246B69;">{{ item.content }}</div>
                </el-collapse-item>
            </el-collapse>
        </div>
    </div>
</template>

<script>
import DateUtils from "./DateUtils";
export default {
    name: "Hinfo",
    components: { DateUtils },
    data() {
        return {
            user: {},
            activeName:"",
            tableData:[]
        }
    },
    computed: {
    },
    mounted(){
        this.findNotice();
    },
    methods: {
        findNotice(){
            //发起post请求
            this.axios.post('/api/notice').then(res => {
                if (res && res.data.code == 200) {
                    this.tableData = res.data.data
                } else {
                    console.log('获取数据失败')
                }
            })
        },
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