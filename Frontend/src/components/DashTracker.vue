<template>
  <div class="trackdetail">
    <div class="row">
      <div
        class="col-sm-10 offset-sm-1 col-lg-8 offset-lg-2 justify-content-center"
      >
        <h4>Trend</h4>
        <div class="container border mb-5">
          <div class="chart" id="myChart"></div>
        </div>

        <div class="h4 d-flex justify-content-between">
          Log Entries
          <a
            class="export-p d-flex p-0 "
            type="button"
            @click="obj_to_csv(tracker.log_objects)"
          >
            <h6 class="export text-muted pt-1">Export logs</h6>
            <img
              src="@/assets/svg/export.svg"
              data-bs-toggle="tooltip"
              title="Export log"
              style="width:30px;margin-top:0px"
            />
          </a>
        </div>
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
                  <div class="action d-flex">
                    <router-link
                      :to="{ name: 'log.update', params: { id: l.log_id } }"
                    >
                      <img
                        src="@/assets/svg/edit.svg"
                        data-bs-toggle="tooltip"
                        title="Edit log"
                      />
                    </router-link>
                    <a @click.prevent="del(l.log_id)">
                      <img
                        src="@/assets/svg/delete.svg"
                        data-bs-toggle="tooltip"
                        title="Delete log"
                    /></a>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="col" align="right">
        <router-link :to="{ name: 'log.add.id', params: { id: tracker_id } }">
          <img
            src="@/assets/svg/add.svg"
            width="40"
            alt="add log"
            data-bs-toggle="tooltip"
            title="Add log"
        /></router-link>
        <a
          class="m-2"
          type="button"
          data-bs-toggle="offcanvas"
          data-bs-target="#alert"
          aria-controls="alert"
        >
          <img
            src="@/assets/svg/alert.svg"
            width="40"
            alt="alert"
            data-bs-toggle="tooltip"
            title="Schedule alert"
          />
        </a>
      </div>
    </div>
    <div
      class="offcanvas offcanvas-end"
      tabindex="-1"
      id="alert"
      aria-labelledby="alertLabel"
    >
      <div class="offcanvas-header">
        <div class="h3 m-4 ps-4" id="alertLabel">
          Scheduling an alert
        </div>
        <button
          type="button"
          class="btn-close text-reset"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body">
        <form id="s_option">
          <div class="h5">
            Schedule name:
            {{ this.current_s.name
            }}<button
              class="h6 m-2 btn btn-outline-danger"
              type="button"
              @click="test_alert"
            >
              test now
            </button>
          </div>
          <div class="form-check form-switch">
            <label class="form-check-label" for="switch">On/Off</label>
            <input
              class="form-check-input"
              type="checkbox"
              role="switch"
              name="switch"
              v-model="sw"
            />
          </div>

          <div class="btn-group my-4">
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="Every hour"
            />
            <label class="btn btn-outline-info " for="Every hour"
              >Every hour</label
            >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="Every day"
            />
            <label class="btn btn-outline-info" for="Every day"
              >Every day</label
            >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="Every week"
            />
            <label class="btn btn-outline-info " for="Every week"
              >Every week</label
            >
            <input
              type="radio"
              class="btn-check"
              name="vbtn-radio"
              @change="onChange($event)"
              id="Every month"
            />
            <label class="btn btn-outline-info " for="Every month"
              >Every month</label
            >
          </div>
          <div class="">
            <em class="h6">Next Schedule ({{ this.current_s.next }})</em>
          </div>
          <div class="my-3" align="center">
            <button
              class="btn btn-outline-primary"
              type="button"
              name="button"
              @click="schedule_alert"
            >
              <img
                src="@/assets/svg/timer.svg"
                data-bs-toggle="tooltip"
                title="Schedule alert"
              />Schedule an alert
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import mychart from "../assets/mychart.js";
import downloadBlob from "@/assets/utils.js";
export default {
  data() {
    return {
      tracker_id: this.$route.params.id,
      tracker: "",
      sw: "",
      s_option: "",
      current_s: {
        name: "No schedule",
        next: ""
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
      fetch(
        "http://localhost:5000/alert/" + this.tracker_id + "?switch=" + this.sw,
        {
          method: "GET",
          headers: {
            "A-T":
              this.$Ciphers
                .decode("Vigenere Cipher", this.$cookies.get("user") || "", [
                  "Pwd"
                ])
                .split(";")[2] || ""
          }
        }
      )
        .then(response => {
          if (response && response.ok) {
            return response.json();
          } else {
            throw response;
          }
        })
        .then(data => {
          this.current_s = data;
          this.s_option = data.schedule;
          this.sw = data.enabled;
          document.getElementById(this.s_option).checked = true;
        })
        .catch(rej => {
          console.log(rej.statusText);
          console.log(rej.status + " kindly re-login");
          return;
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
      this.sw = true;
    },
    schedule_alert() {
      let data = {
        schedule: this.s_option
      };
      fetch(
        "http://localhost:5000/alert/" + this.tracker_id + "?switch=" + this.sw,
        {
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
        }
      )
        .then(response => {
          if (response && response.ok) {
            return response.json();
          } else {
            throw response;
          }
        })
        .then(data => {
          this.current_s = data;
          this.sw = data.enabled;
          document.getElementById(this.s_option).checked = true;
          alert("scheduled");
        })
        .catch(rej => {
          if (rej.status == 400) {
            alert("select a schedule first");
          }
          return;
        });
    },
    test_alert() {
      let data = {
        schedule: "now"
      };
      fetch("http://localhost:5000/alert/" + this.tracker_id, {
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
      })
        .then(response => {
          if (response && response.ok) {
            return response.text();
          }
        })
        .then(data => {
          alert(data);
        })
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login");
          return;
        });
    },
    obj_to_csv: async function(objArray) {
      let array = [
        [
          "S.No",
          "Log timestamp(iso)",
          "Log note",
          "Log value",
          "Tracker id",
          "Log id"
        ]
      ];
      objArray.forEach((item, i) => {
        array =
          array +
          "\r\n" +
          (i + 1) +
          "," +
          Object.entries(item)
            .map(v => [`"${v[1]}"`])
            .slice(2, 5)
            .join(",") +
          "," +
          Object.entries(item)
            .map(v => [`"${v[1]}"`])
            .slice(0, 2);
      });

      downloadBlob(
        array,
        `"${this.tracker.tracker_name}_logs.csv"`,
        "text/csv;charset=utf-8;"
      );
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

button {
  box-shadow: 0 6px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 5px 0 rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

a {
  text-decoration: none;
}
img {
  margin: 5px;
  width: 40px;
  border-radius: 40px;
}
img:hover {
  box-shadow: 0 0 0 2px #d0d0d0;
}
/* .export {
  visibility: hidden;
}
.export-p:hover .export {
  visibility: visible;
} */
.chart {
  position: relative;
  height: 70vh;
  overflow: hidden;
}
</style>
