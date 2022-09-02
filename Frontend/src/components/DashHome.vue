<template>
  <div class="trackers align-items-center">
    <div class="card-deck row row-cols-lg-3 row-cols-2 justify-content-center">
      <div class="col m-3" v-for="(t, index) in trackers" :key="t.tracker_id">
        <div class="card border-success">
          <div class="card-header align-middle">
            <h4>{{ index + 1 }}) {{ t.tracker_name }}</h4>
            <span class="text-muted" v-if="t.last_updated"
              ><small
                >Last logged: {{ t.last_updated | date_format }}</small
              ></span
            >
          </div>
          <div class="card-body h5">
            <div class="card-title"></div>
            <div class="card-text">
              Tracker type: {{ t.tracker_type }}<br /><br />
              <span v-if="t.tracker_description"
                >Tracker description: {{ t.tracker_description }}<br
              /></span>
            </div>
          </div>
          <div class="card-footer collapse">
            <router-link
              :to="{ name: 'dash.tracker', params: { id: t.tracker_id } }"
              ><button type="button" class="btn btn-primary">
                Details
              </button></router-link
            >
            <router-link :to="'/tracker/update/' + t.tracker_id"
              >Edit</router-link
            >
            <a @click="del_trk(t.tracker_id)" class="btn btn-primary">Delete</a>
            <a @click="obj_to_csv(t)" class="btn">export</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import downloadBlob from "@/assets/utils.js";
export default {
  data() {
    return {
      trackers: this.$store.getters.get_trackers
    };
  },
  methods: {
    refresh() {
      let self = this;
      fetch("http://localhost:5000/api/user/" + this.$store.state.user, {
        method: "GET",
        headers: {
          "A-T":
            this.$Ciphers
              .decode("Vigenere Cipher", this.$cookies.get("user") || "", [
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
            // self.trackers.push(i)
            self.$store.commit("set_tracker", i);
          }
        })
        .catch(rej => {
          console.log(rej.error + " kindly re-login");
          self.$router.push("/login"); //remember
        });
    },
    del_trk(tid) {
      if (window.confirm("Delete this tracker along with all logs?")) {
        fetch("http://localhost:5000/api/tracker/" + tid, {
          method: "DELETE",
          headers: {
            "A-T":
              this.$Ciphers
                .decode("Vigenere Cipher", this.$cookies.get("user") || "", [
                  "Pwd"
                ])
                .split(";")[2] || ""
          }
        })
          .then(response => {
            // console.log(response)
            if (response.ok && !response.redirected) {
              alert("Deleted");
              this.$router.go();
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
            this.$router.push("/login"); //remember
          });
      }
    },
    obj_to_csv(objArray) {
      let array = [["Fields", "values\r\n"]];
      array =
        array +
        Object.entries(objArray) // escape double colons
          .map(v => [v[0] + "," + `"${v[1]}"`])
          .slice(0, 7) // quote it
          .join("\r\n"); // comma-separated

      console.log(array);
      downloadBlob(
        array,
        `"${objArray.tracker_name}.csv"`,
        "text/csv;charset=utf-8;"
      );
    }
  },
  mounted() {
    if (this.$store.getters.tracker_types.length == 0) {
      this.refresh();
    }
  }
};
</script>

<style scoped>
.table {
  border: hidden;
}

button {
  box-shadow: 0 6px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 5px 0 rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

a {
  text-decoration: none;
}

.card {
  box-shadow: 0 6px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.1);
  background-color: #00f3ff2e;
  border-radius: 15px;
  min-height: 15rem;
}

.card:hover {
  scale: 1.05;
  box-shadow: 0 0 0 2px #d0d0d0;
}

.card:hover .card-footer {
  display: inherit;
}
</style>
