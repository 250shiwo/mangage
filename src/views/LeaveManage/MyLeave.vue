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
        </div>
        <!--数据-->
        <el-table :data="tableData" :header-cell-style="{ background: '#f2f5fc', color: '#555555' }">
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
                    <el-button size="mini" type="danger" @click="handleRevoke(scope.$index, scope.row)"
                        icon="el-icon-edit-outline">撤销</el-button>
                </template>
            </el-table-column>
        </el-table>
        <el-pagination style="text-align: center;" @size-change="handleSizeChange" @current-change="handleCurrentChange"
            :current-page="pageNum" :page-sizes="[5, 10]" :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
    </div>
</template>

<script>
    export default{
        name:"MyLeave",
        data(){
            return {
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
                    status: ""     
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
            init() {
                this.user = JSON.parse(sessionStorage.getItem('CurUser'))
                this.params.name = this.user.name
            },
            reset() {
                this.params.type = ''
                this.params.status = ''
                this.postApplication()
            },
            handleRevoke(index, row) {
                if (row.status === 1 || row.status === 2) {
                    this.$message({ type: 'warning', message: '已审批的申请无法撤销' });
                    return;
                }
                this.$confirm('此操作将撤销ID为【' + row.id + '】的请假申请, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log(row.id)
                    this.axios.delete("/api/application/delete?id=" + row.id).then(res => {
                        if (res && res.data.code == '200') {
                            this.$message({
                                type: "success", message: "撤销成功"
                            })
                            this.postApplication();
                        }
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消撤销'
                    });
                });
            },
            postApplication() {
                //发起post请求
                this.axios.post('/api/application/paginated', {
                    pageNum: this.pageNum,
                    pageSize: this.pageSize,
                    params: {
                        type: this.params.type,
                        status: this.params.status,
                        name: this.params.name
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