<template>
<div class="loginform">
	<div class="row" align="center">
		<h1>Welcome to TWYW</h1><br><br>
	</div><br>
	<div class="row">
		<div class="form col-sm-6 offset-sm-3">
			<h3>User Login</h3>
			<label for="username">Username:</label><br>
			<input type="text" class="form-control" name="username" v-model='username' required><br>
			<h6 v-if="!username_validate" style="font-family: zillaslab,palatino,Palatino Linotype,serif; color:red;">{{error.u}}</h6> <br>
			<label for="password">Enter your password:</label><br>
			<input type="password" class="form-control" name="password" v-model='password' required><br>
			<button type="button" @click="login">Login</button><br>
			<h6 v-if="!password_validate" style="font-family: zillaslab,palatino,Palatino Linotype,serif; color:red;">{{error.p}}</h6> Not a member? <a href="/signup">Sign Up</a>
		</div>
	</div>
</div>
</template>

<script>
export default {
	name: 'LogIn',
	data() {
		return {
			username: "",
			password: "",
			error: {
				u: "",
				p: ""
			}
		}
	},
	methods: {
		gen_uerror: function(e) {
			this.error.u = e;
		},
		gen_perror: function(e) {
			this.error.p = e;
		},
		login: function() {
			let self = this;
			if(this.username_validate && this.password_validate) {
				let data = {
					'username': this.username,
					'password': this.password
				};
				console.log("going to login");
				fetch("http://127.0.0.1:5000/api/login", {
					method: "POST",
					credentials: 'include',
					headers: {
						"Content-Type": "application/json",
						"Access-Control-Allow-Credentials": true,
						"Access-Control-Allow-Origin": "http://localhost:8080",
					},
					body: JSON.stringify(data)
				}).then(function(response) {
					if(response.ok) {
						return response.json();
					} else {
						throw "no response"
					}
				}).then(function(data) {
					// self.$cookies.set("data", data.auth_token)
					// console.log(data.auth_token)
					self.$cookies.set("user", self.$Ciphers.encode("Vigenere Cipher", data.user_id + ";" + data.username + ";" + data.auth_token, ["Pwd"]));
					self.$store.commit('login', data);
					self.$router.push('/dashboard');
				}).catch(error => console.log(error))
			} else {
				alert("Invalid username or password");
			}
		}
	},
	computed: {
		username_validate: function() {
			let regEx = /^[0-9a-zA-Z]*$/;
			if(this.username.match(regEx) && (this.username.length > 0)) {
				this.gen_uerror("")
				return true;
			} else {
				this.gen_uerror("Username must be alphanumeric")
				return false;
			}
		},
		password_validate: function() {
			let regEx = /^(?=.*).{8,}$/;
			if(this.password.match(regEx)) {
				this.gen_perror("");
				return true;
			} else {
				this.gen_perror('Password should be atleast 8 characters');
				return false;
			}
		}
	}
}
</script>

<style>

</style>
