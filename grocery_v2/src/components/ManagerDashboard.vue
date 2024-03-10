<template>
  <navbar role="manager"></navbar>
  <div class="content">
    <div class="container mt-5">
      <table class="table table-bordered border-primary">
        <!-- Categories Table -->
        <thead>
          <tr class="table-dark">
            <th class="fs-5 text-center" colspan="4">
              Categories
              <router-link :to="{ name: 'add-category', params: { role: 'manager' } }">
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
              <router-link :to="{ name: 'add-product', params: { categoryId: category.category_id } }">
                <button type="button" class="btn btn-primary btn-sm">
                  <i class="bi bi-plus-circle-fill"></i>
                </button>
              </router-link>
            </td>
            <td style="width: 50px">
              <!-- Update category button -->
              <router-link :to="{ name: 'update-category', params: { Id: category.category_id, role: 'manager' } }">
                <button type="button" class="btn btn-success btn-sm">
                  <i class="bi bi-pencil-square"></i>
                </button>
              </router-link>
            </td>
            <td style="width: 50px">
              <!-- Delete category button -->
              <router-link :to="{ name: 'confirm-delete', params: { Id: category.category_id, role: 'manager', type: 'category' } }">
                <button type="button" class="btn btn-danger btn-sm">
                  <i class="bi bi-trash3"></i>
                </button>
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>

      <table class="table table-bordered border-primary">
        <thead>
          <tr class="table-dark">
            <th>Product</th>
            <th>Category</th>
            <th>Description</th>
            <th>Price</th>
            <th>Stock</th>
            <th class="text-center" colspan="2">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.product_id" class="table-warning">
            <td>{{ product.product_name }}</td>
            <td>{{ product.category_name }}</td>
            <td class="text-wrap text-break">{{ product.product_description }}</td>
            <td style="white-space: nowrap;"><i class="bi bi-currency-rupee"></i>{{ product.product_price }}{{ product.product_unit }}</td>
            <td>{{ product.product_stock }}</td>
            <td style="width: 50px;">
              <router-link :to="{ name: 'update-product', params: { productId: product.product_id } }">
                <button type="button" class="btn btn-success btn-sm"><i class="bi bi-pencil-square"></i></button>
              </router-link>
            </td>
            <td style="width: 50px;">
              <router-link :to="{ name: 'confirm-delete', params: { role: 'manager', Id: product.product_id, type: 'product' } }">
                <button type="button" class="btn btn-danger btn-sm"><i class="bi bi-trash3"></i></button>
              </router-link> 
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
      products: [],
    };
  },
  mounted() {
    this.fetchCategories();
    this.fetchProducts();
  },
  methods: {
    async fetchCategories() {
        const url = `http://127.0.0.1:5000/api/category`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("manager_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.categories = data.categories;
        } else {
          alert(data.message);
          this.$router.push({ name: "role-auth" , params: { role: 'manager' }});
        }
    },

    async fetchProducts() {
      const url = `http://127.0.0.1:5000/api/product`;
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: localStorage.getItem("manager_token"),
        },
      });
      const data = await response.json();
      if (response.ok) {
        this.products = data.products;
        console.log(this.products)
      } else {
        alert(data.message);
        this.$router.push({ name: "role-auth" , params: { role: 'manager' }});
      }
    },
  },
};
</script>

<style scoped>
</style>
