<template>
  <div>
    <h1>请SUPER_ADMIN用户直接操作数据库</h1>
  </div>
</template>

<script>
export default {
  name: 'user',
  data () {
    return {
      username: localStorage.username || sessionStorage.username,
      token: localStorage.token || sessionStorage.token,
    }
  },
  mounted () {
    if (this.username !== 'admin' || !this.token) {
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>

</style>
