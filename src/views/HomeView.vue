<template>
  <div>
    <!--这是管理员界面-->
    <!--导航栏部分-->
    <el-container style="height: 100%; border: 1px solid #eee">
      <el-aside :width="aside_width" style="background-color: rgb(238, 241, 246);height: 100%;margin-left: -1px;">
        <el-menu background-color="#545c64" text-color="#fff" active-text-color="#ffd04b" default-active="/Home"
          :collapse="isCollapse" :collapse-transition="false" style="height: 100vh; text-align: left;">
          <el-menu-item index="/Home">
            <i class="el-icon-s-home"></i>
            <span slot="title">首页</span>
          </el-menu-item>

          <el-menu-item index="/School">
            <i class="el-icon-school"></i>
            <span slot="title">学院专业管理</span>
          </el-menu-item>

          <el-menu-item index="/User">
            <i class="el-icon-user"></i>
            <span slot="title">用户管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <!--header部分-->
      <el-container style="height: 100%;">
        <el-header
          style="text-align: right; font-size: 12px; display: flex; line-height: 60px;height: 100%; border-bottom: rgba(168, 168, 168, 0.8) 1px solid;">
          <div style="margin-top:8px">
            <i :class="icon" style="font-size: 20px; cursor: pointer;" @click="collapse"></i>
          </div>
          <div style="flex: 1; text-align: center; font-size: 34px;">
            <span>欢迎来到学生请假管理系统</span>
          </div>
          <span>{{ user.username }}</span>
          <el-dropdown>
            <i class="el-icon-arrow-down" style="margin-left: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click.native="toUser">个人中心</el-dropdown-item>
              <el-dropdown-item @click.native="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-header>
        <!--内容部分-->
        <el-main style="height: 100%; width: 100%;">
         <!-- <Student></Student> -->
         <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

// @ is an alias to /src

export default {
  name: 'Home',
  data() {
    return {
      user:JSON.parse(sessionStorage.getItem('CurUser')),
      isCollapse:false,
      aside_width:'200px',
      icon:'el-icon-s-fold',    
    }
  },
  created(){
    this.$router.push("/Hinfo")
  },
  methods:{ 
    toUser(){
      console.log('to_user')
      this.$router.push("Hinfo")
    },
    logout(){
      console.log('to_logout')
      this.$confirm('您确定要退出登录吗?','提示',{
        confirmButtonText:'确定',
        type:'warning',
        center:true,
      })
        .then(()=>{
          this.$message({
            type:'success',
            message:'退出登录成功'
          })
          this.$router.push('/');
          sessionStorage.clear()
        })
        .catch(()=>{
           this.$message({
            type:'info',
            message:'已取消退出登录'
          })
        })
     
    },
    collapse(){
      this.isCollapse = !this.isCollapse
      if(!this.isCollapse){//展开
        this.aside_width='200px'
        this.icon='el-icon-s-fold'
      }else{//收起
        this.aside_width='64px'
        this.icon='el-icon-s-unfold'
      }
    },
  }
}
</script>

<style>
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}
.el-main {
  padding: 5px;
}
.el-aside {
  color: #333;
}
</style>
