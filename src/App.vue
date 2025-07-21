<template>
  <div id="app">
    <!--
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </nav>
    -->
    <router-view/>
  </div>
</template>

<script>
  export default{
    name:'App',
    components:{},
    data(){
      return{
        user:JSON.parse(sessionStorage.getItem('CurUser'))
      }
    
    },
    watch:{
      '$store.state.menu':{
        handler(val,old) {
          if(!old && this.user && this.user.username){
            this.$store.commit("setRouter",val)
          }
        },
        immediate:true
      }
    }
  }
</script>

<style lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100%;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
