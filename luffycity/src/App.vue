<template>
  <div id="app">
      <luffycity_header></luffycity_header>
      <router-view></router-view>
      <luffycity_footer></luffycity_footer>
  </div>
</template>

<script>
import LuffyCityHeader from './components/LuffyCityHeader/LuffyCityHeader'
import LuffyCityFooter from './components/LuffyCityFooter/LuffyCityFooter'
export default {
  name: 'App',
  components:{
    luffycity_header:LuffyCityHeader,
    luffycity_footer:LuffyCityFooter,
  }
}
</script>

<style>
  * {
    padding: 0;
    margin: 0;
}

ul {
    list-style: none;
}

a {
    text-decoration: none;
}
</style>
