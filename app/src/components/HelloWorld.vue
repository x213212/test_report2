<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <button @click="fetchUsers">Fetch Users</button>
    <ul>
      <li v-for="user in users" :key="user.id">
        <div>
          <el-input v-model="user.name"></el-input>
        </div>
        <div>
          <el-input-number v-model="user.age"></el-input-number>
        </div>
        <div>
          <el-button @click="deleteUser(user._id.$oid)" type="danger">Delete</el-button>
          <el-button @click="updateUser(user._id.$oid)" type="primary">Update</el-button>
        </div>
      </li>
    </ul>
    <form @submit.prevent="createUser">
      <input type="text" v-model="newUser.name" placeholder="Name" required>
      <input type="number" v-model="newUser.age" placeholder="Age" required>
      <button type="submit">Create User</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      users: [],
      newUser: {
        name: '',
        age: null
      }
    }
  },
  methods: {
    fetchUsers() {
      axios.get('/api/users')
        .then(response => {
          this.users = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
    createUser() {
      axios.post('/api/users', this.newUser)
        .then(response => {
          this.users.push(response.data)
          this.newUser.name = ''
          this.newUser.age = null
        })
        .catch(error => {
          console.error(error)
        })
    },
    deleteUser(userId) {
      axios.delete(`/api/users/${userId}`)
        .then(response => {
          // 請求成功處理
          console.log("User deleted:", response.data);
          // 更新用戶列表
          this.users = this.users.filter(user => user.id !== userId);
          this.fetchUsers();
        })
        .catch(error => {
          // 請求失敗處理
          console.error("Error deleting user:", error);
        });
    },
    updateUser(userId) {
      const user = this.users.find(user => user._id.$oid === userId);
      const updatedUser = {
        name: user.name,
        age: user.age
      };
      axios.put(`/api/users/${userId}`, updatedUser)
        .then(response => {
          // 更新成功后的处理
          console.log("User update:", response.data);
          this.fetchUsers();
        })
        .catch(error => {
          console.error(error);
        });
    }
  }
}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>