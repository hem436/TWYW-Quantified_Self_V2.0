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
              <option v-for="i of get_trackers" :key="i.tracker_id" :value="i">{{ i.tracker_name }}-{{ i.tracker_type }}
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
            <input id="log_val" type="text" :value="time" />
            <button id="start" @click="stopwatch().start()">Start</button>
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
              id="log_note"
              name="note"
              placeholder="Note/Remark"
            ></textarea>
          </div>
        </div>
        <div class="row m-3 ">
          <div class="col d-flex justify-content-center">
            <button type="submit" name="button" @click='postlog'>Submit</button>
            <div id="error">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import stopwatch from "@/assets/stopwatch.js";

export default {
  data() {
    return {
      tracker: "",
      tracker_id:this.$route.params.id||"",
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
      return stopwatch;
    },
    postlog(){
      //----Validation------
      if(this.tracker===""){
        document.getElementById('error').innerHTML="Select Tracker first"
        return null;
      }
      else if (document.getElementById('log_val')===null || document.getElementById('log_val').value==="") {
        document.getElementById('error').innerHTML="Enter log value";
        return null;
      }
      else if(document.getElementById('log_note')===null){
        console.log("note element missing");
        return null;

      }
      else{
        document.getElementById('error').innerHTML="";
      }
      //#------validation--------
      let currentdate = new Date();
      let mstr=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
let datetime = currentdate.getDate() + "/"
                + mstr[(currentdate.getMonth())] + "/"
                + currentdate.getFullYear()+", "
                + currentdate.getHours() + ":"
                + currentdate.getMinutes() + ":"
                + currentdate.getSeconds()+"."
                +currentdate.getMilliseconds();
      console.log(datetime)
      let data={
        'tracker_id':this.tracker.tracker_id,
        'log_value':document.getElementById('log_val').value,
      'log_datetime':datetime,
      'log_note':document.getElementById('log_note').value
    }

      fetch("http://localhost:5000/api/log", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "A-T":
            this.$Ciphers
              .decode("Vigenere Cipher", this.$cookies.get("user") || "", [
                "Pwd"
              ])
              .split(";")[2] || ""
        },
        body:JSON.stringify(data)
      })
        .then(response => {
          if (response.ok && !response.redirected) {
            alert("Logged")
          } else {
            throw {
              e_code: response.status,
              error: response.statusText
            };
          }
        })
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login");
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
