<template>
  <div class="add_tracker">
    <div class="row">
      <div class="col-6 offset-3 d-flex justify-content-center">
        <h1>Add a Tracker</h1>
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
            <select id="t_type" v-model="type">
              <option value="Integer">Integer</option>
              <option value="Numeric">Numeric</option>
              <option value="Time">Time</option>
              <option value="Multiple-choice">Multiple-choice</option>
            </select>
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
              add options
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
              @click="addtracker"
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
    addtracker() {
      //----------validation----------
      if (this.t_name.length == 0) {
        this.error = "Enter valid Tracker name";
        return;
      } else if (this.type.length == 0) {
        this.error = "Select correct tracker type";
        return;
      } else if (this.type == "Multiple-choice" && this.t_option.length <= 1) {
        this.error = "options should be more than 1";
        return;
      } else {
        this.error = "";
      }
      //-------------data----------------
      let data = {
        user_id: this.$store.state.user_id,
        tracker_name: this.t_name,
        tracker_description: this.t_desc,
        tracker_type: this.type,
        settings: this.t_option.join()
      };
      fetch(process.env.VUE_APP_BACKEND_URL + "api/tracker", {
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
          if (response.ok && !response.redirected) {
            return response.json();
          } else {
            if (response.code == "401") {
              this.$router.push("/login");
            }
            throw {
              e_code: response.status,
              error: response.statusText
            };
          }
        })
        .then(data => {
          this.$store.commit("set_tracker", data);
          alert("Added");
        })
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login");
          return;
        });
    }
  },
  computed: {}
};
</script>
