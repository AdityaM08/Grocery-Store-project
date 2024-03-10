import { createRouter, createWebHistory } from "vue-router";
import RoleAuthForm from "../components/RoleAuthForm.vue";
import AdminDashboard from "../components/AdminDashboard.vue";
import ManagerDashboard from "../components/ManagerDashboard.vue";
import UserDashboard from "../components/UserDashboard.vue";
import CategoryForm from "../components/CategoryForm.vue";
import ProductForm from "../components/ProductForm.vue";
import ConfirmDelete from "../components/ConfirmDelete.vue";
import CartPage from "../components/CartPage.vue";
import OrderPage from "../components/OrderPage.vue";


const routes = [
  {
    path: "/",
    name: "RoleAuthForm",
    component: RoleAuthForm,
    props: (route) => ({ isLogin: true, role: 'user' })
  },
  {
    path: "/auth/:role/login",
    name: "login",
    component: RoleAuthForm,
    props: (route) => ({ isLogin: true, role: route.params.role }),
  },
  {
    path: "/auth/:role/signup",
    name: "signup",
    component: RoleAuthForm,
    props: (route) => ({ isLogin: false, role: route.params.role }),
  },
  {
    path: "/admin/dashboard",
    name: "admin-dashboard",
    component: AdminDashboard,
  },
  {
    path: "/manager/dashboard",
    name: "manager-dashboard",
    component: ManagerDashboard,
  },
  {
    path: "/user/dashboard",
    name: "user-dashboard",
    component: UserDashboard,
  },
  {
    path: "/:role/add-category",
    name: "add-category",
    component: CategoryForm,
    props: (route) => ({
      isUpdate: false,
      role: route.params.role,
    }),
  },
  {
    path: "/:role/update-category/:Id",
    name: "update-category",
    component: CategoryForm,
    props: (route) => ({
      isUpdate: true,
      Id: parseInt(route.params.Id),
      role: route.params.role,
    }),
  },
  {
    path: "/:role/delete/:type/:Id",
    name: "confirm-delete",
    component: ConfirmDelete,
    props: (route) => ({
      Id: route.params.Id,
      type: route.params.type,
      role: route.params.role,
    }),
  },
  {
    path: "/manager/add-product/:categoryId",
    name: "add-product",
    component: ProductForm,
    props: (route) => ({
      isUpdate: false,
      categoryId: parseInt(route.params.categoryId),
    }),
  },

  {
    path: "/manager/update-product/:productId",
    name: "update-product",
    component: ProductForm,
    props: (route) => ({
      isUpdate: true,
      productId: parseInt(route.params.productId),
    }),
  },

  {
    path: "/user/cart",
    name: "cart-page",
    component: CartPage,
  },
  {
    path: "/user/orders",
    name: "order-page",
    component: OrderPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});
export default router;
