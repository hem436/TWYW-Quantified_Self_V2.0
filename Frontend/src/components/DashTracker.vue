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
            </thead>
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
      tracker: ""
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
    }
  },
  watch: {
    tracker: function(n) {
      if (n.log_objects.length > 0) {
        console.log(mychart);
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
  /* border: hidden; */
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
  height: 60vh;
  overflow: hidden;
}
</style>
