<script setup>
// eslint-disable-next-line no-unused-vars
import { RouterView, RouterLink } from 'vue-router'

</script>

<template>
  <div>
    <div >
      <RouterView />
    </div>
  </div>
</template>

<style>
/* removing body margins */
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  overflow-x: hidden;
}

#app {
  margin: 0;
  padding: 0;
  width: 100%;
  min-height: 100vh;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}
</style>
