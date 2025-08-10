<template>
    <div>
        <!-- 顶部统计数据卡片 -->
        <div class="stats-container">
            <el-row :gutter="20">
                <el-col :xs="24" :sm="12" :md="6" v-for="(item, index) in statsData" :key="index" class="stats-col">
                    <div class="stats-card" :class="`stats-card-${index}`">
                        <div class="stats-icon">
                            <i :class="item.icon"></i>
                        </div>
                        <div class="stats-value">{{ item.number }}</div>
                        <div class="stats-title">{{ item.title }}</div>
                    </div>
                </el-col>
            </el-row>
        </div>
        <!-- 图表区域 -->
        <div style="display: flex;">
            <div style="width: 50%; background-color: #FFFFFF; margin-left: 5px;">
                <div id="pie" style="width: 100%; height: 450px;"></div>
            </div>
            <div style="width: 50%; background-color: #FFFFFF; margin-left: 20px;">
                <div id="bar" style="width: 100%; height: 450px;"></div>
            </div>
        </div>
    </div>
</template>
<script>
import * as echarts from 'echarts';
export default {
  name: 'Monitor',
  data() {
    return {
      statsData: [
        { icon: 'el-icon-office-building', number: 6, title: '专业数量' },
        { icon: 'el-icon-user', number: 8, title: '学生总数' },
        { icon: 'el-icon-tickets', number: 20, title: '累计请假人次' },
        { icon: 'el-icon-time', number: 1992.76, title: '累计请假时长(单位：小时)' }
      ],
    }
  },
  mounted() {
    this.initEcharts()
  },
  methods: {
      initEcharts(){
          this.axios.get('/api/echarts/pie').then(res => {
              if (res && res.data.code == 200) {
                  this.initPie(res.data.data)
              } else {
                  console.log('获取数据失败')
              }
          })
          this.axios.get('/api/echarts/bar').then(res => {
              if (res && res.data.code == 200) {
                  this.initBar(res.data.data.xAxis,res.data.data.yAxis)
              } else {
                  console.log('获取数据失败')
              }
          })
      },
      initPie(data) {
          let chartDom = document.getElementById('pie');
          let myChart = echarts.init(chartDom);
          let option;

          option = {
              title: {
                  text: '请假单类型分布图',
                  left: 'center'
              },
              tooltip: {
                  trigger: 'item'
              },
              legend: {
                  orient: 'vertical',
                  left: 'left',
                  top:'top'
              },
              series: [
                  {
                      name: '请假类型',
                      type: 'pie',
                      radius: '70%',
                      data:data,
                      emphasis: {
                          itemStyle: {
                              shadowBlur: 10,
                              shadowOffsetX: 0,
                              shadowColor: 'rgba(0, 0, 0, 0.5)'
                          }
                      }
                  }
              ]
          };

          option && myChart.setOption(option);
      },
      initBar(xAxis,yAxis){
          let chartDom = document.getElementById('bar');
          let myChart = echarts.init(chartDom);
          let option;
          option = {
              tooltip: {
                  trigger: 'axis',
                  axisPointer: {
                      type: 'shadow'
                  }
              },
              title: {
                  text: '学生请假次数排行TOP5',
                  left: 'center'
              },
              grid: {
                  left: '3%',
                  right: '4%',
                  bottom: '3%',
                  containLabel: true
              },
              xAxis: {
                  type: 'category',
                  data: xAxis,
                  axisTick: {
                      alignWithLabel: true
                  }
              },
              yAxis: {
                  type: 'value'
              },
              series: [
                  {
                      data: yAxis,
                      type: 'bar',

                      backgroundStyle: {
                          color: 'rgba(180, 180, 180, 0.2)'
                      }
                  }
              ]
          };

          option && myChart.setOption(option);
      }
  }
}
</script>

<style scoped>
.stats-container {
  padding: 20px;
}

.stats-col {
  padding: 10px;
}

.stats-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 120px;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

/* 自定义不同卡片的颜色 */
.stats-card-0 {
  background-color: #409EFF;
  border: 1px solid #409EFF;
  color: #fff;
}

.stats-card-1 {
  background-color: #67C23A;
  border: 1px solid #67C23A;
  color: #fff;
}

.stats-card-2 {
  background-color: #F56C6C;
  border: 1px solid #F56C6C;
  color: #fff;
}

.stats-card-3 {
  background-color: #409EFF;
  border: 1px solid #409EFF;
  color: #fff;
}

.stats-icon {
  font-size: 40px;
  margin-bottom: 15px;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.stats-title {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
}
</style>