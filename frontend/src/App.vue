<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
        <RouterLink to = "/staffrequests"> View own requests</RouterLink>
      </nav>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  position: fixed; /* Stays in place even when you scroll */
  top: 0;         /* Aligns to the top of the screen */
  left: 0;        /* Aligns to the left of the screen */
  padding: 10px;  /* Adds some padding for spacing */
  background-color: #f8f9fa; /* Optional background color */
  width: 100%;    /* Set the width if needed */
  z-index: 1000;  /* Ensures it's on top of other elements */
}

</style>
