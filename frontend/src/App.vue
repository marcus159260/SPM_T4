<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <header>

    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/team-schedule">My Team Schedule</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>
