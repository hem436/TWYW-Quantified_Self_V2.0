<template>
  <div class="update_tracker">
    <div class="row">
      <div class="col-6 offset-3 d-flex justify-content-center">
        <h1>Update a Tracker</h1>
      </div>
      <div class="col-3 d-flex justify-content-center"></div>
    </div>
    <br />
    <div class="row">
      <div class="col-6 offset-3 h5 ">
        <div class="row m-3">
          <div class="col-6 ">
            Tracker Name:
          </div>
          <div class="col-6">
            <input type="text" v-model="t_name" value="" />
          </div>
        </div>
        <div class="row m-3">
          <div class="col-6">
            Tracker type:
          </div>
          <div class="col-6">
            {{ type }}
          </div>
        </div>
        <!-- ############# -->
        <div class="row m-3" v-if="type == 'Multiple-choice'">
          <div class="col-6">
            <label for="t_option">Options</label>
          </div>
          <div class="col-6">
            <input type="text" id="option" value="" />
            <button type="button" name="button" @click="addopt">
              update options
            </button>
            <button type="button" name="button" @click="remopt">
              remove
            </button>

            <div>{{ t_option.join() }}</div>
          </div>
        </div>
        <!-- ####### -->
        <div class="row m-3">
          <div class="col-6">
            Tracker Description:
          </div>
          <div class="col-6">
            <textarea
              v-model="t_desc"
              name="desc"
              placeholder="Note/Remark"
            ></textarea>
          </div>
        </div>
        <div class="row m-3 ">
          <div class="col d-flex justify-content-center">
            <button
              class="btn btn-outline-info"
              type="submit"
              name="button"
              @click="updatetracker"
            >
              Submit
            </button>
            <div class="error">{{ error }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      t_id: this.$route.params.id,
      t_name: "",
      t_desc: "",
      t_option: [],
      type: "",
      error: ""
    };
  },
  methods: {
    addopt() {
      let opt = document.getElementById("option").value;
      if (opt) {
        this.t_option.push(opt);
        document.getElementById("option").value = "";
      }
    },
    remopt() {
      if (this.t_option.length > 0) {
        document.getElementById("option").value = this.t_option.pop();
      }
    },
    updatetracker() {
      //----------validation----------
      if (this.t_name.length == 0) {
        this.error = "Enter valid Tracker name";
        return;
      } else if (this.type.length == 0) {
        this.error = "Select correct tracker type";
        return;
      } else {
        this.error = "";
      }
      //-------------data----------------
      let data = {
        user_id: this.$store.state.user_id,
        modified_tracker_name: this.t_name,
        modified_tracker_description: this.t_desc,
        tracker_type: this.type,
        modified_tracker_settings: this.t_option.join()
      };
      fetch(process.env.VUE_APP_BACKEND_URL + "api/tracker/" + this.t_id, {
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
          console.log(rej.error + " kindly re-login");
          return;
        });
    }
  },
  mounted() {
    if (this.t_id) {
      fetch(process.env.VUE_APP_BACKEND_URL + "api/tracker/" + this.t_id, {
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
          // console.log(response);
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
          this.t_name = data.tracker_name;
          this.t_desc = data.tracker_description;
          this.type = data.tracker_type;
          this.t_option = data.settings.split(",");
        })
        .catch(rej => {
          // console.log(rej)
          console.log(rej.error + " kindly re-login");
          this.$router.push("/login"); //remember
        });
    }
  }
};
</script>
