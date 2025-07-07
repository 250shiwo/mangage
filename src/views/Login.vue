<template>

    <body id="poster">
        <el-form :rules="rules" :model="loginForm" class="login-container" label-position="left" label-width="0px" ref="loginForm">
            <h3 class="login_title">
                系统登录
            </h3>
            <el-form-item label="" prop="username">
                <el-input type="text" v-model="loginForm.username" autocomplete="off" placeholder="账号"></el-input>
            </el-form-item>
            <el-form-item label="" prop="password">
                <el-input type="password" v-model="loginForm.password" autocomplete="off" placeholder="密码"></el-input>
            </el-form-item>
            <el-form-item label="">
                <el-radio-group v-model="loginForm.radio">
                <el-radio :label="1">管理员</el-radio>
                <el-radio :label="2">教师</el-radio>
                <el-radio :label="3">学生</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item style="width:100%;">
                <el-button type="primary" style="width:100%; background: #505458; border: none;"
                    @click="Login()">登录</el-button>
            </el-form-item>
        </el-form>
    </body>
</template>

<script>



export default {
    name: 'Login',
    data() {
        return {
            loginForm: {
                username: '',
                password:'',
                radio:1,
            },
            rules: {
                username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
                password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
            }
            
        }
    },
    methods: {
        Login() {
            this.$refs.loginForm.validate((valid) => {
                if (valid) {
                    this.axios.post('/api/login', this.loginForm)
                        .then(resp => {
                            // 处理登录成功
                            if (resp.data.code === 200) {
                               this.$message.success(resp.data.message);
                                // 跳转到首页或其他页面
                                switch(this.loginForm.radio){
                                    case 1:
                                        this.$router.push('/home');
                                        break;
                                    case 2:
                                        this.$router.push('/about');
                                        break;
                                    case 3:
                                        this.$router.push('/student');
                                }
                            } else {
                                 this.$message.error(resp.data.message);
                            }
                        })
                        .catch(error => {
                            this.loading = false;
                            this.$message.error('登录失败，请重试');
                        })
                } else {
                    return false;
                }
            });
        },
    }
}
</script>

<style>
    #poster{
        background-position: center;
        height: 100%;
        width: 100%;
        background-size: cover;
        position: fixed;
    }
    body{
        margin: 0px;
        padding: 0px;
    }
    .login-container{
        border-radius: 15px;
        background-clip: padding-box;
        margin: 90px auto;
        width: 350px;
        padding: 35px 35px 15px 35px;
        background: #fff;
        border: 1px solid #eaeaea;
        box-shadow: 0 0 25px #cac6c6;
    }
    .login_title{
        margin:0px auto 40px auto;
        text-align: center;
        color: #505458;
    }
</style>
