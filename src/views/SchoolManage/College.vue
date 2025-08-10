<template>
    <!--搜索-->
    <div>
        <div style="margin-bottom: 5px;">
            <el-input style="width: 200px;" placeholder="请输入学院ID" suffix-icon="el-icon-search"
                v-model="params.college_id" @keyup.enter.native="postCollege">
            </el-input>
            <el-input style="width: 200px; margin-left: 5px;" placeholder="请输入学院名称" suffix-icon="el-icon-search"
                v-model="params.college_name" @keyup.enter.native="postCollege">
            </el-input>
            <el-button type="primary" style="margin-left: 5px;" icon="el-icon-search"
                @click="postCollege">搜索</el-button>
            <el-button type="success" style="margin-left: 5px;" icon="el-icon-plus" @click="add">添加</el-button>
            <el-button type="danger" style="margin-left: 5px;" icon="el-icon-delete" @click="selectDelete" v-if="multipleSelection.length > 0">删除选中行</el-button>
        </div>
        <!--数据-->
        <el-table :data="tableData" :header-cell-style="{ background: '#f2f5fc', color: '#555555' }"
            @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column prop="id" label="ID" width="300" align='center'></el-table-column>
            <el-table-column prop="college_id" label="学院ID" width="360" align='center'></el-table-column>
            <el-table-column prop="college_name" label="学院名称" width="360" align='center'></el-table-column>
            <el-table-column label="操作" width="360" align='center'>
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
                <el-form-item label="学院ID" prop="college_id">
                    <el-col :span="20">
                        <el-input v-model="form.college_id" placeholder="请输入学院ID"></el-input>
                    </el-col>
                </el-form-item>
                <el-form-item label="学院名称" prop="college_name">
                    <el-col :span="20">
                        <el-input v-model="form.college_name" placeholder="请输入学院名称"></el-input>
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
                multipleSelection:[],
                //记录搜索条件内容
                params: {
                    college_id: "",
                    college_name: ""     
                },
                tableData: [],
                //弹窗标题
                title: "",
                //控制弹窗是否显示
                centerDialogVisible: false,
                //存储弹窗form表单对应的字段
                form: {
                    college_id: "",
                    college_name: ""
                },
                //检查规则
                rules: {
                    college_id: [{ required: true, message: '请输入学院ID', trigger: 'blur' }],
                    college_name: [{ required: true, message: '请输入学院名称', trigger: 'blur' }]
                },
                pageSize: 10,
                pageNum: 1,
                total: 1,
            }
        },
        mounted() {
            this.postCollege()
        },
        methods:{
            handleSelectionChange(val){
                this.multipleSelection = []
                val.forEach(item =>{
                    this.multipleSelection.push(item.id)
                })
            },
            selectDelete(){
                this.$confirm('此操作将删除所有选中行,是否继续?','提示',{
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(()=>{
                    this.multipleSelection.forEach(id => {
                        this.selectHandleDelete(id)
                    })
                    this.multipleSelection = []
                    this.postCollege()
                }).catch(()=>{
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                })
                
            },
            selectHandleDelete(id){
                this.axios.delete("/api/college/delete?id=" + id)
            },
            cancel() {
                this.centerDialogVisible = false;
                this.resetForm()
                   
            },
            resetForm() {
                this.$refs.form.resetFields();
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除【' + row.college_name + '】, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log(row.id)
                    this.axios.delete("/api/college/delete?id=" + row.id).then(res => {
                        if (res && res.data.code == '200') {
                            this.$message({
                                type: "success", message: "删除成功"
                            })
                            this.postCollege();
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
                this.title = "编辑学院",
                    this.form = Object.assign({}, row);
                this.centerDialogVisible = true;
            },
            save() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        if (this.form.id) {
                            //发起put请求修改方法
                            this.axios.put('/api/college/update', this.form).then(res => {
                                console.log(res)
                                if (res && res.data.code == '200') {
                                    this.$message({
                                        message: "修改成功!",
                                        type: "success"
                                    });
                                    this.centerDialogVisible = false;
                                    this.postCollege();
                                } else {
                                    this.$message({
                                        message: "修改失败!",
                                        type: "error"
                                    });
                                }
                            })
                        } else {
                            //发起post请求添加方法
                            this.axios.post('/api/college/save', this.form).then(res => {
                                if (res && res.data.code == 200) {
                                    this.$message({
                                        message: "添加学院成功!",
                                        type: "success"
                                    })
                                    this.centerDialogVisible = false;
                                    this.postCollege();
                                } else {
                                    console.log('获取数据失败')
                                    this.$message({
                                        message: "发生错误,添加学院失败!",
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
                this.title = '添加学院'
                this.centerDialogVisible = true
                this.resetForm()
                this.form = {
                    college_id:'',
                    college_name:'',
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
            postCollege() {
                //发起post请求
                this.axios.post('/api/college/paginated', {
                    pageNum: this.pageNum,
                    pageSize: this.pageSize,
                    params: {
                        college_id: this.params.college_id,
                        college_name: this.params.college_name
                    }
                }).then(res => {
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
                this.postCollege()
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
                this.pageNum = val
                this.postCollege()
            }
        }
    }
</script>

<style>

</style>