<template>
  <navuser role="user"></navuser>
  <div class="content">
    <div class="container mt-5">
      <table class="table table-bordered">
        <thead>
          <tr class="table-info"> 
              <th class="text-center" colspan="6">Your Orders</th>
          </tr>
          <tr class="table-dark">
            <th>Product</th>
            <th>Quantity</th>
            <th>Date</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in orders" :key="orders.order_id">
            <td>{{ order.order_name }}</td>
            <td>{{ order.order_quantity }}</td>
            <td>{{ order.order_date }}</td>
            <td style="white-space: nowrap;"><i class="bi bi-currency-rupee"></i>{{ order.order_total }}</td>
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
    navuser: RoleNavbar,
  },
  data() {
    return {
      orders: [],
    };
  },
  methods: {
    async fetchOrders() {
        const url = `http://127.0.0.1:5000/api/user/orders`;
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: localStorage.getItem("user_token"),
          },
        });
        const data = await response.json();
        if (response.ok) {
          this.orders = data.orders;
        } else {
          alert(data.message);
          this.$router.push({ name: "home" });
        }
    },
  },
  mounted() {
    this.fetchOrders();
  },
};
</script>

