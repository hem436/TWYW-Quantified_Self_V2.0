<template lang="html">
  <div class="addlogs">
    <div class="row">
      <div class="col-sm-3 d-flex justify-content-center">
        <span class="align-self-center"><img src='/assets/userimg.png' width="40px" height="40px" /></span>
      </div>
      <div class="col-sm-6 d-flex justify-content-center">
        <h1>Add a log</h1>
      </div>
      <div class="col-sm-3 d-flex justify-content-center">
        <h3><a href="/logout"> Logout</a></h3>
      </div>
    </div><br>
    <div class="log">
      {{tracker_types}}
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
  data(){
    return {tracker_id:this.$store.getters.tracker_ids}
  },
  computed:{
    ...mapGetters([
    'tracker_types',
    'get_trackers',
    'tracker_ids'
  ])

  }
}
</script>

<style lang="css" scoped>
</style>
