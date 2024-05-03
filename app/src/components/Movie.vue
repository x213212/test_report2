<template>
  <div>
    <h1>Movie Schedules</h1>
    <div v-if="weeklySchedule">
      <h2>Weekly Schedule</h2>
      <table>
        <thead>
          <tr>
            <th>Day</th>
            <th>Times</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(times, day) in weeklySchedule" :key="day">
            <td>{{ day }}</td>
            <td>
              <ul>
                <li v-for="time in times" :key="time.Time">
                  {{ time.Name }} at {{ time.Time }}
                </li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="monthlySchedule.length > 0">
      <h2>Monthly Schedule for {{ selectedMovie }}</h2>
      <ul>
        <li v-for="show in monthlySchedule" :key="show.Date">
          {{ show.Date }} - {{ show.Time }} - Entrance: {{ show.Entrance }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MovieScheduleViewer', // Updated component name
  data() {
    return {
      weeklySchedule: null,
      monthlySchedule: [],
      selectedMovie: 'Unicorn Galaxy',
      selectedMonth: '2023-12'
    };
  },
  mounted() {
    this.fetchWeeklySchedule();
    this.fetchMonthlySchedule();
  },
  methods: {
    fetchWeeklySchedule() {
      axios.get('/api/movies/weekly-schedule')
        .then(response => {
          this.weeklySchedule = response.data;
        })
        .catch(error => {
          console.error('Error fetching weekly schedule:', error);
        });
    },
    fetchMonthlySchedule() {
      axios.get(`/api/movies/monthly-schedule?name=${this.selectedMovie}&month=${this.selectedMonth}`)
        .then(response => {
          this.monthlySchedule = response.data;
        })
        .catch(error => {
          console.error('Error fetching monthly schedule:', error);
        });
    }
  }
};
</script>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  border: 1px solid black;
  padding: 8px;
  text-align: left;
}
</style>