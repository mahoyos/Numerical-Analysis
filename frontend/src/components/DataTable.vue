<script>
export default {
  data() {
    return {
      tableHeaders: ['Iteration', 'Xn', 'F(Xn)', 'Error']
    };
  },
  props: {
    tableData: {
      type: Array,
      required: true
    }
  }
};
</script>

<template>
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Data Table Results</h6>
    </div>
    <div class="card-body">
      <table>
        <thead>
          <tr>
            <th v-for="(header, index) in tableHeaders" :key="index">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in tableData" :key="index">
            <td>{{ item.iteration }}</td>
            <td>{{ item.value1 }}</td>
            <td>{{ item.value2 }}</td>
            <td>{{ item.value3 }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 8px;
}

th {
  background-color: #edeaea;
  text-align: left;
}
</style>
