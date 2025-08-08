<template>
  <el-card class="info-container">
    <template #header>
      <div class="card-header">
        <span>个人信息</span>
      </div>
    </template>
    <el-form :model="userInfo" label-width="100px" class="info-form">
      <el-form-item label="姓名" v-if="userInfo.role_id !== 1">
        <span>{{ userInfo.name }}</span>
      </el-form-item>
      <el-form-item label="用户名">
        <el-input v-model="userInfo.username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          v-model="userInfo.password"
          show-password
        />
      </el-form-item>
      <el-form-item label="邮箱地址">
        <el-input v-model="userInfo.email" />
      </el-form-item>
      <el-form-item label="性别" v-if="userInfo.role_id !== 1">
        <el-radio-group v-model="userInfo.sex">
          <el-radio :label="1">男</el-radio>
          <el-radio :label="2">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="手机号" v-if="userInfo.role_id !== 1">
        <el-input v-model="userInfo.phone" />
      </el-form-item>
      <el-form-item label="角色:">
        <el-tag>{{ getRoleName(userInfo.role_id) }}</el-tag>
      </el-form-item>
      <el-form-item label="IP地址:">
        <span>{{ userInfo.ip }}</span>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="saveInfo">保存修改</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      userInfo: {},
    }
  },
  methods: {
    getInfo(){
      this.axios.post('/api/user/get_info', this.userInfo).then(res => {
        console.log(res.data.data)
        if (res && res.data.code == 200) {
          Object.assign(this.userInfo, res.data.data)
        }
      })
    },
    saveInfo() {
      this.axios.put('/api/user/update_info',this.userInfo).then(res =>{
        console.log(this.userInfo)
        console.log(res)
        if(res && res.data.code =='200'){
          this.$message({
            message:'修改成功!',
            type:"success"
          });
          this.getInfo()
          sessionStorage.setItem('CurUser', JSON.stringify(this.userInfo))
        }else{
          this.$message({
            message:"缺少修改信息!",
            type:"error"
          })
        }
      });
    },
    init() {
      this.userInfo = JSON.parse(sessionStorage.getItem('CurUser'))
    },
    getRoleName(roleId) {
      switch (roleId) {
        case 1:
          return '管理员'
        case 2:
          return '教师'
        case 3:
          return '学生'
        default:
          return roleId
      }
    }
  },
  created() {
    this.init()
  }
}
</script>

<style scoped>
  .info-container {
    max-width: 800px;
    margin: 20px auto;
  }
  .card-header {
    display: flex;
    justify-content: center;
  }
</style>