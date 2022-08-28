<template>
  <div class="trackdetail">
    <div class="row">
      <div class="col-8 offset-2">
        <div class="h4 justify-content-center">Log Entries</div>
        <canvas id="myChart" width="200" height="100"></canvas>
        <table class="table">
          <thead>
            <tr>
              <th>S.no</th>
              <th>Timestamp</th>
              <th>Value</th>
              <th>Note</th>
              <th>Actions</th>
            </tr>
            <tr v-for="(l, index) in logs" :key="l.log_datetime">
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
          </thead>
        </table>
        <div class="text-center">
          <button class="button h5" type="button">
            <router-link
              :to="{ name: 'log.add.id', params: { id: tracker_id } }"
              >Add Log</router-link
            >
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import "chartjs-adapter-date-fns";
export default {
  data() {
    return {
      tracker_id: this.$route.params.id,
      logs: []
    };
  },
  methods: {
    refresh() {
      let self = this;
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
          for (let i of data.log_objects) {
            self.logs.push(i);
          }
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
              window.location.reload();
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
    }
  },
  watch: {
    logs: function(n) {
      // console.log(o);
      if (n.length > 0) {
        const ctx = document.getElementById("myChart");
        let xlabel = [];
        let ylabel = [];
        for (let i of this.logs) {
          xlabel.push(i.log_datetime);
          ylabel.push(i.log_value);
        }
        xlabel.sort(function(a, b) {
          let dateA = new Date(a);
          let dateB = new Date(b);
          return dateA - dateB;
        });
        // console.log(xlabel);
        // console.log(ylabel);
        new Chart(ctx, {
          type: "line",
          data: {
            labels: xlabel,
            datasets: [
              {
                label: "# val",
                data: ylabel,
                backgroundColor: [
                  "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(255, 206, 86, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(255, 159, 64, 0.2)"
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(75, 192, 192, 1)",
                  "rgba(153, 102, 255, 1)",
                  "rgba(255, 159, 64, 1)"
                ],
                borderWidth: 1
              }
            ]
          },
          options: {
            scales: {
              x: {
                type: "time",
                time: {
                  unit: "minute"
                  // displayFormats: {
                  //       minute: 'HH:MM'
                  //   },
                },
                ticks: {
                  maxRotation: 0,
                  major: {
                    enabled: true
                  }
                }
              },
              y: {
                beginAtZero: true
              }
            }
          }
        });
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
</style>
