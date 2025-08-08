<template>
    <div class="leave-form-container">
        <el-form ref="leaveForm" :model="formData" :rules="rules" label-width="120px" class="leave-form">
            <!-- 申请人 -->
            <el-form-item label="申请人" prop="name">
                <el-input v-model="formData.name" :disabled="true"></el-input>
            </el-form-item>

            <!-- 请假类型 -->
            <el-form-item label="请假类型" prop="type">
                <el-select v-model="formData.type" placeholder="请选择" clearable>
                    <el-option v-for="item in leaveTypeOptions" :key="item.value" :label="item.label"
                        :value="item.value" />
                </el-select>
            </el-form-item>

            <!-- 请假时间 -->
            <el-form-item label="请假时间" prop="leaveTime">
                <div class="datetime-range">
                    <el-date-picker v-model="formData.StartleaveTime" type="datetime" placeholder="开始日期时间"
                        format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss">
                    </el-date-picker>
                    <span class="range-separator">到</span>
                    <el-date-picker v-model="formData.EndleaveTime" type="datetime" placeholder="结束日期时间"
                        format="yyyy-MM-dd HH:mm:ss" value-format="yyyy-MM-dd HH:mm:ss">
                    </el-date-picker>
                </div>
            </el-form-item>

            <!-- 请假说明 -->
            <el-form-item label="请假说明" prop="remark">
                <el-input v-model="formData.remark" type="textarea" :rows="4" placeholder="请输入请假说明" />
            </el-form-item>

            <!-- 提交按钮 -->
            <el-form-item>
                <el-button type="primary" @click="submitForm">提交</el-button>
                <el-button type="success" style="margin-left: 15px;"@click="reset">重置</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

<script>
export default {
  name: 'LeaveForm',
  data() {
    return {
      user:{},
      formData: {
        name: '', 
        type: '',
        StartleaveTime:'',
        EndleaveTime:'',
        remark: '',
        apply_time:''
      },
      leaveTypeOptions: [
        { label: '事假', value: '事假' },
        { label: '病假', value: '病假' },
        { label: '丧假', value: '丧假' },
        { label: '校外实习', value: '校外实习' }
      ],
      rules: {
        type: [{ required: true, message: '请选择请假类型', trigger: 'blur' }],
        leaveTime: [{required:true, validator:this.validateLeaveTime,trigger:'blur'}],
        remark: [{ required: true, message: '请输入请假说明', trigger: 'blur' }]
      }
    };
  },
  methods: {
    validateLeaveTime(rule,value,callback){
        const startTime = this.formData.StartleaveTime;
        const endTime = this.formData.EndleaveTime;
        if (!startTime || !endTime) {
            return callback(new Error('请选择完整的开始和结束时间'));
        }
        const start = new Date(startTime).getTime();
        const end = new Date(endTime).getTime();
        if (end < start) {
            return callback(new Error('结束时间不能早于开始时间'));
        }
        callback();
    },
    init(){
        this.user = JSON.parse(sessionStorage.getItem('CurUser'))
        this.formData.name = this.user.name
    },
    reset() {
      this.formData.type = ''
      this.formData.StartleaveTime = ''
      this.formData.EndleaveTime = ''
      this.formData.remark = ''
    },
    getIncrease(num, digit) {
      var increase = "";
      for (var i = 0; i < digit; i++) {
        increase += "0";
      }
      return (increase + num).slice(-digit);
    },
    submitForm() {
      this.$refs.leaveForm.validate(valid => {
        if (valid) {
          // 表单验证通过，提交数据
          const newtime = new Date();
          const hour = this.getIncrease(newtime.getHours(), 2);
          const minitus = this.getIncrease(newtime.getMinutes(), 2);
          const seconds = this.getIncrease(newtime.getSeconds(), 2);
          const nian = this.getIncrease(newtime.getFullYear(), 4);
          const yue = this.getIncrease(newtime.getMonth() + 1, 2);
          const re = this.getIncrease(newtime.getDate(), 2)
          this.formData.apply_time = nian+"-"+yue+"-"+re+" "+hour+":"+minitus+":"+seconds
          console.log('表单数据：', this.formData);
          // 这里可以替换为实际的API请求
          this.axios.post('/api/application/save', this.formData).then(res => {
            if (res && res.data.code == 200) {
              this.$message({
                message: "请假申请提交成功!",
                type: "success"
              })
              this.reset()
            } else {
              this.$message({
                message: "发生错误,请假申请提交失败!",
                type: "error"
              })
            }
          })
        }
      });
    }
  },
  created(){
    this.init()
  }
};
</script>

<style scoped>
.leave-form-container {
  padding: 20px;
}
.leave-form {
  max-width: 800px;
}
.el-form-item {
  margin-bottom: 20px;
}
.datetime-range {
  display: flex;
  align-items: center;
}

.range-separator {
  margin: 0 10px;
  color: #606266;
}
</style>