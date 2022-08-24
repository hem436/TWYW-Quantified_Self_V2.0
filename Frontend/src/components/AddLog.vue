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
      <div class="col-6 offset-3  d-flex justify-content-center">
        <div class="row">
          <div class="col-6 offset-3 d-flex justify-content-center">
            <div class="dropdown">
              <a
                class="btn  dropdown-toggle "
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                data-bs-display="static"
                aria-expanded="false"
              >
                <label class="h5" for="checkbox"
                  >Select Trackers to add logs:
                </label>
                <input id="checkbox" type="text" name="form-control" value="" />
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li class="" v-for="i in get_trackers" :key="i.tracker_id">
                  <input
                    class="form-check-input mx-1"
                    type="checkbox"
                    :id="i.tracker_id"
                  />
                  <label :for="i.tracker_id"
                    >{{ i.tracker_name }}-{{ i.tracker_type }}</label
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col d-flex justify-content-center">
            Tracker type: {{ this.tracker_type }}
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
      tracker_type: ""
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
    ...mapGetters(["tracker_types", "get_trackers", "tracker_ids"])
  },
  mounted() {
    if (this.$store.getters.tracker_types.length == 0) {
      this.refresh();
    }
  }
};
</script>

<style lang="css" scoped></style>
