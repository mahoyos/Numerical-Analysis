<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';

function hideSidebar() {
  const body = document.querySelector('body');
  if (body) {
    body.classList.toggle('sidebar-toggled');
  }

  const sidebar = document.querySelector('.sidebar');
  if (sidebar) {
    sidebar.classList.toggle('toggled');
  }

  const mainIcon = document.querySelector('#main-icon');
  if (mainIcon) {
    mainIcon.classList.toggle('display-icon-yes');
  }

  const mainText = document.querySelector('#main-text');
  if (mainText) {
    mainText.classList.toggle('d-none');
  }
}
</script>

<template>
  <!-- Sidebar -->
  <ul class="navbar-nav sidebar sidebar-dark accordion" id="accordionSidebar">

    <router-link to="/">
      <a class="sidebar-brand d-flex align-items-center justify-content-center">
        <div id="main-icon" class="sidebar-brand-icon rotate-n-15 display-icon">
          Calc
        </div>
        <div id="main-text" class="sidebar-brand-text mx-3">Calculator</div>
      </a>
    </router-link>

    <hr class="sidebar-divider my-0 hr-nav-top">

    <li class="nav-item">
      <router-link to="/" class="nav-link">
        <i class="fas fa-fw fa-home"></i>
        <span>Home</span>
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/non-linear-equations" class="nav-link">
        <i class="fas fa-fw fa-tachometer-alt"></i>
        <span>Non-Linear Equations</span>
      </router-link>
    </li>

    <li class="nav-item">
      <router-link to="/equations-systems" class="nav-link pad-0">
        <i class="fas fa-fw fas fa-globe"></i>
        <span>Equations Systems</span>
      </router-link>
    </li>

    <hr class="sidebar-divider my-0 hr-nav-top mt-2">

    <div class="text-center d-none d-md-inline mt-2">
      <button @click="hideSidebar" class="rounded-circle border-0" id="sidebarToggle"></button>
    </div>
  </ul>
  <!-- Sidebar -->

  <div id="content-wrapper" class="d-flex flex-column">
    <!-- Main Content -->
    <div id="content" class="ms-2 me-2">
      <div id="page-content" class="container-fluid mar20">
        <div class="row">
          <div class="col-lg-12">
            <RouterView />
          </div>
        </div>
      </div>
    </div>
    <!-- Main Content -->

    <!-- Footer -->
    <footer class="sticky-footer bg-white">
      <div class="container my-auto">
        <div class="copyright text-center my-auto"><span>Author Reserved © <a href="#"
              target="_blank">Numerical Analysis Calculator</a> 2024</span></div>
      </div>
    </footer>
    <!-- Footer -->
  </div>
</template>

<style>
.mar20 {
  margin-top: 20px;
}

#map-leaflet {
  height: 450px;
}
</style>
