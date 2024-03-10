<template>
    <nav class="navbar navbar-expand-md navbar-primary bg-primary">
        <span class="text-white fw-bold fs-4" style="margin-left: 10px;"><i class="bi bi-bag-heart"></i> GroceryShop</span>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav" style="margin-right: 5px;">
          <li class="nav-item">
            <router-link :to="{ name: 'login', params: { role: 'user' } }" class="btn btn-warning me-2 mb-2 mb-md-0">User</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'login', params: { role: 'manager' } }" class="btn btn-warning me-2 mb-2 mb-md-0">Manager</router-link>
          </li>
          <li class="nav-item">
            <router-link :to="{ name: 'login', params: { role: 'admin' } }" class="btn btn-warning">Admin</router-link>
          </li>
        </ul>
      </div>
    </nav>
  </template>

<script>
export default {
};
</script>