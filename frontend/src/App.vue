<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <header>
    <div class="wrapper">
      <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#">
                  <RouterLink to="/">Home</RouterLink>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/team-schedule">My Team Schedule</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/staff-requests"> (staff) View own requests</RouterLink>
                </a>
              </li>

              <li class="nav-item">
                <a class="nav-link" href="#">
                  <RouterLink to="/manager-schedule"> (M/D) View staff requests</RouterLink>
                </a>
              </li>

            </ul>
            <form class="d-flex" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
          </div>
        </div>
      </nav>
    </div>
  </header>



  <RouterView />
</template>
