<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <h3>绝育率统计</h3>
          <div ref="sterilizationChart" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <h3>区域分布</h3>
          <div ref="zoneChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <h3>近6个月医疗支出趋势</h3>
          <div ref="costChart" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <h3>动物累计花费排行</h3>
          <el-empty v-if="animalCosts.length === 0" description="暂无数据" />
          <el-table v-else :data="animalCosts" style="width: 100%" stripe>
            <el-table-column type="index" label="序号" width="80" :index="(index) => index + 1" />
            <el-table-column prop="name" label="动物名称" />
            <el-table-column prop="total_cost" label="累计花费(元)" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import axios from '../utils/axios'

const sterilizationChart = ref(null)
const zoneChart = ref(null)
const costChart = ref(null)
const animalCosts = ref([])

const initSterilizationChart = async () => {
  const response = await axios.get('/api/statistics/sterilization')
  const data = response.data
  
  const chart = echarts.init(sterilizationChart.value)
  chart.setOption({
    tooltip: { trigger: 'item' },
    legend: { top: '5%', left: 'center' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: data.map(item => ({
        value: item.count,
        name: item.is_sterilized ? '已绝育' : '未绝育'
      }))
    }]
  })
}

const initZoneChart = async () => {
  const response = await axios.get('/api/statistics/zone-distribution')
  const data = response.data
  
  const chart = echarts.init(zoneChart.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: data.map(item => item.zone)
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: data.map(item => item.count),
      itemStyle: { color: '#5470c6' }
    }]
  })
}

const initCostChart = async () => {
  const response = await axios.get('/api/statistics/monthly-costs')
  const data = response.data
  
  const chart = echarts.init(costChart.value)
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: data.map(item => item.month)
    },
    yAxis: { type: 'value', name: '费用(元)' },
    series: [{
      type: 'line',
      data: data.map(item => parseFloat(item.total_cost)),
      smooth: true,
      itemStyle: { color: '#91cc75' }
    }]
  })
}

const loadAnimalCosts = async () => {
  const response = await axios.get('/api/statistics/animal-costs')
  animalCosts.value = response.data.slice(0, 10)
}

onMounted(() => {
  initSterilizationChart()
  initZoneChart()
  initCostChart()
  loadAnimalCosts()
})
</script>
