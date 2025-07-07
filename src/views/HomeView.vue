<template>
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
        <span>王小虎</span>
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
        <el-table :data="tableData" :header-cell-style="{background:'#f2f5fc',color:'#555555'}">
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="id" label="ID" width="60" align='center'></el-table-column>
          <el-table-column prop="username" label="用户名" width="100" align='center'></el-table-column>
          <el-table-column prop="sex" label="性别" width="60" align='center'>
            <template slot-scope="scope">
              <el-tag :type="scope.row.sex === 1 ? 'primary' : 'success'" disable-transitions>{{ scope.row.sex === 1 ?
                '男' : '女' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱地址" width="180" align='center'></el-table-column>
          <el-table-column prop="phone" label="联系方式" width="120" align='center'></el-table-column>
          <el-table-column prop="student_id" label="学号" width="120" align='center'></el-table-column>
          <el-table-column prop="college_id" label="学院" width="120" align='center'></el-table-column>
          <el-table-column prop="speciality_id" label="专业" width="120" align='center'></el-table-column>
          <el-table-column label="操作" width="180" align='center'>
            <template slot-scope="scope">
                    <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'Home',
  data() {
    return {
      tableData: [],//记录学生表数据
      isCollapse:false,
      aside_width:'200px',
      icon:'el-icon-s-fold'
    }
  },
  mounted(){
    this.getStudents()
  },
  methods:{
    getStudents(){
      this.axios.get('/students',{}).then(res=>{
        if(res && res.data.code == 200){
          this.tableData=res.data.data
        }else{
          console.log('获取数据失败')
        }
      })
    },
    toUser(){
      console.log('to_user')
    },
    logout(){
      console.log('to_logout')
      // this.$router.push('/');
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
    }
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
