<template>
  <navbar role="manager"></navbar>
  <div class="content">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-12 col-md-5 col-lg-4 auth-container">
          <h2 class="text-center">
            {{ isUpdate ? "Edit Product" : "Create Product" }}
          </h2>
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label for="productName" class="form-label">Product Name</label>
              <input
                type="text"
                class="form-control"
                name="name"
                v-model="product.product_name"
                required
              />
            </div>
            <div class="mb-3">
              <label for="productName" class="form-label">Description</label>
              <textarea
                type="text"
                class="form-control"
                name="description"
                v-model="product.product_description"
              ></textarea>
            </div>
            <div class="mb-3">
              <label for="stock" class="form-label">Stock</label>
              <input
                type="number"
                class="form-control"
                name="stock"
                v-model="product.product_stock"
                required
                min="0"
                step="1"
              />
            </div>
            <div class="row mb-3">
              <div class="col-6">
              <label for="price" class="form-label">Price</label>
              <input
                type="number"
                class="form-control"
                name="price"
                v-model="product.product_price"
                required
                min="0"
                step="1"
              />
            </div>
              <div class="col-6">
                <label for="unit" class="form-label">Unit</label>
                <select id="unit" v-model="product.product_unit" class="form-control" required>
                  <option value="/kg">Per kilogram</option>
                  <option value="/unit">Per unit</option>
                  <option value="/gm">Per gram</option>
                  <option value="/liter">Per litre</option>
                </select>
              </div>
            </div>
            <button type="submit" class="btn btn-primary btn-block">
              {{ isUpdate ? "Edit" : "Create" }}
            </button>
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
    categoryId: Number,
    productId: Number,
  },
  data() {
    return {
      product: {
        product_description: "",
        product_name: "",
        product_stock: 0,
        product_price: 0,
        product_unit: "/unit",
      }
    };
  },
  computed: {
    isUpdate() {
      return !!this.productId;
    },
  },
  methods: {
    handleSubmit() {
      if (this.isUpdate) {
        this.updateProduct();
      } else {
        this.addProduct();
      }
    },
    async addProduct() {
        const url = `http://127.0.0.1:5000/api/product/${this.categoryId}`;
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("manager_token"),
          },
          body: JSON.stringify({
            name: this.product.product_name,
            description: this.product.product_description,
            stock: this.product.product_stock,
            price: this.product.product_price,
            unit: this.product.product_unit,
          }),
        });

        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push({ name: "manager-dashboard" });
        } else {
          alert(data.message);
          this.$router.push({ name: "manager-dashboard" });
        }
    },

    async updateProduct() {
        const url = `http://127.0.0.1:5000/api/product/${this.productId}`;
        const response = await fetch(url, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("manager_token"),
          },
          body: JSON.stringify({
            name: this.product.product_name,
            description: this.product.product_description,
            stock: this.product.product_stock,
            price: this.product.product_price,
            unit: this.product.product_unit,
          }),
        });

        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push({ name: "manager-dashboard" });
        } else {
          alert(data.message);
          this.$router.push({ name: "manager-dashboard" });
        }
    },

    async fetchProductData() {
        const url = `http://127.0.0.1:5000/api/product?id=${this.productId}`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("manager_token"),
          },
        });

        const data = await response.json();
        if (response.ok) {
          this.product = data.product
          // this.name = data.product.name;
          // this.price = data.product.price;
          // this.stock = data.product.stock;
          // this.unit = data.product.unit;
          // this.description = data.product.description;
        } else {
          alert(data.message);
          this.$router.push({ name: "manager-dashboard" });
        }
    },
  },
  mounted() {
    if (this.isUpdate) {
      this.fetchProductData();
    }
  },
};
</script>
