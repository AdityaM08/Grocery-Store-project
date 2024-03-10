<template>
  <navbar :role="role"></navbar>
  <div class="row justify-content-center mt-5">
    <div class="col-md-4">
      <div class="card">
        <div class="card-body">
          <h3 class="card-title text-center">Do you really want to Delete this {{ type }}?</h3>
          <form @submit.prevent="deletehandler">
            <div class="row justify-content-center mt-5">
              <button type="submit" class="btn btn-danger" style="width: 100px">Delete</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import RoleNavbar from "./RoleNavbar.vue";
export default {
  components: {
    navbar: RoleNavbar,
  },
  props: {
    role: String,
    type: String,
    Id: Number,
  },
  computed: {
    isAdmin() {
      return this.role === "admin";
    },
  },
  methods: {
    getToken() {
      if (this.role === "admin") {
        return localStorage.getItem("admin_token");
      } else {
        return localStorage.getItem("manager_token");
      }
    },

    getUrl() {
      if (this.role === "manager" && this.type === "category") {
        return `http://127.0.0.1:5000/api/category/request/${this.Id}`;
      } else {
        return `http://127.0.0.1:5000/api/${this.type}/${this.Id}`;
      }
    },

    async deletehandler() {
        const response = await fetch(this.getUrl(), {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: this.getToken(),
          },
        });
        
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push({ name: `${this.role}-dashboard` });
        } else {
          alert(data.message);
          this.$router.push({ name: `${this.role}-dashboard` });
        }
    },
  }
}
</script>
  
<style scoped>

.card {
  min-width: 352px;
}
</style>