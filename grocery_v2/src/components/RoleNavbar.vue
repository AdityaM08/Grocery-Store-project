<template>
  <nav class="navbar navbar-expand-md navbar-primary bg-primary">
    <router-link :to="getDashboardLink()">
      <span class="text-white fw-bold fs-4" style="margin-left: 10px;">
        <i class="bi bi-bag-heart"></i> GroceryShop | 
        <span class="fs-5 text-white">
          {{
            role === "admin"
            ? "Admin"
            : role === "manager"
              ? name ? name : "Manager"
              : role === "user"
                ? name ? name : "User"
                : ""
          }}
        </span>
      </span>
    </router-link>

    <!-- Collapse button for small screens -->
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
      aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse justify-content-end" id="navbarNavDropdown">
      <ul class="navbar-nav" style="margin-right: 5px;">
        <template v-if="role === 'admin'">
          <!-- Admin specific menu items -->
        </template>

        <template v-if="role === 'manager'">
          <li class="nav-item">
            <button class="btn btn-warning btn-sm" @click="exportData" style="margin-right: 5px; cursor: pointer;">
            Export
            </button>
          </li>
        </template>

        <template v-if="role === 'user'">
          <li class="nav-item">
            <form class="form-inline" @submit.prevent="search">
              <input style="width: 220px;" class="form-control-sm " type="search" v-model="searchQuery"
                @keyup.enter="search" placeholder="Search" aria-label="Search" />
            </form>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'cart-page' }">
              <button type="button" class="btn btn-warning btn-sm" style="margin-left: 5px; margin-right: 5px;">
                <i class="bi bi-cart4"></i> Cart
              </button>
            </router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'order-page' }">
              <button type="button" class="btn btn-warning btn-sm" style="margin-right: 5px;">
                Orders
              </button>
            </router-link>
          </li>
        </template>

        <li class="nav-item">
          <button class="btn btn-danger btn-sm" @click="logout" style="cursor: pointer;">
            Logout
          </button>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  props: ["role"],
  data() {
    return {
      searchQuery: "",
      name: this.getName(),
    };
  },
  methods: {
    search() {
      this.$router.push({
        name: "user-dashboard",
        query: { q: this.searchQuery },
      });
    },
    getName() {
      if (this.role === "admin") {
        return "Admin";
      } else if (this.role === "manager") {
        return localStorage.getItem("manager_name");
      } else if (this.role === "user") {
        return localStorage.getItem("user_name");
      }
    },

    getDashboardLink() {
      if (this.role === "admin") {
        return { name: "admin-dashboard" };
      } else if (this.role === "manager") {
        return { name: "manager-dashboard" };
      } else if (this.role === "user") {
        return { name: "user-dashboard" };
      }
    },
    logout() {
      if (this.role === "admin") {
        localStorage.removeItem("admin_token");
      } else if (this.role === "manager") {
        localStorage.removeItem("manager_token");
        localStorage.removeItem("manager_name");
      } else if (this.role === "user") {
        localStorage.removeItem("user_token");
        localStorage.removeItem("user_name");
      }
      this.$router.replace({ name: "login", params: { role: this.role } });
    },
    async exportData() {
      try {
        const url = `http://127.0.0.1:5000/api/product/export`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem('manager_token'),
          },
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert("An error occurred:", error);
        this.$router.push({ name: `manager-dashboard` });
      }
    }
  },
};
</script>

<style scoped>
</style>
