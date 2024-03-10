<template>
  <navbar :role="role"></navbar>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-md-6 col-lg-4 col-12 auth-container">
        <h2 class="text-center fw-bold">
          {{ isUpdate ? "Edit Category" : "Create Category" }}
        </h2>

        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="category" class="form-label">Category Name</label>
            <input
              type="text"
              class="form-control"
              v-model="name"
              placeholder="Enter Category Name"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary btn-block">
            {{ isUpdate ? "Edit" : "Create" }}
          </button>
        </form>
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
    Id: Number,
  },
  data() {
    return {
      name: "",
    };
  },
  computed: {
    isAdmin() {
      return this.role === "admin";
    },
    isUpdate() {
      return !!this.Id;
    },
  },
  mounted() {
    if (this.isUpdate) {
      this.fetchCategoryData();
    }
  },
  methods: {
    getToken() {
      if (this.role === "admin") {
        return localStorage.getItem("admin_token");
      } else {
        return localStorage.getItem("manager_token");
      }
    },

    handleSubmit() {
      if (this.isUpdate) {
        this.updateCategory();
      } else {
        this.addCategory();
      }
    },
    async addCategory() {
      let url;
      if (this.role === "admin") {
        url = `http://127.0.0.1:5000/api/category`;
      } else {
        url = `http://127.0.0.1:5000/api/category/request`;
      }

        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: this.getToken(),
          },
          body: JSON.stringify({
            category: this.name,
          }),
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

    async updateCategory() {
      let url;
      if (this.role === "admin") {
        url = `http://127.0.0.1:5000/api/category/${this.Id}`;
      } else {
        url = `http://127.0.0.1:5000/api/category/request/${this.Id}`;
      }

        const response = await fetch(url, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: this.getToken(),
          },
          body: JSON.stringify({
            category: this.name,
          }),
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

    async fetchCategoryData() {
        const url = `http://127.0.0.1:5000/api/category?id=${this.Id}`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: this.getToken(),
          },
        });

        const data = await response.json();
        if (response.ok) {
          this.name = data.category.category_name;
        } else {
          alert(data.message);
          this.$router.push({ name: `${this.role}-dashboard` });
        }
    },
  },
};
</script>

<style scoped></style>
