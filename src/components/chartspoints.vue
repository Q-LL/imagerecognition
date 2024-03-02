<template>
  <div>
    <div id="charts"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist'
export default {
  props: {
    ponints: null,
    linexy: null,
    line: null,
  },

  mounted() {
    // this.line = {
    //   x:{
    //     type: 'function',
    //     func: 'return linexy[0]*x+linexy[1];',
    //   },
    //   type: 'scatter',
    // };
    Plotly.newPlot('charts', this.ponints, {}, { modeBarButtonsToRemove: ['select2d', 'lasso2d'], displaylogo: false });
  },

  watch: {
  },

  methods: {
    
  }
}
</script>

<style scoped></style>