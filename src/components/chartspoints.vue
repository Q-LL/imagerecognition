<template>
  <div>
    <div id="charts" class="charts"></div>
  </div>
</template>

<script>
var layout = {
  width: 800, // 画布宽度
  height: 600, 
};
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
    Plotly.newPlot('charts', this.ponints, layout, { modeBarButtonsToRemove: ['select2d', 'lasso2d'], displaylogo: false });
  },

  watch: {
  },

  methods: {
    
  }
}
</script>

<style scoped>
  .charts {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  </style>