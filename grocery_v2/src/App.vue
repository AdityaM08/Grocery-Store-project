<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <RouterView />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 30px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

body {
  overflow-y: hidden;
  overflow-x: scroll;
  background: aliceblue;

}

.auth-container {
    background-color: #f7f7f7; 
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    /* max-width: 400px; */
    margin: 0 auto;
    margin-top: 50px;
}

.content {
  padding-left: 32px;
  padding-right: 32px;
  padding-bottom: 100px;
  min-height: 100vh;
  max-height: 100vh;
  overflow: auto;
  display: flex;
  flex-wrap: wrap;
}

.container {
  margin: auto;
}

#pdp{
  min-height: 72px;
  max-height: 72px;
  overflow: auto;
}
</style>
