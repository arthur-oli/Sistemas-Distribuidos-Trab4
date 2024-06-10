<template>
  <v-app>
    <v-main>
      <home-app />
    </v-main>
  </v-app>
</template>

<script>
import HomeApp from './components/HomeApp';

export default {
  name: 'App',

  components: {
    HomeApp,
  },

  data: () => ({
    //
  }),
};
</script>
