<template lang="html">
  <div class="addlogs">
    <div class="row">
      <div class="col-6 offset-3 d-flex justify-content-center">
        <h1>Add a log</h1>
      </div>
      <div class="col-3 d-flex justify-content-center">
        <h3><a href="/logout"> Logout</a></h3>
      </div>
    </div>
    <br />
    <div class="row">
      Debugging:{{ tracker_types }}
      <div class="col-6 offset-3 h5">
        <div class="row">
          <div class="col-6 d-flex ">
            Add logs to Tracker:
          </div>
          <div class="col-6">
            <select id="sel_trk">
                <option class="form-check" v-for="i in get_trackers" :key="i.tracker_id">
                  <input
                    class="form-check-input mx-1"
                    type="radio"
                    :id="i.tracker_id"
                    :value=i.tracker_type
                  />
                  <label :for="i.tracker_id"
                    >{{ i.tracker_name }}-{{ i.tracker_type }}</label
                  >
                </option>
            </select>
          </div>
        </div>
        <div class="row">
          <div class="col-6 d-flex">
            Tracker type: {{ this.sel_tracker.split("-")[0] }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";


export default {
  data() {
    return {
      tracker_id: this.$store.getters.tracker_ids,
      tracker: ""
    };
  },
  methods: {
    refresh() {
      let self = this;
      fetch("http://localhost:5000/api/user/" + self.$store.state.user, {
        method: "GET",
        headers: {
          "A-T":
            self.$Ciphers
              .decode("Vigenere Cipher", self.$cookies.get("user") || "", [
                "Pwd"
              ])
              .split(";")[2] || ""
        }
      })
        .then(response => {
          // console.log(response)
          if (response.ok && !response.redirected) {
            return response.json();
          } else {
            throw {
              e_code: response.status,
              error: response.statusText
            };
          }
        })
        .then(data => {
          for (let i of data.trackers) {
            self.$store.commit("set_tracker", i);
          }
        })
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login");
          self.$router.push("/login"); //remember
        });
    }
  },
  computed: {
    ...mapGetters(["tracker_types", "get_trackers", "tracker_ids"]),
    sel_tracker(){return this.tracker}
  },
  mounted() {
    if (this.$store.getters.tracker_types.length == 0) {
      this.refresh();
    }
    this.tracker=(document.getElementById('sel_trk').value)||"";
  }
};
</script>

<style lang="css" scoped></style>
