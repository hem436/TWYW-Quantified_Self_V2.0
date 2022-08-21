<template>

</template>

<script>
export default {
	data() {
		return {
			logs: []
		}
	},
	beforeCreate() {
		let self = this
		fetch("http://localhost:5000/api/tracker/" + (self.$routes.params.id), {
			method: 'GET',
			headers: {
				"A-T": self.$Ciphers.decode("Vigenere Cipher", self.$cookies.get("user") || "",
					["Pwd"]).split(";")[1] || ""
			}
		}).then((response) => {
			// console.log(response)
			if(response.ok && !response.redirected) {
				return response.json()
			} else {
				throw {
					'e_code': response.status,
					'error': response.statusText
				}
			}
		}).then((data) => {
			for(let i of data.logs) {
				self.logs.push(i)
			}
		}).catch(rej => {
			console.log(rej.error + ' kindly re-login')
			self.$router.push('/login') //remember
		})
	},
}
</script>

<style>

</style>
