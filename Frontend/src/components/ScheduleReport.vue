<template>
  <div class="row">
    <form class="form col-10 offset-1">
      <div class="h5">
        Schedule name:
        {{ this.current_s.name }}<br />
      </div>
      <div class="form-check form-switch">
        <label class="form-check-label" for="switch">On/Off</label>
        <input
          class="form-check-input"
          type="checkbox"
          role="switch"
          name="switch"
          v-model="sw"
        />
      </div>

      <div class="btn-group my-4">
        <input
          type="radio"
          class="btn-check"
          name="vbtn-radio"
          @change="onChange($event)"
          id="Every day"
        />
        <label class="btn btn-outline-info" for="Every day">Every day</label>
        <input
          type="radio"
          class="btn-check"
          name="vbtn-radio"
          @change="onChange($event)"
          id="Every week"
        />
        <label class="btn btn-outline-info " for="Every week">Every week</label>
        <input
          type="radio"
          class="btn-check"
          name="vbtn-radio"
          @change="onChange($event)"
          id="Every month"
        />
        <label class="btn btn-outline-info " for="Every month"
          >Every month</label
        >
        <input
          type="radio"
          class="btn-check"
          name="vbtn-radio"
          @change="onChange($event)"
          id="Every year"
        />
        <label class="btn btn-outline-info " for="Every year">Every year</label>
      </div>
      <div class="">
        <em class="h6"
          >Next Schedule ({{ this.current_s.next.slice(0, -4) }})</em
        >
      </div>

      <div class="my-3">
        <button
          class="btn btn-outline-primary"
          type="button"
          name="button"
          @click="schedule_report"
        >
          Schedule report
        </button>
        <button
          class="h6 m-2 btn btn-outline-danger"
          type="button"
          @click="test_report"
        >
          Send now
        </button>
      </div>
    </form>
  </div>
</template>

<script type="text/javascript">
export default {
  data() {
    return {
      user_id: this.$store.state.user_id,
      sw: "",
      s_option: "",
      current_s: {
        name: "No schedule",
        next: ""
      }
    };
  },
  methods: {
    onChange(event) {
      this.s_option = event.target.id;
      this.sw = true;
    },
    schedule_report() {
      let data = {
        schedule: this.s_option
      };
      fetch(
        process.env.VUE_APP_BACKEND_URL +
          "gen_report/" +
          this.user_id +
          "?switch=" +
          this.sw,
        {
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
        }
      )
        .then(response => {
          if (response && response.ok) {
            return response.json();
          } else {
            throw response;
          }
        })
        .then(data => {
          this.current_s = data;
          this.sw = data.enabled;
          document.getElementById(this.s_option).checked = true;
          alert("scheduled");
        })
        .catch(rej => {
          if (rej.status == 400) {
            alert("select a schedule first");
          }
          return;
        });
    },
    test_report() {
      let data = {
        schedule: "now"
      };
      fetch(process.env.VUE_APP_BACKEND_URL + "gen_report/" + this.user_id, {
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
          if (response && response.ok) {
            return response.text();
          }
        })
        .then(data => {
          alert(data);
        })
        .catch(rej => {
          console.log(rej);
          console.log(rej.error + " kindly re-login");
          return;
        });
    }
  },
  mounted() {
    fetch(
      process.env.VUE_APP_BACKEND_URL +
        "gen_report/" +
        this.user_id +
        "?switch=" +
        this.sw,
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
        if (response && response.ok) {
          return response.json();
        } else {
          throw response;
        }
      })
      .then(data => {
        this.current_s = data;
        this.s_option = data.schedule;
        this.sw = data.enabled;
        document.getElementById(this.s_option).checked = true;
      })
      .catch(rej => {
        console.log(rej.statusText);
        console.log(rej.status + " kindly re-login");
        return;
      });
  }
};
</script>

<style></style>
