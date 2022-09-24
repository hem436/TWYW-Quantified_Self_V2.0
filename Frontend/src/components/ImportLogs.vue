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
            <input class="form-control" type="file" id="csv_file" />
          </div>
        </div>
        <div class="row">
          <div class="d-flex justify-content-center h4">
            Format:
          </div>
        </div>

        <div class="row m-3">
          <div class="col-sm-8 offset-sm-2">
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
              @click="implog"
              disabled
            >
              Import
            </button>
          </div>
        </div>
        <div
          class="h6"
          align="center"
          style="font-family: zillaslab,palatino,Palatino Linotype,serif; color:red;"
        >
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
        let arr = file
          .split("\n")
          .map(a =>
            a
              .replaceAll('"', "")
              .replace("\r", "")
              .split(",")
          )
          .slice(1);
        console.log(arr);
        arr.forEach(item => {
          if (item.length > 0) {
            this.addlog(item);
          }
        });
      }

      //-------------data----------------
    },
    addlog: async function(obj) {
      if (obj.length < 5) {
        this.csv_data = "Incorrect fields";
        console.log("Incorrect fields :" + obj);
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
            this.csv_data = "Logging...";
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
          alert("Error:" + rej);
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
