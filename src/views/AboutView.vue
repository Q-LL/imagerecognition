<template>
  <div class="markdown">
    <v-md-preview :text="markdown"></v-md-preview>
  </div>
</template>

<script>
import mdoc from 'raw-loader!../markdown/timeline.md';


export default {
  data() {
    return {
      markdown: mdoc,
    };
  },
};
</script>

<style>
.markdown {
  width: 98vw;
}
</style>