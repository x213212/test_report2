<template>
  <div class="chart-container-wrapper">
    <div class="chart-container">
      <Line id="my-chart-id1" :options="chartOptions1" :data="chartData1" />
    </div>
  </div>
</template>
<style>
.chart-container-wrapper {
  width: 100%;
  overflow-x: auto;
}

.chart-container {
  width: fit-content;
  height: 200px;
}
</style>
<script>
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { Line } from 'vue-chartjs';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export default {
  name: 'LineChart',
  components: { Line },
  data() {
    return {
      chartData1: {
        labels: [],
        datasets: [
          {
            label: 'Score 1',
            data: [],
            fill: false,
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.1)',
            pointRadius: 2,
            pointBackgroundColor: 'rgba(54, 162, 235, 1)',
            pointStyle: 'circle'
          }
        ]
      },
      chartOptions1: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            min: 0,
            max: 50
          },
          x: {
            display: false // 隐藏 x 轴标签
          }
        }
      }
    };
  },
  created() {
    this.generateRandomData();
  },
  methods: {
    generateRandomData() {
      const scoreData1 = [];
      const timestamps = [];

      for (let i = 0; i < 100; i++) {
        const randomScore1 = Math.random() * 50;
        const timestamp = Date.now() + i * 86400000;

        scoreData1.push(randomScore1);
        timestamps.push(timestamp);
      }

      const dateLabels = timestamps.map(timestamp => {
        const date = new Date(timestamp);
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        return `${year}/${month}/${day}`;
      });

      this.chartData1.labels = dateLabels;
      this.chartData1.datasets[0].data = scoreData1;
    }
  }
};
</script>