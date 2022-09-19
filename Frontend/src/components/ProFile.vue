<template>
  <div class="userprofile">
    <div class="row" align="center">
      <h3>Profile</h3>
      <br />
    </div>
    <br />
    <div class="row">
      <div class="form col-sm-6 offset-sm-3">
        <label for="username">Username:</label><br />
        <input
          type="text"
          class="form-control"
          name="username"
          id="username"
          v-model="username"
          disabled
          required
        /><button
          class="btn btn-outline-secondary"
          type="button"
          @click="edit_username"
        >
          edit</button
        ><br />
        <h6
          v-if="!username_validate"
          style="font-family: zillaslab,palatino,Palatino Linotype,serif; color:red;"
        >
          {{ error.u }}
        </h6>
        <br />
        <label for="email">Email:</label><br />
        <input
          type="email"
          class="form-control"
          id="email"
          name="email"
          v-model="email"
          required
          disabled
        />
        <button
          class="btn btn-outline-secondary"
          type="button"
          @click="edit_email"
        >
          edit
        </button>

        <h6
          v-if="!email_validate"
          style="font-family: zillaslab,palatino,Palatino Linotype,serif; color:red;"
        >
          {{ error.e }}
        </h6>
        <br />
        <div class="row">
          <div class=" col-6">
            <label for="password">Enter password:</label>
            <input
              type="password"
              class="form-control"
              id="password"
              v-model="old_password"
              required
            />
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="show_pwd"
            >
              view
            </button>
          </div>
          <div class="col-6" v-if="changepwd">
            <label for="new_password">New password:</label><br />
            <input
              type="text"
              class="form-control"
              name="new_password"
              v-model="new_password"
              required
            /><br />
          </div>
        </div>
        <h6
          v-if="!password_validate"
          style="font-family: zillaslab,palatino,Palatino Linotype,serif; color:red;"
        >
          {{ error.p }}
        </h6>
      </div>
    </div>
    <div class="d-flex col justify-content-center">
      <button
        class="m-2 btn btn-outline-info"
        type="button"
        @click="changepwd ? (changepwd = false) : (changepwd = true)"
      >
        Change password
      </button>
      <button class="m-2 btn btn-outline-primary" type="button" @click="update">
        Update submit
      </button>
      <button class="h6 m-2 btn btn-outline-danger" type="button" @click="del">
        Delete Account
      </button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      changepwd: false,
      old_password: "",
      new_password: "",
      email: "",
      error: {
        u: "",
        p: "",
        e: ""
      }
    };
  },
  methods: {
    gen_uerror: function(e) {
      this.error.u = e;
    },
    gen_perror: function(e) {
      this.error.p = e;
    },
    gen_eerror: function(e) {
      this.error.e = e;
    },
    edit_email() {
      if (document.getElementById("email").disabled) {
        document.getElementById("email").disabled = false;
      } else {
        document.getElementById("email").disabled = true;
      }
    },
    edit_username() {
      if (document.getElementById("username").disabled) {
        document.getElementById("username").disabled = false;
      } else {
        document.getElementById("username").disabled = true;
      }
    },
    show_pwd() {
      if (document.getElementById("password").type == "password") {
        document.getElementById("password").type = "text";
      } else {
        document.getElementById("password").type = "password";
      }
    },
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
          self.username = data.username;
          self.email = data.email;
        })
        .catch(rej => {
          console.log(rej.error + " kindly re-login");
          self.$router.push("/login"); //remember
        });
    },
    update: function() {
      let self = this;
      if (this.username_validate) {
        let data = {
          modified_username: this.username,
          old_password: this.old_password,
          new_password: this.new_password,
          modified_email: this.email
        };
        fetch(
          process.env.VUE_APP_BACKEND_URL +
            "api/user/" +
            this.$store.state.user,
          {
            method: "PUT",
            credentials: "include",
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
          .then(function(response) {
            if (response.ok) {
              return response.json();
            } else {
              throw "no response";
            }
          })
          .then(function(data) {
            console.log(data);
            self.$cookies.set(
              "user",
              self.$Ciphers.encode(
                "Vigenere Cipher",
                data.user_id +
                  ";" +
                  data.username +
                  ";" +
                  self.$store.state.token,
                ["Pwd"]
              )
            );
            self.$store.commit("login", data);
            alert("Updated successfully");
            self.$router.push("/dashboard");
          })
          .catch(error => console.log(error));
      } else {
        alert("Invalid username or password");
      }
    },
    del: function() {
      let self = this;
      if (
        window.confirm("Are you sure want to delete this account completely?")
      ) {
        let data = {
          password: this.old_password
        };
        fetch(
          process.env.VUE_APP_BACKEND_URL +
            "api/user/" +
            this.$store.state.user,
          {
            method: "DELETE",
            credentials: "include",
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
          .then(function(response) {
            if (response.ok) {
              return response.json();
            } else {
              throw response;
            }
          })
          .then(() => {
            console.log(self);
            self.$cookies.remove("user");
            alert("Deleted");
            self.$router.push("/dashboard");
          })
          .catch(error => {
            console.log(error);
            alert(error.statusText);
          });
      }
    }
  },
  computed: {
    username_validate: function() {
      let regEx = /^[0-9a-zA-Z]*$/;
      if (this.username.match(regEx) && this.username.length > 0) {
        this.gen_uerror("");
        return true;
      } else {
        this.gen_uerror("Username must be alphanumeric");
        return false;
      }
    },
    password_validate: function() {
      let regEx = /^(?=.*).{8,}$/;
      if (this.old_password.match(regEx)) {
        if (this.changepwd && !this.new_password.match(regEx)) {
          this.gen_perror("New password should be atleast 8 characters");
          return false;
        } else {
          this.gen_perror("");
          return true;
        }
      } else {
        this.gen_perror("Password should be atleast 8 characters");
        return false;
      }
    },
    email_validate: function() {
      let regEx = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
      if (this.email.match(regEx)) {
        return true;
      } else {
        this.gen_eerror("Invalid email");
        return false;
      }
    }
  },
  mounted() {
    this.refresh();
  }
};
</script>
