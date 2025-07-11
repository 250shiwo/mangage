<template>
  <div>
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
          <!--搜索-->
          <div style="margin-bottom: 5px;">
            <el-input style="width: 200px;" placeholder="请输入用户名" suffix-icon="el-icon-search" v-model="params.username"
              @keyup.enter.native="postStudents">
            </el-input>
            <el-input style="width: 200px; margin-left: 5px;" placeholder="请输入联系方式" suffix-icon="el-icon-search"
              v-model="params.phone" @keyup.enter.native="postStudents">
            </el-input>
            <el-input style="width: 200px; margin-left: 5px;" placeholder="请输入学号" suffix-icon="el-icon-search"
              v-model="params.student_id" @keyup.enter.native="postStudents">
            </el-input>
            <el-button type="primary" style="margin-left: 5px;" icon="el-icon-search"
              @click="postStudents">搜索</el-button>
            <el-button type="success" style="margin-left: 5px;" icon="el-icon-plus" @click="add">添加</el-button>
          </div>
          <!--数据-->
          <el-table :data="tableData" :header-cell-style="{background:'#f2f5fc',color:'#555555'}">
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column prop="id" label="ID" width="60" align='center'></el-table-column>
            <el-table-column prop="username" label="用户名" width="120" align='center'></el-table-column>
            <el-table-column prop="sex" label="性别" width="120" align='center'>
              <template slot-scope="scope">
                <el-tag :type="scope.row.sex === 1 ? 'primary' : 'success'" disable-transitions>{{ scope.row.sex === 1 ?
                  '男' : '女' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="email" label="邮箱地址" width="180" align='center'></el-table-column>
            <el-table-column prop="phone" label="联系方式" width="180" align='center'></el-table-column>
            <el-table-column prop="student_id" label="学号" width="180" align='center'></el-table-column>
            <el-table-column prop="college_id" label="学院" width="120" align='center'></el-table-column>
            <el-table-column prop="speciality_id" label="专业" width="120" align='center'></el-table-column>
            <el-table-column label="操作" width="180" align='center'>
              <template slot-scope="scope">
                <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination style="text-align: center;" @size-change="handleSizeChange"
            @current-change="handleCurrentChange" :current-page="pageNum" :page-sizes="[5,10]" :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper" :total="total">
          </el-pagination>
          <!--弹窗-->
          <el-dialog :title="title" :visible.sync="centerDialogVisible" width="30%" center>
            <el-form ref="form" :rules="rules" :model="form" label-width="80px" >
              <el-form-item label="姓名" prop="name">
                <el-col :span="20">
                  <el-input v-model="form.name" placeholder="请输入学生姓名"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="用户名" prop="username">
                <el-col :span="20">
                  <el-input v-model="form.username" placeholder="请输入学生用户名"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="性别" prop="sex">
                <el-radio-group v-model="form.sex">
                  <el-radio label="1" >男</el-radio>
                  <el-radio label="2" >女</el-radio>
                </el-radio-group>
              </el-form-item>
              <el-form-item label="邮箱地址" prop="email">
                <el-col :span="20">
                  <el-input v-model="form.email" placeholder="请输入学生邮箱地址"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="联系方式" prop="phone">
                <el-col :span="20">
                  <el-input v-model="form.phone" placeholder="请输入学生联系方式"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="学号" prop="student_id">
                <el-col :span="20">
                  <el-input v-model="form.student_id" placeholder="请输入学生学号"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="学院" prop="college_id">
                <el-col :span="20">
                  <el-input v-model="form.college_id" placeholder="请输入学生学院"></el-input>
                </el-col>
              </el-form-item>
              <el-form-item label="专业" prop="speciality_id">
                <el-col :span="20">
                  <el-input v-model="form.speciality_id" placeholder="请输入学生专业"></el-input>
                </el-col>
              </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
              <el-button @click="centerDialogVisible = false">取 消</el-button>
              <el-button type="primary" @click="save">确 定</el-button>
            </span>
          </el-dialog>
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
      tableData: [],//记录学生表数据
      isCollapse:false,
      aside_width:'200px',
      icon:'el-icon-s-fold',
      pageSize:10,
      pageNum:1,
      total:1,
      //记录搜索条件内容
      params:{
        username:"",
        phone:"",
        student_id:""
      },
      //弹窗标题
      title: "",
      //控制弹窗是否显示
      centerDialogVisible: false,
      //存储弹窗form表单对应的字段
      form:{
        name:'',
        username:'',
        sex:'',
        email:'',
        phone:'',
        student_id:'',
        college_id:'',
        speciality_id:''
      },
      //检查规则
      rules: {
        name: [{ required: true, message: '请输入学生姓名', trigger: 'blur' }],
        username: [{ required: true, message: '请输入学生用户名', trigger: 'blur' }],
        sex: [{ required: true, message: '请选择学生性别', trigger: 'blur' }],
        email: [{ required: true, message: '请输入学生邮箱地址', trigger: 'blur' }],
        phone: [{ required: true, message: '请输入学生联系方式', trigger: 'blur' }],
        student_id: [{ required: true, message: '请输入学生学号', trigger: 'blur' }],
        college_id: [{ required: true, message: '请输入学生学院', trigger: 'blur' }],
        speciality_id: [{ required: true, message: '请输入学生专业', trigger: 'blur' }]
      }
    }
  },
  mounted(){
    this.postStudents()
  },
  methods:{
    resetForm() {
        this.$refs.form.resetFields();
      },
    save(){
      this.$refs.form.validate((valid) => {
        if (valid) {
          //发起post请求
          this.axios.post('/students/save', this.form).then(res => {
            console.log(res)
            if (res && res.data.code == 200) {
              this.$message({
                message: "添加学生成功!",
                type: "success"
              })
              this.centerDialogVisible = false;
              this.postStudents();
            } else {
              console.log('获取数据失败')
              this.$message({
                message: "发生错误,添加学生失败!",
                type: "error"
              })
            }
          })
        } else {
          this.$message({
            message: "请检查输入数据是否完整",
            type: "error"
          })
          return false;
        }
      });

    },
    add(){
      this.title ='添加学生'
      this.centerDialogVisible = true
      this.$nextTick(()=>{
        this.resetForm()
      })
    },
    // getStudents(){
    //   this.axios.get('/students?'+queryParams.toString(),{}).then(res=>{
    //     if(res && res.data.code == 200){
    //       this.tableData=res.data.data
    //     }else{
    //       console.log('获取数据失败')
    //     }
    //   })
    // },
    postStudents(){
      //发起post请求
      this.axios.post('/students/paginated',{
        pageNum:this.pageNum,
        pageSize:this.pageSize,
        params:{
          username:this.params.username,
          phone:this.params.phone,
          student_id:this.params.student_id
        }
      }).then(res=>{
        console.log(res)
        if(res && res.data.code == 200){
          this.tableData=res.data.data
          this.total=res.data.total
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
    },
    handleSizeChange(val) {
      console.log(`每页 ${val} 条`);
      this.pageNum=1
      this.pageSize=val
      this.postStudents()
    },
    handleCurrentChange(val) {
      console.log(`当前页: ${val}`);
      this.pageNum=val
      this.postStudents()
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
