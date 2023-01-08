
const {createApp} = Vue

createApp({
  data() {
    return {
      users: [],
      message: 'Hello world'
    }
  },
  async mounted() {
    await axios.get("http:localhost:5000/users").then(({data}) => {
      this.users = data;
    });
    console.log(this.users, 'here')
  }
}).mount('#app')