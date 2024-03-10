<template>
    <normalnav></normalnav>
    <div class="container">
      <div class="row justify-content-center">
    
        <div class="col-10 col-lg-4 col-md-5 auth-container bg-light">
          <h2 class="text-center fw-bold">
            {{
              role === "admin" ? "Admin" : role === "manager" ? "Manager" : "User"
            }}
            {{ isLogin ? "Login" : "Signup" }}
          </h2>
          <form @submit.prevent="handleSubmit">
            <div v-if="!isLogin" class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input type="text" id="name" v-model="userData.name" class="form-control" 
              placeholder="Enter your username" required />
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input type="email" id="email" v-model="userData.email" class="form-control" 
              placeholder="Enter your email" required />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password</label>
              <input type="password" id="password" v-model="userData.password" class="form-control" 
              placeholder="Enter your password" required />
            </div>
            <button type="submit" class="btn btn-primary btn-block">
              {{ isLogin ? "Login" : "Signup" }}
            </button>
          </form>
          <hr />
          <div class="text-center" v-if="isManagerOrUser" >
            {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
            <router-link :to="{ name: isLogin ? 'signup' : 'login', params: { role: role } }" class="text-decoration-none">
              {{ isLogin ? "Signup" : "Login" }}
            </router-link>
        </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
  import HomeNavbar from "./HomeNavbar.vue";
  export default {
    props: ["isLogin", "role"],
    components: {
      normalnav: HomeNavbar,
    },
    computed: {
      isManagerOrUser() {
        return this.role === "manager" || this.role === "user";
      },
    },
  
    data() {
      return {
        userData: {
          name: "",
          email: "",
          password: "",
        },
      };
    },
    methods: {
      handleSubmit() {
        if (this.isLogin) {
          this.login();
        } else {
          this.signup();
        }
      },
      async login() {
          const url = `http://127.0.0.1:5000/api/${this.role}/login`
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              email: this.userData.email,
              password: this.userData.password,
            }),
          });
  
          const data = await response.json()
          if (response.ok) {
            localStorage.setItem(`${this.role}_token`, data.token)
            if (this.role === "manager" || this.role === "user") {
              localStorage.setItem(`${this.role}_name`, data.name)
            }
            alert(data.message);
            this.$router.push({ name: `${this.role}-dashboard` });
          } else {
            alert(data.message);
            this.$router.push({ name: 'role-auth', params: { role: this.role } });
          }
      },
      async signup() {
          const url = `http://127.0.0.1:5000/api/${this.role}/signup`
          const response = await fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: this.userData.name,
              email: this.userData.email,
              password: this.userData.password,
            }),
          });
  
          const data = await response.json()
          if (response.ok) {
            if (this.role === "admin" || this.role === "user") {
              localStorage.setItem(`${this.role}_token`, data.token)
              localStorage.setItem(`${this.role}_name`, data.name)
              this.$router.push({ name: `${this.role}-dashboard` });
            } else {
              alert(data.message);
              this.$router.push({ name: 'role-auth' });
            }
          } else {
            alert(data.message);
            this.$router.push({ name: 'role-auth' });
          }
      },
    },
  };
  </script>
 
 <style scoped>
</style>