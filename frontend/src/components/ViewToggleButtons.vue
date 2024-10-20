<template>
    <div class="view-toggle-buttons">
      <button
        v-for="mode in modes"
        :key="mode.value"
        @click="selectViewMode(mode.value)"
        :class="{'active': selectedViewMode === mode.value}"
      >
        {{ mode.label }}
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ViewToggleButtons',
    props: {
      value: {
        type: String,
        default: 'Week',
      },
      modes: {
        type: Array,
        default: () => [
          { label: 'Daily View', value: 'Day' },
          { label: 'Weekly View', value: 'Week' },
          { label: 'Monthly View', value: 'Month' },
        ],
      },
    },
    computed: {
      selectedViewMode: {
        get() {
          return this.value;
        },
        set(newValue) {
          this.$emit('input', newValue);
        },
      },
    },
    methods: {
      selectViewMode(mode) {
        this.selectedViewMode = mode;
      },
    },
  };
  </script>
  
  <style scoped>
  .view-toggle-buttons {
    margin-bottom: 10px;
  }
  
  .view-toggle-buttons button {
    margin-right: 5px;
    padding: 5px 10px;
  }
  
  .view-toggle-buttons button.active {
    background-color: #007bff;
    color: white;
  }
  </style>
  