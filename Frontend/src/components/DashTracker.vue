<template>
  <div class="trackdetail">
    <div class="row">
      <div class="col-8 offset-2 justify-content-center">
        <canvas id="myChart" width="900" height="500"></canvas>

        <div class="h4 justify-content-center">Log Entries</div>
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
// import Chart from "chart.js/auto";
// import "chartjs-adapter-date-fns";
export default {
  data() {
    return {
      tracker_id: this.$route.params.id,
      tracker: "",
      logs: []
    };
  },
  methods: {
    refresh() {
      console.log(this);
      let self = this;
      if (this.logs.length != 0) {
        this.logs = [];
      }
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
    }
  },
  watch: {
    logs: function(n) {
      console.log(this);
      if (n.length > 0) {
        var xlabel = [];
        var ylabel = [];
        for (let i of this.logs) {
          xlabel.push(i.log_datetime);
          ylabel.push(i.log_value);
        }
        var echarts = this.$echarts;
        var chartDom = document.getElementById("myChart");
        var myChart = echarts.init(chartDom);
        var option;
        option = {
          title: {
            text: "Log Values",
            left: "center"
          },
          grid: {
            bottom: 100
          },
          toolbox: {
            feature: {
              dataZoom: {
                yAxisIndex: "none"
              },
              restore: {},
              saveAsImage: {}
            }
          },
          tooltip: {
            trigger: "axis",
            axisPointer: {
              type: "cross",
              animation: false,
              label: {
                backgroundColor: "#505765"
              }
            }
          },
          legend: {
            data: ["Flow"],
            left: 10
          },
          dataZoom: [
            {
              show: true,
              realtime: true,
              start: 0,
              end: 100
            },
            {
              type: "inside",
              realtime: true,
              start: 0,
              end: 100
            }
          ],
          xAxis: [
            {
              type: "category",
              boundaryGap: false,
              axisLine: { onZero: false },
              // prettier-ignore
              data: xlabel.map(function (str) {
                    return str.replace(' ', '\n').slice(0,-7);
                })
            }
          ],
          yAxis: [
            {
              name: "Flow(m^3/s)",
              type: "value"
            }
          ],
          series: [
            {
              name: "Flow",
              type: "line",
              // areaStyle: {},
              lineStyle: {
                width: 1
              },
              // emphasis: {
              //   focus: "series"
              // },
              // markArea: {
              //   silent: true,
              //   itemStyle: {
              //     opacity: 0.3
              //   },
              //   data: [
              //     [
              //       {
              //         xAxis: "2009/9/12\n7:00"
              //       },
              //       {
              //         xAxis: "2009/9/22\n7:00"
              //       }
              //     ]
              //   ]
              // },
              // prettier-ignore
              data:ylabel
            }
          ]
        };

        option && myChart.setOption(option);
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
