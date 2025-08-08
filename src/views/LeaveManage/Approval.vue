<template>
    <!--搜索-->
    <div>
        <div style="margin-bottom: 5px;">
            <el-select style="width: 200px; margin-left: 5px;" v-model="params.type" placeholder="请选择请假类型">
                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
            <el-select style="width: 200px; margin-left: 5px;" v-model="params.status" placeholder="请选择审批状态">
                <el-option v-for="item in StatusOptions" :key="item.value" :label="item.label" :value="item.value">
                </el-option>
            </el-select>
            <el-button type="primary" style="margin-left: 5px;" icon="el-icon-search"
                @click="postApplication">搜索</el-button>
            <el-button type="success" style="margin-left: 5px;" icon="el-icon-refresh-right"
                @click="reset">重置</el-button>
            <el-button type="danger" style="margin-left: 5px;" icon="el-icon-delete" @click="selectDelete"
                v-if="multipleSelection.length > 0">删除选中行</el-button>
        </div>
        <!--数据-->
        <el-table :data="tableData" :header-cell-style="{ background: '#f2f5fc', color: '#555555' }"
            @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column prop="id" label="ID" width="180" align='center'></el-table-column>
            <el-table-column prop="name" label="申请人" width="240" align='center'></el-table-column>
            <el-table-column prop="apply_time" label="申请时间" width="300" align='center'></el-table-column>
            <el-table-column prop="type" label="请假类型" width="180" align='center'></el-table-column>
            <el-table-column prop="status" label="状态" width="240" align='center'>
                <template slot-scope="scope">
                    <el-tag :type="scope.row.status === 0 ? 'warning' : (scope.row.status === 1 ? 'success' : 'danger')"
                        disable-transitions>
                        {{ scope.row.status === 0 ? '待审批' : (scope.row.status === 1 ? '已批准' : '已拒绝') }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作" width="240" align='center'>
                <template slot-scope="scope">
                    <el-button size="mini" type="success" @click="handleApproval(scope.$index, scope.row)"
                        icon="el-icon-edit" v-if="scope.row.status===0">审批</el-button>
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)"
                        v-else>删除</el-button>
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
                <el-form-item label="状态" prop="status">
                    <el-col :span="20">
                        <el-radio-group v-model="form.status">
                            <el-radio :label="1">批准</el-radio>
                            <el-radio :label="2">拒绝</el-radio>
                        </el-radio-group>
                    </el-col>
                </el-form-item>
                <el-form-item label="审批意见" prop="audit_remark">
                    <el-col :span="20">
                        <el-input v-model="form.audit_remark" type="textarea" :rows="4"
                            placeholder="请输入审批意见"></el-input>
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
        name:"Approval",
        data(){
            return {
                multipleSelection:[],
                rules: {
                    status: [{ required: true, message: '请选择状态', trigger: 'blur' }],
                    audit_remark: [{ required: true, message: '请输入审批意见', trigger: 'blur' }],
                },
                form:{
                    status:"",
                    audit_remark:""
                },
                //弹窗标题
                title: "",
                //控制弹窗是否显示
                centerDialogVisible: false,
                user:{},
                options: [{
                    value: '事假',
                    label: '事假'
                }, {
                    value: '病假',
                    label: '病假'
                }, {
                    value: '丧假',
                    label: '丧假'
                }, {
                    value: '校外实习',
                    label: '校外实习'
                }],
                StatusOptions: [{
                    value: '0',
                    label: '待审批'
                }, {
                    value: '1',
                    label: '已批准'
                }, {
                    value: '2',
                    label: '已拒绝'
                }],
                //记录搜索条件内容
                params: {
                    name:"",
                    type: "",
                    status: "",
                    role_id:""
                },
                tableData: [],
                pageSize: 10,
                pageNum: 1,
                total: 1,
            }
        },
        mounted() {
            this.init()
            this.postApplication()
        },
        methods:{
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除ID为【' + row.id + '】的请假, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log(row.id)
                    this.axios.delete("/api/application/delete?id=" + row.id).then(res => {
                        if (res && res.data.code == '200') {
                            this.$message({
                                type: "success", message: "删除成功"
                            })
                            this.postApplication();
                        }
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            handleSelectionChange(val) {
                this.multipleSelection = []
                val.forEach(item => {
                    this.multipleSelection.push(item.id)
                })
            },
            selectHandleDelete(id) {
                this.axios.delete("/api/application/delete?id=" + id)
            },
            selectDelete() {
                this.$confirm('此操作将删除所有选中行,是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.multipleSelection.forEach(id => {
                        this.selectHandleDelete(id)
                    })
                    this.multipleSelection = []
                    this.postApplication()
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                })

            },
            save() {
                this.$refs.form.validate((valid) => {
                    if (valid) {
                        if (this.form.id) {
                            //发起put请求修改方法
                            this.axios.put('/api/application/update', this.form).then(res => {
                                console.log(res)
                                if (res && res.data.code == '200') {
                                    this.$message({
                                        message: "审批成功!",
                                        type: "success"
                                    });
                                    this.centerDialogVisible = false;
                                    this.postApplication();
                                } else {
                                    this.$message({
                                        message: "审批失败!",
                                        type: "error"
                                    });
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
            cancel() {
                this.centerDialogVisible = false;
                this.resetForm()

            },
            resetForm() {
                if (this.$refs.form) {
                    this.$refs.form.resetFields();
                } else {
                    console.log('表单引用不存在')
                }

            },
            init() {
                this.user = JSON.parse(sessionStorage.getItem('CurUser'))
                this.params.name = this.user.name
                this.params.role_id = this.user.role_id
            },
            reset() {
                this.params.type = ''
                this.params.status = ''
                this.postApplication()
            },
            handleApproval(index, row) {
                this.title = "审批请假",
                    this.form = Object.assign({}, row);
                this.centerDialogVisible = true;
            },
            postApplication() {
                //发起post请求
                this.axios.post('/api/application/paginated', {
                    pageNum: this.pageNum,
                    pageSize: this.pageSize,
                    params: {
                        type: this.params.type,
                        status: this.params.status,
                        name: this.params.name,
                        role_id:this.params.role_id
                    }
                }).then(res => {
                    console.log(this.params)
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
                this.postApplication()
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
                this.pageNum = val
                this.postApplication()
            }
        },
    }
</script>

<style>

</style>