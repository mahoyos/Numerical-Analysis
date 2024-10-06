<script setup lang="ts">
interface BreadCrumbItem {
  title: string;
  route: string;
}

defineProps<{
  breadCrumbList: BreadCrumbItem[];
}>();
</script>

<template>
  <nav aria-label="breadcrumb" class="breadcrumb-font">
    <ol class="breadcrumb">
      <li class="breadcrumb-item" v-for="breadCrumb in breadCrumbList" :key="breadCrumb.title" aria-current="page">
        <template v-if="breadCrumb.route != ''">
          <router-link :to="breadCrumb.route">
            {{ breadCrumb.title }}
          </router-link>
        </template>
        <template v-else>
          {{ breadCrumb.title }}
        </template>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  padding: 12px 16px;
  margin-bottom: 16px;
  list-style: none;
  background-color: #eaecf4;
  border-radius: 5px;
}

.breadcrumb-item {
  color: #858796;
}
</style>
