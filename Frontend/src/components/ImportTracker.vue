<template>
  <div class="update_tracker">
    <div class="row">
      <div class="col-6 offset-3 d-flex justify-content-center">
        <h1>Import Trackers</h1>
      </div>
    </div>
    <br />
    <div class="row">
      <div class="col-8 offset-2 h5 ">
        <div class="row m-3">
          <div class="col-6 ">
            Upload csv file:
          </div>
          <div class="col-6">
            <input class="form-control" type="file" id="csv_file" />
          </div>
        </div>
        <div class="row">
          <div class="d-flex justify-content-center h4">
            Format:
          </div>
        </div>

        <div class="row m-3">
          <div class="col-8 offset-2">
            <img
              class="img img-fluid"
              src="../../public/img/tracker_fields.jpg"
              alt=""
            />
          </div>
        </div>
        <!-- ############# -->

        <!-- ####### -->

        <div class="row m-3 ">
          <div class="col d-flex justify-content-center">
            <button
              class="btn btn-outline-info"
              type="submit"
              id="check"
              @click="check"
            >
              Check
            </button>
            <button
              class="btn btn-outline-danger"
              type="submit"
              id="import"
              @click="imptracker"
              disabled
            >
              Import
            </button>
          </div>
        </div>
        <div class="content">
          {{ csv_data }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      csv_data: "",
      validate: false
    };
  },
  methods: {
    imptracker: async function() {
      let file_input = document.getElementById("csv_file");
      if (this.validate) {
        this.validate = false;
        let file = await file_input.files[0].text();

        console.log(file);
        let arr = file
          .split("\r\n")
          .map(a => a.replaceAll('"', "").split(","))
          .slice(1, -3);

        console.log(arr);
        this.addtracker(arr);
      }

      //-------------data----------------
    },
    addtracker(obj) {
      //----------validation----------
      console.log(obj);
      if (obj[0][1].length == 0) {
        this.csv_data = "Enter valid Tracker name";
        return;
      } else if (obj[2][1].length == 0) {
        this.csv_data = "Select correct tracker type";
        return;
      } else if (obj[2][1] == "Multiple-choice" && obj[3][1].length <= 1) {
        this.csv_data = "options should be more than 1";
        return;
      } else {
        this.csv_data = "";
      }
      //-------------data----------------
      let data = {
        user_id: parseInt(this.$store.state.user_id),
        tracker_name: obj[0][1],
        tracker_description: obj[1][1],
        tracker_type: obj[2][1],
        settings: obj[3][1]
      };
      console.log(data);
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
            alert("Added");
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
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login");
          return;
        });
    },
    check() {
      let file_input = document.getElementById("csv_file");
      // console.log(file_input);
      if (file_input.files.length > 0) {
        this.validate = true;
        document.getElementById("import").disabled = false;
      } else {
        console.log("else executed");
        this.csv_data = "Please select a correct csv file";
      }
    }
  }
};
</script>
