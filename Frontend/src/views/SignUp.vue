<template>
  <div class="login">
    <div class="row" align="center">
      <h1>New user sign up</h1>
      <br /><br />
    </div>
    <br />
    <div class="row">
      <div class="form col-8 offset-2 col-sm-6 offset-sm-3">
        <label for="username">Username:</label>
        <input
          class="form-control"
          type="text"
          name="username"
          v-model="username"
          required
        /><br />
        <h6
          v-if="!username_validate"
          style="font-family: zillaslab,palatino,Palatino Linotype,serif;color:red"
        >
          {{ error.u }}
        </h6>
        <br />
        <label for="email">Email:</label>
        <input
          class="form-control"
          type="text"
          name="email"
          v-model="email"
          required
        /><br />
        <h6
          v-if="!email_validate"
          style="font-family: zillaslab,palatino,Palatino Linotype,serif; color:red;"
        >
          {{ error.e }}
        </h6>
        <br />
        <label for="password">Enter a Password:</label>
        <input
          class="form-control"
          type="password"
          name="password"
          v-model="password"
          required
        /><br />
        <button type="button" @click="signup">Sign up</button>
        <br />
        <h6
          v-if="!password_validate"
          style="font-family: zillaslab,palatino,Palatino Linotype,serif;color:red"
        >
          {{ error.p }}
        </h6>
        Already have an account? <router-link to="/login">Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SignUp",
  data() {
    return {
      username: "",
      password: "",
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
    signup: function() {
      if (this.username_validate && this.password_validate) {
        let self = this;
        let data = {
          username: this.username,
          password: this.password,
          email: this.email
        };
        // console.log("going to signup");
        fetch(process.env.VUE_APP_BACKEND_URL + "api/user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "https://localhost:8080"
          },
          body: JSON.stringify(data)
        })
          .then(function(response) {
            if (response.ok) {
              //
              // console.log(response)
              return response.json();
            } else {
              throw "bad response";
            }
          })
          .then(function(data) {
            // console.log(data);
            self.$cookies.set(
              "user",
              self.$Ciphers.encode(
                "Vigenere Cipher",
                data.username + ";" + data.auth_token,
                ["Pwd"]
              )
            );
            self.$store.commit("login", data);
            self.$router.push("/login");
          })
          .catch(error => console.log(error));
        // console.log(response);
      } else {
        alert("Invalid username or password");
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
      if (this.password.match(regEx)) {
        this.gen_perror("");
        return true;
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
  }
};
</script>

<style scoped></style>
