<template lang="html">
  <div class="addlogs">
    <div class="row">
      <div class="col col-sm-6 offset-sm-3 d-flex justify-content-center">
        <h1>Update a log</h1>
      </div>
      <br />
    </div>
    <br />
    <div class="row">
      <div class="col col-sm-6 offset-sm-3 h5 ">
        <div class="row m-3">
          <div class="col-6 ">
            Tracker:
          </div>
          <div class="col-6">
            <router-link
              :to="{ name: 'dash.tracker', params: { id: tracker.tracker_id } }"
              >{{ tracker.tracker_name }}</router-link
            >
          </div>
        </div>
        <div class="row m-3">
          <div class="col-6">
            Tracker type:
          </div>
          <div class="col-6">
            {{ tracker.tracker_type }}
          </div>
        </div>
        <div class="row m-3">
          <div class="col-6 ">
            Logged datetime
          </div>
          <div class="col-6">
            <input
              class="form-control"
              type="text"
              id="log_datetime"
              :value="log.log_datetime | date_format"
            />
            <button
              class="btn btn-outline-info"
              type="button"
              name="button"
              @click="update_dt"
            >
              @
            </button>
          </div>
        </div>
        <!-- ############# -->
        <div class="row m-3" v-if="tracker.tracker_type === 'Integer'">
          <div class="col-6">
            <label for="log_val">Log value</label>
          </div>
          <div class="col-6">
            <input
              class="form-control"
              type="Number"
              id="log_val"
              name="log_val"
              placeholder="Int"
              :value="log.log_value"
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
              :value="log.log_value"
              required
            />
          </div>
        </div>

        <div class="row m-3" v-if="tracker.tracker_type === 'Time'">
          <div class="col-6">
            <label for="log_val">Log value</label>
          </div>
          <div class="col-6">
            <input id="log_val" type="text" :value="log.log_value" />
            <button
              class="btn btn-outline-danger"
              id="start"
              @click="stopwatch().start()"
            >
              Start
            </button>
            <button
              class="btn btn-outline-danger"
              id="reset"
              @click="stopwatch().reset()"
            >
              Reset
            </button>
          </div>
        </div>

        <div class="row m-3" v-if="tracker.tracker_type === 'Multiple-choice'">
          <div class="col-6">
            <label for="log_val">Log value</label>
          </div>
          <div class="col-6">
            <select id="log_val" name="log_val" :value="log.log_value">
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
            Update note
          </div>
          <div class="col-6">
            <textarea
              class="form-control"
              id="log_note"
              name="note"
              placeholder="Note/Remark"
              :value="log.note"
            ></textarea>
          </div>
        </div>
        <div class="row m-3 ">
          <div class="col d-flex justify-content-center">
            <button
              class="btn btn-outline-secondary"
              type="submit"
              name="button"
              @click="postlog"
            >
              Submit
            </button>
            <div id="error"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import stopwatch from "@/scripts/stopwatch.js";

export default {
  data() {
    return {
      tracker: "",
      log: "",
      log_id: this.$route.params.id || "",
      time: "00:00:00"
    };
  },
  methods: {
    refresh() {
      let self = this;
      var l = fetch(
        process.env.VUE_APP_BACKEND_URL + "api/log/" + self.log_id,
        {
          method: "GET",
          headers: {
            "A-T":
              self.$Ciphers
                .decode("Vigenere Cipher", self.$cookies.get("user") || "", [
                  "Pwd"
                ])
                .split(";")[2] || ""
          }
        }
      );
      l.then(response => {
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
          console.log(data);
          self.log = data;
        })
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login");
        })
        .then(() => {
          if (self.log != "" && self.log !== null) {
            console.log("getting tracker");
            fetch(
              process.env.VUE_APP_BACKEND_URL +
                "api/tracker/" +
                self.log.tracker_id,
              {
                method: "GET",
                headers: {
                  "A-T":
                    self.$Ciphers
                      .decode(
                        "Vigenere Cipher",
                        self.$cookies.get("user") || "",
                        ["Pwd"]
                      )
                      .split(";")[2] || ""
                }
              }
            )
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
                // console.log(data);
                self.tracker = data;
              })
              .catch(rej => {
                console.log(rej);
                console.log(rej.error + " kindly re-login");
              });
          }
        });
    },
    stopwatch: function() {
      return stopwatch;
    },
    postlog() {
      //----Validation------
      if (
        document.getElementById("log_val") === null ||
        document.getElementById("log_val").value === ""
      ) {
        document.getElementById("error").innerHTML = "Enter log value";
        return null;
      } else if (document.getElementById("log_note") === null) {
        console.log("note element missing");
        return null;
      } else {
        document.getElementById("error").innerHTML = "";
      }
      //#------validation--------

      let datetime = document.getElementById("log_datetime").value;

      console.log(datetime);
      let data = {
        log_value: document.getElementById("log_val").value,
        log_datetime: datetime,
        log_note: document.getElementById("log_note").value
      };

      fetch(process.env.VUE_APP_BACKEND_URL + "api/log/" + this.log.log_id, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "A-T":
            this.$Ciphers
              .decode("Vigenere Cipher", this.$cookies.get("user") || "", [
                "Pwd"
              ])
              .split(";")[2] || ""
        },
        body: JSON.stringify(data)
      })
        .then(response => {
          if (response.ok && !response.redirected) {
            alert("Updated");
          } else {
            throw {
              e_code: response.status,
              error: response.statusText
            };
          }
        })
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login"); //remember
        });
    },
    update_dt() {
      let currentdate = new Date();
      let mstr = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
      ];
      let datetime =
        currentdate.getDate() +
        "/" +
        mstr[currentdate.getMonth()] +
        "/" +
        currentdate.getFullYear() +
        ", " +
        currentdate.getHours() +
        ":" +
        currentdate.getMinutes() +
        ":" +
        currentdate.getSeconds() +
        "." +
        currentdate.getMilliseconds();

      document.getElementById("log_datetime").value = datetime;
    }
  },
  computed: {
    ...mapGetters(["tracker_types", "get_trackers", "tracker_ids"]),
    get_tracker() {
      return this.tracker;
    }
  },
  mounted() {
    if (this.tracker.length == 0) {
      this.refresh();
    }
  }
};
</script>

<style lang="css" scoped>
input {
  padding: 0px;
}
</style>
