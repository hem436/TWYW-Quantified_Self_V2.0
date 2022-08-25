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
      <div class="col-6 offset-3 h5 ">
        <div class="row m-3">
          <div class="col-6 ">
            Add log to Tracker:
          </div>
          <div class="col-6">
            <select
              id="sel_trk"
              class="sel_trk"
              name="sel_trk"
              v-model="tracker"
            >
              <option v-for="i of get_trackers" :key="i.tracker_id" :value="i"
                >{{ i.tracker_name }}-{{ i.tracker_type }}
              </option>
            </select>
          </div>
        </div>
        <div class="row m-3">
          <div class="col-6">
            Tracker type:
          </div>
          <div class="col-6">
            {{ this.tracker.tracker_type }}
          </div>
        </div>
        <!-- ############# -->
        <div class="row m-3" v-if="tracker.tracker_type === 'Integer'">
          <div class="col-6">
            <label for="log_val">Log value</label>
          </div>
          <div class="col-6">
            <input
              type="Number"
              id="log_val"
              name="log_val"
              placeholder="Int"
              required
            />
          </div>
        </div>

        <div class="row m-3" v-if="tracker.tracker_type === 'Numeric'">
          <div class="col-6">
            <label for="log_val">Log value</label>
          </div>
          <div class="col-6">
            <input
              type="Number"
              id="log_val"
              name="log_val"
              step="0.000001"
              placeholder="Float"
              required
            />
          </div>
        </div>

        <div class="row m-3" v-if="tracker.tracker_type === 'Time'">
          <div class="col-6">
            <label for="log_val">Log value</label>
          </div>
          <div class="col-6">
            <div id="timer"></div>
            <input id="time" type="text" :value="time" />
            <button id="start" @click="stopwatch()">Start</button>
            <button id="stop" @click="stopwatch()">Start</button>

            <button id="reset" @click="stopwatch().reset()">Reset</button>
          </div>
        </div>

        <div class="row m-3" v-if="tracker.tracker_type === 'Multiple-choice'">
          <div class="col-6">
            <label for="log_val">Log value</label>
          </div>
          <div class="col-6">
            <select id="log_val" name="log_val">
              <option
                v-for="(item, index) in tracker.settings.split(',')"
                :key="index"
                >{{ item }}</option
              >
            </select>
          </div>
        </div>
        <!-- ####### -->
        <div class="row m-3">
          <div class="col-6">
            Enter a note
          </div>
          <div class="col-6">
            <textarea
              id="note"
              name="note"
              placeholder="Note/Remark"
            ></textarea>
          </div>
        </div>
        <div class="row m-3 ">
          <div class="col d-flex justify-content-center">
            <button type="button" name="button">Submit</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import stopwatch from "@/assets/stopwatch.js";
console.log(stopwatch);
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      tracker: this.$route.params.id || "",
      time: "00:00:00"
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
    },
    stopwatch: function() {
      // var hour = 0,
      //   sec = 0,
      //   min = 0;
      // var dispHour = 0,
      //   dispMin = 0,
      //   dispSec = 0;
      // var timeoutId = null;
      // return {
      //   timer: function() {
      //     sec++;
      //     if (sec / 60 == 1) {
      //       min++;
      //       sec = 0;
      //       if (min / 60 == 1) {
      //         hour++;
      //         min = 0;
      //       }
      //     }
      //     if (sec < 10) {
      //       dispSec = "0" + sec.toString();
      //     } else {
      //       dispSec = sec.toString();
      //     }
      //     if (min < 10) {
      //       dispMin = "0" + min.toString();
      //     } else {
      //       dispMin = min.toString();
      //     }
      //     if (hour < 10) {
      //       dispHour = "0" + hour.toString();
      //     } else {
      //       dispHour = hour.toString();
      //     }
      //     document.getElementById("timer").innerHTML =
      //       dispHour + ":" + dispMin + ":" + dispSec;
      //   },
      //   start: function() {
      //     console.log("watch");
      //     timeoutId = window.setInterval(this.timer, 1000);
      //     document.getElementById("start").innerHTML = "Stop";
      //   },
      //   stop: function() {
      //     window.clearInterval(timeoutId);
      //     document.getElementById("start").innerHTML = "Start";
      //   },
      //   reset: function() {
      //     window.clearInterval(timeoutId);
      //     (sec = 0), (min = 0), (hour = 0);
      //     document.getElementById("timer").innerHTML = "00:00:00";
      //     document.getElementById("start").innerHTML = "Start";
      //   }
      // };
      return stopwatch.start();
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
