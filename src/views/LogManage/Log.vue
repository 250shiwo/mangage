<template>
    <!--搜索-->
    <div>
        <div style="margin-bottom: 5px;">
            <el-input style="width: 200px;" placeholder="请输入操作内容" suffix-icon="el-icon-search"
                v-model="params.content" @keyup.enter.native="postLog">
            </el-input>
            <el-input style="width: 200px; margin-left: 5px;" placeholder="请输入操作人" suffix-icon="el-icon-search"
                v-model="params.username" @keyup.enter.native="postLog">
            </el-input>
            <el-button type="primary" style="margin-left: 5px;" icon="el-icon-search"
                @click="postLog">搜索</el-button>
            <el-button type="danger" style="margin-left: 5px;" icon="el-icon-delete" @click="selectDelete" v-if="multipleSelection.length > 0">删除选中行</el-button>
        </div>
        <!--数据-->
        <el-table :data="tableData" :header-cell-style="{ background: '#f2f5fc', color: '#555555' }"
            @selection-change="handleSelectionChange">
            <el-table-column type="selection" width="60"></el-table-column>
            <el-table-column prop="id" label="ID" width="60" align='center'></el-table-column>
            <el-table-column prop="content" label="操作内容" width="240" align='center'></el-table-column>
            <el-table-column prop="time" label="操作时间" width="360" align='center'></el-table-column>
            <el-table-column prop="username" label="操作人" width="180" align='center'></el-table-column>
            <el-table-column prop="ip" label="IP地址" width="240" align='center'></el-table-column>
            <el-table-column label="操作" width="300" align='center'>
                <template slot-scope="scope">
                    <el-button size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
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
        name:"Log",
        data(){
            return {
                multipleSelection:[],
                //记录搜索条件内容
                params: {
                    content: "",
                    username: ""     
                },
                tableData: [],
                pageSize: 10,
                pageNum: 1,
                total: 1,
            }
        },
        mounted() {
            this.postLog()
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
                    this.postLog()
                }).catch(()=>{
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                })
                
            },
            selectHandleDelete(id){
                this.axios.delete("/api/log/delete?id=" + id)
            },
            handleDelete(index, row) {
                this.$confirm('此操作将永久删除ID为【' + row.id + '】的数据, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    console.log(row.id)
                    this.axios.delete("/api/log/delete?id=" + row.id).then(res => {
                        if (res && res.data.code == '200') {
                            this.$message({
                                type: "success", message: "删除成功"
                            })
                            this.postLog();
                        }
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });
                });
            },
            postLog() {
                //发起post请求
                this.axios.post('/api/log/paginated', {
                    pageNum: this.pageNum,
                    pageSize: this.pageSize,
                    params: {
                        content: this.params.content,
                        username: this.params.username
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
                this.postLog()
            },
            handleCurrentChange(val) {
                console.log(`当前页: ${val}`);
                this.pageNum = val
                this.postLog()
            }
        }
    }
</script>

<style>

</style>