<template>
    <!--搜索-->
    <div>
        <div style="margin-bottom: 5px;">
            <el-input style="width: 200px;" placeholder="请输入专业ID" suffix-icon="el-icon-search" v-model="params.speciality_id"
                @keyup.enter.native="postSpeciality">
            </el-input>
            <el-input style="width: 200px; margin-left: 5px;" placeholder="请输入专业名称" suffix-icon="el-icon-search"
                v-model="params.speciality_name" @keyup.enter.native="postSpeciality">
            </el-input>
            <el-input style="width: 200px; margin-left: 5px;" placeholder="请输入所属学院" suffix-icon="el-icon-search"
                v-model="params.college_id" @keyup.enter.native="postSpeciality">
            </el-input>
            <el-button type="primary" style="margin-left: 5px;" icon="el-icon-search"
                @click="postSpeciality">搜索</el-button>
            <el-button type="success" style="margin-left: 5px;" icon="el-icon-plus" @click="add">添加</el-button>
        </div>
        <!--数据-->
        <el-table :data="tableData" :header-cell-style="{ background: '#f2f5fc', color: '#555555' }">
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column prop="id" label="ID" width="240" align='center'></el-table-column>
            <el-table-column prop="speciality_id" label="专业ID" width="300" align='center'></el-table-column>
            <el-table-column prop="speciality_name" label="专业名称" width="300" align='center'></el-table-column>
            <el-table-column prop="college_id" label="所属学院ID" width="240" align='center'></el-table-column>
            <el-table-column label="操作" width="300" align='center'>
                <template slot-scope="scope">
                    <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination style="text-align: center;" @size-change="handleSizeChange" @current-change="handleCurrentChange"
            :current-page="pageNum" :page-sizes="[5, 10]" :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
        <!--弹窗-->
        <el-dialog :title="title" :visible.sync="centerDialogVisible" width="30%" center>
            <el-form ref="form" :rules="rules" :model="form" label-width="80px">
                <el-form-item label="专业ID" prop="speciality_id">
                    <el-col :span="20">
                        <el-input v-model="form.speciality_id" placeholder="请输入专业ID"></el-input>
                    </el-col>
                </el-form-item>
                <el-form-item label="专业名称" prop="speciality_name">
                    <el-col :span="20">
                        <el-input v-model="form.speciality_name" placeholder="请输入专业名称"></el-input>
                    </el-col>
                </el-form-item>
                 <el-form-item label="所属学院" prop="college_id">
                    <el-col :span="20">
                        <el-input v-model="form.college_id" placeholder="请输入所属学院"></el-input>
                    </el-col>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancel">取 消</el-button>
                <el-button type="primary" @click="save">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default{
        name:"College",
        data(){
            return {
                //记录搜索条件内容
                params: {
                    speciality_id: "",
                    speciality_name: "",
                    college_id: ""  
                },
                tableData: [],
                //弹窗标题
                title: "",
                //控制弹窗是否显示
                centerDialogVisible: false,
                //存储弹窗form表单对应的字段
                form: {
                    speciality_id: "",
                    speciality_name: "",
                    college_id:"",
                },
                //检查规则
                rules: {
                    speciality_id: [{ required: true, message: '请输入专业ID', trigger: 'blur' }],
                    speciality_name: [{ required: true, message: '请输入专业名称', trigger: 'blur' }],
                    college_id: [{ required: true, message: '请输入所属学院', trigger: 'blur' }]
                },
                pageSize: 10,
                pageNum: 1,
                total: 1,
            }
        },
        mounted() {
            this.postSpeciality()
        },
        methods:{
            cancel() {
                this.centerDialogVisible = false;
                this.resetForm()
                   
            },
            resetForm() {
                this.$refs.form.resetFields();
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除【' + row.speciality_name + '】, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log(row.id)
                    this.axios.delete("/api/speciality/delete?id=" + row.id).then(res => {
                        if (res && res.data.code == '200') {
                            this.$message({
                                type: "success", message: "删除成功"
                            })
                            this.postSpeciality();
                        }
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            handleEdit(index, row) {
                this.title = "编辑专业",
                    this.form = Object.assign({}, row);
                this.centerDialogVisible = true;
            },
            save() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        if (this.form.id) {
                            //发起put请求修改方法
                            this.axios.put('/api/speciality/update', this.form).then(res => {
                                console.log(res)
                                if (res && res.data.code == '200') {
                                    this.$message({
                                        message: "修改成功!",
                                        type: "success"
                                    });
                                    this.centerDialogVisible = false;
                                    this.postSpeciality();
                                } else {
                                    this.$message({
                                        message: "修改失败!",
                                        type: "error"
                                    });
                                }
                            })
                        } else {
                            //发起post请求添加方法
                            this.axios.post('/api/speciality/save', this.form).then(res => {
                                if (res && res.data.code == 200) {
                                    this.$message({
                                        message: "添加专业成功!",
                                        type: "success"
                                    })
                                    this.centerDialogVisible = false;
                                    this.postSpeciality();
                                } else {
                                    console.log('获取数据失败')
                                    this.$message({
                                        message: "发生错误,添加专业失败!",
                                        type: "error"
                                    })
                                }
                            })
                        }
                    } else {
                        this.$message({
                            message: "请检查输入数据是否完整",
                            type: "error"
                        })
                        return false;
                    }
                });

            },
            add() {
                this.title = '添加专业'
                this.centerDialogVisible = true
                this.resetForm()
                this.form = {
                    speciality_id:'',
                    speciality_name:'',
                    college_id:'',
                    id: ''
                }
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
            postSpeciality() {
                //发起post请求
                this.axios.post('/api/speciality/paginated', {
                    pageNum: this.pageNum,
                    pageSize: this.pageSize,
                    params: {
                        speciality_id: this.params.speciality_id,
                        speciality_name: this.params.speciality_name,
                        college_id:this.params.college_id
                    }
                }).then(res => {
                    console.log(res)
                    if (res && res.data.code == 200) {
                        this.tableData = res.data.data
                        this.total = res.data.total
                    } else {
                        console.log('获取数据失败')
                    }
                })
            },
            handleSizeChange(val) {
                console.log(`每页 ${val} 条`);
                this.pageNum = 1
                this.pageSize = val
                this.postSpeciality()
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
                this.pageNum = val
                this.postSpeciality()
            }
        }
    }
</script>

<style>

</style>