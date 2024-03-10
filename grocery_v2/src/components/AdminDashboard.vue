<template>
  <navbar role="admin"></navbar>
  <div class="content">
    <div class="container mt-5">
      <table class="table table-bordered border-primary">
        <!-- Categories Table -->
        <thead>
          <tr class="table-dark">
            <th class="fs-5 text-center" colspan="3">Categories
              <router-link :to="{ name: 'add-category', params: { role: 'admin' } }">
                <button class="btn btn-primary btn-sm"><i class="bi bi-plus-circle-fill"></i></button>
              </router-link>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.category_id" class="table-warning">
            <!-- Display categories -->
            <td>{{ category.category_name }}</td>
            <td style="width: 50px">
              <!-- Update category button -->
              <router-link :to="{ name: 'update-category', params: { Id: category.category_id, role: 'admin' } }">
                <button type="button" class="btn btn-success btn-sm">
                  <i class="bi bi-pencil-square"></i>
                </button>
              </router-link>
            </td>
            <td style="width: 50px">
              <!-- Delete category button -->
              <router-link :to="{ name: 'confirm-delete', params: { Id: category.category_id, role: 'admin', type: 'category' } }">
                <button type="button" class="btn btn-danger btn-sm">
                  <i class="bi bi-trash3"></i>
                </button>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>

      <table class="table table-bordered border-primary">
        <!-- Manager Requests Table -->
        <thead>
          <tr class="table-info">
            <th colspan="5" class="fs-5 text-center">Requests from Managers</th>
          </tr>
          <tr class="table-dark">
            <th>Name</th>
            <th>Request / Email</th>
            <th>Status</th>
            <th class="text-center" colspan="2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- Display category requests -->
          <tr v-for="request in category_requests" :key="request.request_id" class="table-warning">
            <td>{{ request.name }}</td>
            <td>{{ request.request }}</td>
            <td>{{ request.status }}</td>
            <td style="width: 50px;">
              <button type="button" class="btn btn-success btn-sm" 
                v-on:click="categoryRequestHandler(request.request_id, 'approve')"
                :disabled="request.status != 'Pending'"> 
                <i class="bi bi-check-circle-fill"></i>
              </button>
            </td>
            <td style="width: 50px;">
              <button type="button" class="btn btn-danger btn-sm" 
                v-on:click="categoryRequestHandler(request.request_id, 'reject')"
                :disabled="request.status != 'Pending'"> 
                <i class="bi bi-x-circle-fill"></i>
              </button>
            </td>
          </tr>
          <!-- Display manager requests -->
          <tr v-for="request in manager_requests" :key="request.request_id" class="table-warning">
            <td>{{ request.manager_name }}</td>
            <td>{{ request.manager_email }}</td>
            <td>{{ request.manager_status }}</td>
            <td style="width: 50px;">
              <button type="button" class="btn btn-success btn-sm" 
                v-on:click="managerRequestHandler(request.manager_id, 'approve')"
                :disabled="request.manager_status != 'Pending'"> 
                <i class="bi bi-person-check"></i>
              </button>
            </td>
            <td style="width: 50px;">
              <button type="button" class="btn btn-danger btn-sm" 
                v-on:click="managerRequestHandler(request.manager_id, 'reject')"
                :disabled="request.manager_status != 'Pending'"> 
                <i class="bi bi-person-fill-x"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import RoleNavbar from "./RoleNavbar.vue";

export default {
  components: {
    navbar: RoleNavbar,
  },
  data() {
    return {
      categories: [],
      category_requests: [],
      manager_requests: [],
    };
  },
  mounted() {
    this.fetchCategories();
    this.fetchCategoryRequests();
    this.fetchManagerRequests();
  },
  methods: {
    async fetchCategories() {
        const url = `http://127.0.0.1:5000/api/category`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("admin_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.categories = data.categories;
        } else {
          alert(data.message);
          this.$router.push({ name: "role-auth" , params: { role: 'admin' }});
        }
    },

  async fetchManagerRequests() {
        const url = `http://127.0.0.1:5000/api/request/manager`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("admin_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.manager_requests = data.manager_requests;
        } else {
          alert(data.message);
          this.$router.push({ name: "admin-dashboard" });
        }
    },
    async managerRequestHandler(id, action) {
        const url = `http://127.0.0.1:5000/api/request/manager/${id}?action=${action}`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("admin_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchManagerRequests()
          this.fetchCategories();
        } else {
          alert(data.message);
          this.fetchManagerRequests()
          this.fetchCategories();
        }
    },
    async fetchCategoryRequests() {
        const url = `http://127.0.0.1:5000/api/request/category`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("admin_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.category_requests = data.category_requests;
        } else {
          alert(data.message);
          this.$router.push({ name: "admin-dashboard" });
        }
    },
    async categoryRequestHandler(id, action) {
        const url = `http://127.0.0.1:5000/api/request/category/${id}?action=${action}`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("admin_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.fetchCategoryRequests()
          this.fetchCategories();
        } else {
          alert(data.message);
          this.fetchCategoryRequests()
          this.fetchCategories();
        }
    },
  },
};
</script>

<style scoped>
</style>
