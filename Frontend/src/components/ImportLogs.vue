<template>
  <div class="update_log">
    <div class="row">
      <div class="col-6 offset-3 d-flex justify-content-center">
        <h1>Import Logs</h1>
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
            <input type="file" id="csv_file" />
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
              src="../../public/img/log_fields.png"
              alt=""
              style="scale:1.5"
            />
          </div>
        </div>
        <br />
        <!-- ############# -->

        <!-- ####### -->

        <div class="row m-3 ">
          <div class="col d-flex justify-content-center">
            <button type="submit" id="check" @click="check">
              Check
            </button>
            <button type="submit" id="import" @click="implog" disabled>
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
    implog: async function() {
      let file_input = document.getElementById("csv_file");
      if (this.validate) {
        this.validate = false;
        let file = await file_input.files[0].text();

        console.log(file);
        let arr = file
          .split("\n")
          .map(a =>
            a
              .replaceAll('"', "")
              .replace("\r", "")
              .split(",")
          )
          .slice(1);
        console.log(file.split("\n"));
        arr.forEach(item => {
          console.log("item");
          console.log(item);
          this.addlog(item);
        });
      }

      //-------------data----------------
    },
    addlog: async function(obj) {
      if (obj.len == 0) {
        console.log("no fields available");
        return;
      }
      let tid = obj[4];
      let ldatetime = obj[1];
      let lnote = obj[2];
      let lval = obj[3];
      //----------validation----------
      if (tid == "") {
        this.csv_data = "Enter valid tracker id";
        return;
      } else if (lval.length == 0) {
        this.csv_data = "Enter a log value";
        return;
      } else {
        this.csv_data = "";
      }
      //#------validation--------
      let currentdate = new Date();
      let mstr = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
      ];
      let datetime =
        currentdate.getDate() +
        "/" +
        mstr[currentdate.getMonth()] +
        "/" +
        currentdate.getFullYear() +
        ", " +
        currentdate.getHours() +
        ":" +
        currentdate.getMinutes() +
        ":" +
        currentdate.getSeconds() +
        "." +
        currentdate.getMilliseconds();
      if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*$/.test(ldatetime)) {
        datetime = this.$options.filters.date_format(ldatetime);
      }
      let data = {
        tracker_id: tid,
        log_value: lval,
        log_note: lnote,
        log_datetime: datetime
      };
      console.log(data);
      fetch(process.env.VUE_APP_BACKEND_URL + "api/log", {
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
            this.csv_data = "Logged";
            console.log("Logged");
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
          this.$router.go("/");
        });
    },
    check() {
      let file_input = document.getElementById("csv_file");
      if (
        file_input.files.length > 0 &&
        file_input.files[0].type == "text/csv"
      ) {
        this.validate = true;
        this.csv_data = "";
        document.getElementById("import").disabled = false;
      } else {
        console.log("else executed");
        this.csv_data = "Please select a correct csv file";
      }
    }
  }
};
</script>
