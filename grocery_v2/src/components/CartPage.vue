<template>
  <navbar role="user"></navbar>
  <div class="content">
    <div class="container mt-5">
      <form @submit.prevent="buyCart">
        <table class="table table-bordered col-12 col-md-10 col-lg-8 " style="max-width: ">
          <thead class="table-dark">
            <tr class="table-info"> 
              <th class="text-center" colspan="5">Your Cart</th>
            </tr>
            <tr>
              <th>Product Name</th>
              <th>Price</th>
              <th>Stock</th>
              <th>Quantity</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(c, i) in cart_products" :key="i">
              <td>
                {{ c[0].product_name }}
              </td>
              <td class="number-b" style="width: 120px">
                <i class="bi bi-currency-rupee"></i>{{ c[0].product_price }}{{ c[0].product_unit }}
              </td>
              <td v-if="c[0].product_stock > 0">{{ c[0].product_stock - c[1] }} </td>
              <td v-else >{{ c[0].product_stock }} </td>

              <td style="width: 200px">
               <div v-if="c[0].product_stock === 0">Out of Stock</div>
                <div v-else class="input-group">
                  <span class="input-group-btn">
                    <button type="button" @click="decreaseQuantity(i)" class="btn btn-sm btn-outline-secondary">
                      -
                    </button>
                  </span>
                  <input type="number" class="form-control form-control-sm text-center" :value="c[1]" 
                  :max="c[0].product_stock" readonly />
                  <span class="input-group-btn">
                    <button type="button" @click="increaseQuantity(i)" class="btn btn-sm btn-outline-secondary"
                    :class="{ disabled: c[0].product_stock === 0 }">
                      +
                    </button>
                  </span> 
                </div>
              </td> 
              <td class="result">
                <span v-if="c[0].product_stock === 0">0</span>
                <span v-else><i class="bi bi-currency-rupee"></i> {{ getTotal(i) }}</span>
              </td>
            </tr> 
          </tbody>
          <tfoot>
            <tr>
              <th colspan="4">Grand Total</th>
              <td class="fw-bold"><i class="bi bi-currency-rupee"></i> {{ grandTotal() }}</td>
            </tr>
          </tfoot>
        </table>
        <button type="submit" class="btn btn-primary" :class="{ disabled: cart_products.length === 0 }">
          Buy Cart
        </button>
      </form>
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
      cart_products: [],
    };
  },
  methods: {
    // Method to increase the quantity of a product
    increaseQuantity(i) {
      if (this.cart_products[i] && this.cart_products[i][0].product_stock > 0 && this.cart_products[i][1] < this.cart_products[i][0].product_stock) {
        this.cart_products[i][1] = this.cart_products[i][1] + 1;
      }
    },

    // Method to decrease the quantity of a product
    decreaseQuantity(i) {
      if (this.cart_products[i] && this.cart_products[i][1] > 1) {
        this.cart_products[i][1] = this.cart_products[i][1] - 1;
      }
    },

    // Method to get the total of a product
    getTotal(i) {
      if (this.cart_products[i] && this.cart_products[i][1] > 0) {
        const total = this.cart_products[i][0].product_price * this.cart_products[i][1];
        return total;
      }
    },

    // Method to get the grand total of the cart_products
    grandTotal() {
      var grand = 0;
      for (let i = 0; i < this.cart_products.length; i++) {
        if (this.cart_products[i] && this.cart_products[i][1] > 0 && this.cart_products[i][0].product_stock > 0) {
          grand = grand + this.cart_products[i][0].product_price * this.cart_products[i][1];
        }
      }
      return grand;
    },

    async buyCart() {
        const formData = new FormData();

        // Loop through the cart_products and append product IDs and quantities to formData
        for (const item of this.cart_products) {
          formData.append(item[0].product_id, item[1]); 
        }
        const response = await fetch(`http://127.0.0.1:5000/api/user/cart/purchase`, {
          method: "POST",
          headers: {
            Authorization: localStorage.getItem("user_token"),
          },
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          if (data.error) {
            alert(data.error);
            this.$router.push({ name: "user-dashboard" });
          } else {
            alert(data.message);
            this.$router.push({ name: "user-dashboard" });
          }
        } else {
          if (response.status === 401) {
            throw new Error("Token is not passed or invalid!");
          }
          if (response.status === 403) {
            throw new Error("User access required!");
          } else {
            throw new Error(response.status);
          }
        }
    },

    async fetchCartProducts(){
        const response = await fetch(`http://127.0.0.1:5000/api/user/cart`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("user_token"),
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.cart_products = data.cart_products;
          console.log(this.cart_products)
        } else {
          if (response.status === 401) {
            throw new Error("Token is not passed or invalid!");
          }
          if (response.status === 403) {
            throw new Error("User access required!");
          } else {
            throw new Error(response.status);
          }
        }
    },
  },
  mounted() {
    this.fetchCartProducts();
  },
};


</script>

<style scoped>

</style>
