<template>
  <div class="trackdetail">
    <div class="row">
      <div
        class="col-sm-10 offset-sm-1 col-lg-8 offset-lg-2 justify-content-center"
      >
        <div class="container mb-5">
          <div class="chart" id="myChart"></div>
        </div>

        <div class="h4 d-flex ">Log Entries</div>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>S.no</th>
                <th>Timestamp</th>
                <th>Value</th>
                <th>Note</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(l, index) in tracker.log_objects"
                :key="l.log_datetime"
              >
                <td>{{ index }}</td>
                <td>{{ l.log_datetime | date_format }}</td>
                <td>{{ l.log_value }}</td>
                <td>{{ l.note }}</td>
                <td>
                  <button type="button" name="button">
                    <router-link
                      :to="{ name: 'log.update', params: { id: l.log_id } }"
                      >Edit</router-link
                    >
                  </button>
                  <button type="button" name="button">
                    <a @click.prevent="del(l.log_id)">Delete</a>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="text-center">
          <button class="button h5" type="button">
            <router-link
              :to="{ name: 'log.add.id', params: { id: tracker_id } }"
              >Add Log</router-link
            >
          </button>
        </div>
        <div class="h3 m-3">
          Scheduling an alert
        </div>
        <form id="s_option">
          <div
            class="btn-group-horizontal p-3"
            role="group"
            aria-label="Vertical radio toggle button group"
          >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="everyDay"
            />
            <label class="btn btn-outline-primary mx-1" for="everyDay"
              >Every day</label
            >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="everyWeek"
            />
            <label class="btn btn-outline-primary mx-1" for="everyWeek"
              >Every week</label
            >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="everyMonth"
            />
            <label class="btn btn-outline-primary mx-1" for="everyMonth"
              >Every month</label
            >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="everyYear"
            />
            <label class="btn btn-outline-primary mx-1" for="everyYear"
              >Every year</label
            >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="customFreq"
            />
            <label class="btn btn-outline-primary mx-1" for="customFreq"
              >Custom Frequency</label
            >
          </div>
        </form>
        <div class="table">
          <div class="">
            Reference date:
            <input
              type="datetime-local"
              step="1"
              v-model="schedule.ref_date"
              name="refdate"
              value="today"
            />
          </div>
          <div>Frequency of repeat:</div>
          <label
            class="mx-3"
            for="yearfreq"
            v-if="checkedValue == 'customFreq' || checkedValue == 'everyYear'"
            >year
            <input
              class="inp_freq"
              type="Number"
              step="1"
              v-model="schedule.year"
              name="yearfreq"
              min="0"
              value="0"
          /></label>
          <label
            class="mx-3"
            for="monthfreq"
            v-if="checkedValue == 'customFreq' || checkedValue == 'everyMonth'"
            >month
            <input
              class="inp_freq"
              type="Number"
              step="1"
              v-model="schedule.month"
              name="monthfreq"
              min="0"
              max="11"
              value="0"
          /></label>

          <label class="mx-3" for="weekfreq" v-if="checkedValue == 'everyWeek'"
            >day
            <input
              class="inp_freq"
              type="Number"
              step="1"
              v-model="schedule.week"
              name="weekfreq"
              min="0"
              max="7"
              value="0"
          /></label>

          <label
            class="mx-3"
            for="dayfreq"
            v-if="checkedValue == 'customFreq' || checkedValue == 'everyDay'"
            >day
            <input
              class="inp_freq"
              type="Number"
              step="1"
              v-model="schedule.day"
              name="dayfreq"
              min="0"
              max="31"
              value="0"
          /></label>
          <label
            class="mx-3"
            for="dayfreq"
            v-if="checkedValue == 'customFreq' || checkedValue == 'everyHour'"
            >hour
            <input
              class="inp_freq"
              type="Number"
              step="1"
              v-model="schedule.hour"
              name="hourfreq"
              min="0"
              max=""
              value="0"
          /></label>
          <label
            class="mx-3"
            for="minfreq"
            v-if="checkedValue == 'customFreq' || checkedValue == 'everyMin'"
            >min
            <input
              class="inp_freq"
              type="Number"
              step="1"
              v-model="schedule.min"
              name="minfreq"
              min="0"
              value="0"
          /></label>
          <br />
          <div class="my-2" align="center">
            <button type="button" @click="schedule_alert">
              Schedule alert
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import mychart from "../assets/mychart.js";
// import "chartjs-adapter-date-fns";
export default {
  data() {
    return {
      tracker_id: this.$route.params.id,
      tracker: "",
      s_option: "",
      schedule: {
        ref_date: null,
        year: 0,
        month: 0,
        week: 0,
        day: 0,
        hour: 0,
        min: 0
      }
    };
  },
  methods: {
    refresh() {
      // console.log(this);
      var self = this;
      fetch("http://localhost:5000/api/tracker/" + this.tracker_id, {
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
          // console.log(data)
          this.tracker = data;
        })
        .catch(rej => {
          // console.log(rej)
          console.log(rej.error + " kindly re-login");
          self.$router.push("/login"); //remember
        });
    },
    del(id) {
      if (window.confirm("Want to delete this log?")) {
        let self = this;
        fetch("http://localhost:5000/api/log/" + id, {
          method: "DELETE",
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
              this.refresh();
              // window.location.reload();
              return "";
            } else {
              throw {
                e_code: response.status,
                error: response.statusText
              };
            }
          })
          .catch(rej => {
            // console.log(rej)
            console.log(rej.error + " kindly re-login");
          });
      }
    },
    onChange(event) {
      this.s_option = event.target.id;
    },
    schedule_alert() {
      let data = {
        s_option: this.s_option,
        schedule: this.schedule
      };
      fetch("http://localhost:5000/schedule/" + this.tracker_id, {
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
        body: JSON.stringify(data)
      }).catch(rej => {
        console.log(rej);
        console.log(rej.error + " kindly re-login");
        return;
      });
    }
  },
  computed: {
    checkedValue() {
      return this.s_option;
    }
  },
  watch: {
    tracker: function(n) {
      if (n.log_objects.length > 0) {
        mychart.bind(this)();
      }
    }
  },
  mounted() {
    this.refresh();
  }
};
</script>

<style scoped>
.table {
  box-shadow: 0 6px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.1);
  background-color: #8bf7ed38;
  border-radius: 15px;
  border: hidden;
}
.table-responsive {
  max-height: 80vh;
  overflow-y: scroll;
}
button {
  box-shadow: 0 6px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 5px 0 rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

a {
  text-decoration: none;
}

.chart {
  position: relative;
  height: 70vh;
  overflow: hidden;
}
.inp_freq {
  width: 3rem;
}
</style>
