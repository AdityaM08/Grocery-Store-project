<template>
  <navbar role="user"></navbar>
  <div class="content">
    <div class="container mt-5">
      <template v-if="products.length === 0">
        <h3>No product found.</h3>
      </template>
      <template v-else>
        <table class="table table-bordered border-primary">
        <thead>
          <tr class="table-info"> 
              <th class="text-center" colspan="6">Products</th>
          </tr>
          <tr class="table-dark">
            <th>Product</th>
            <th>Category</th>
            <th>Description</th>
            <th>Price</th>
            <th>Stock</th>
            <th class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.product_id" class="table-warning">
            <td>{{ product.product_name }}</td>
            <td>{{ product.category_name }}</td>
            <td class="text-wrap text-break">{{ product.product_description }}</td>
            <td style="white-space: nowrap;"><i class="bi bi-currency-rupee"></i>{{ product.product_price }}{{ product.product_unit }}</td>
            <td>{{ product.product_stock }}</td>
            <td style="width: 115px;">
              <button
                v-if="product.product_stock > 0"
                @click="addToCart(product.product_id)"
                class="btn btn-sm btn-warning float-end">Add to Cart
              </button>   
              <button v-else
                class="btn btn-sm btn-danger float-end">Out of Stock
              </button>  
            </td>
          </tr>
        </tbody>
      </table>
      </template>
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
      products: [],
    };
  },
  methods: {
    getUrl() {
      if (this.$route.query.q) {
        return `http://127.0.0.1:5000/api/product?q=${this.$route.query.q}`
      } else {
        return `http://127.0.0.1:5000/api/product`
      }
    },
    async addToCart(id) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/user/cart/${id}`, {
          method: "POST",
          headers: {
            Authorization: localStorage.getItem("user_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
            alert(data.message);
        } else {
          alert(data.message);
        }
      } catch (error) {
        alert(error.message);
        this.$router.push({ name: "user-dashboard" });
      }
    },

    async fetchProducts() {
        const url = this.getUrl();
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("user_token")
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.products = data.products;
        } else {
          alert(data.message);
          this.$router.push({ name: "login", params: { role: 'user' } });
        }
    },
  },
  mounted() {
    this.fetchProducts()
  },
  watch: {
    // Watch for changes in the query object of the route
    '$route.query.q': {
      handler(newQuery, oldQuery) {
        // Check if the query has changed
        if (JSON.stringify(newQuery) !== JSON.stringify(oldQuery)) {
          this.fetchProducts()
        }
      },
      deep: true // Watch for nested changes in the query object
    }
  }
};
</script>
  
<style scoped></style>

  