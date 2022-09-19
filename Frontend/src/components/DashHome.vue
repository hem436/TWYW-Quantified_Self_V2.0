<template>
  <div class="trackers align-items-center">
    <div class=" row row-cols-lg-3 row-cols-2 justify-content-center">
      <div
        class="container col m-2"
        v-for="(t, index) in trackers"
        :key="t.tracker_id"
      >
        <div class="action row g-0">
          <div class=" col d-flex align-items-center">
            <div class="group pt-5">
              <router-link
                :to="{ name: 'dash.tracker', params: { id: t.tracker_id } }"
              >
                <img
                  src="@/assets/svg/details.svg"
                  alt="Details"
                  data-bs-toggle="tooltip"
                  title="Details"
                />
              </router-link>
              <router-link :to="'/tracker/update/' + t.tracker_id">
                <img
                  src="@/assets/svg/edit.svg"
                  alt="Edit"
                  data-bs-toggle="tooltip"
                  title="Edit"
                />
              </router-link>

              <a @click="del_trk(t.tracker_id)">
                <img
                  src="../assets/svg/delete.svg"
                  alt="delete"
                  data-bs-toggle="tooltip"
                  title="Delete"
              /></a>

              <a @click="obj_to_csv(t)">
                <img
                  src="../assets/svg/export.svg"
                  alt="export"
                  data-bs-toggle="tooltip"
                  title="Export"
              /></a>
            </div>
          </div>
          <div class="col-md-10">
            <div class="card border-success">
              <div class="card-header align-middle">
                <h4>{{ index + 1 }}) {{ t.tracker_name }}</h4>
                <span class="text-muted" v-if="t.last_updated">
                  <small
                    >Last logged:
                    {{ t.last_updated.slice(0, -7) | date_format }}</small
                  >
                </span>
              </div>
              <div class="card-body h6">
                <div class="card-text">
                  <div class="row">
                    <div class="col text-primary">
                      Tracker type:
                    </div>
                    <div class="col">{{ t.tracker_type }}<br /><br /></div>
                  </div>
                  <div class="text-primary" v-if="t.tracker_description">
                    Tracker description:
                  </div>
                  <span>{{ t.tracker_description }}</span>
                </div>
              </div>
              <div class="card-footer collapse"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import downloadBlob from "@/scripts/utils.js";
export default {
  data() {
    return {
      trackers: this.$store.getters.get_trackers
    };
  },
  methods: {
    refresh() {
      let self = this;
      fetch(
        process.env.VUE_APP_BACKEND_URL + "api/user/" + this.$store.state.user,
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
        fetch(process.env.VUE_APP_BACKEND_URL + "api/tracker/" + tid, {
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
              this.$store.commit("delete_trackers");
              this.trackers = this.$store.state.trackers;
              this.refresh();
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
            this.$router.go("/login"); //remember
          });
      }
    },
    obj_to_csv(objArray) {
      let array = [["Fields", "values\r\n"]];
      array =
        array +
        Object.entries(objArray) // escape double colons
          .map(v => [v[0] + "," + `"${v[1]}"`])
          .slice(2, 7) // quote it
          .join("\r\n") +
        "\r\n" +
        Object.entries(objArray) // escape double colons
          .map(v => [v[0] + "," + `"${v[1]}"`])
          .slice(0, 2) // quote it
          .join("\r\n");
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
  background-color: #00f3ff2e;
  border-radius: 15px;
  min-height: 20rem;
  font-family: Rockwell, sans-serif;
}
.group {
  visibility: hidden;
  display: block;
  align-self: baseline;
  vertical-align: bottom;
}
.card:hover {
  box-shadow: 0 0 0 2px #d0d0d0;
}

.action:hover .group {
  visibility: visible;
}
img {
  margin: 5px;
  width: 40px;
  border-radius: 40px;
}
img:hover {
  box-shadow: 0 0 0 2px #d0d0d0;
}
@media (max-width: 700px) {
  .container {
    min-width: 80%;
  }
}
</style>
