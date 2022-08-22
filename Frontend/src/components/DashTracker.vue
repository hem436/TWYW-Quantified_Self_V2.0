<template>
<div class="trackdetail">
	<div class="row">
		<div class="col-8 offset-2">
			<div class="h4 justify-content-center">Log Entries</div>
			<table class="table">
				<thead>
					<tr>
						<th>S.no</th>
						<th>Timestamp</th>
						<th>Value</th>
						<th>Note</th>
						<th>Actions</th>
					</tr>

					<tr v-for="(l,index) in logs" :key="l.log_id">
						<td>{{index}}</td>
						<td>{{l.log_datetime}}</td>
						<td>{{l.log_value}}</td>
						<td>{{l.note}}</td>
						<td><button type="button" name="button"><a :href="'/log/update/'+l.log_id">Edit</a></button>
							<button type="button" name="button"><a :href="'/log/delete/'+l.log_id">Delete</a></button>
						</td>
					</tr>

				</thead>
			</table>
			<div class='text-center'><button class="button h5" type="button"><a :href="'/log/add/'+tracker_id">Add Log</a></button>
			</div>
		</div>
	</div>
</div>
</template>

<script>
export default {
	data() {
		return {
			tracker_id:this.$route.params.id,
			logs: []
		}
	},
beforeMounted() {
		let self = this
		fetch("http://localhost:5000/api/tracker/" + self.$route.params.id, {
			method: 'GET',
			headers: {
				"A-T": self.$Ciphers.decode("Vigenere Cipher", self.$cookies.get("user") || "",
					["Pwd"]).split(";")[1] || ""
			}
		}).then((response) => {
			console.log(response)
			if(response.ok && !response.redirected) {
				return response.json()
			} else {
				throw {
					'e_code': response.status,
					'error': response.statusText
				}
			}
		}).then((data) => {
			console.log(data)
			for(let i of data.logs) {
				self.logs.push(i)
			}
		}).catch(rej => {
			console.log(rej)
			console.log(rej.error + ' kindly re-login')
			self.$router.push('/login') //remember
		})
	},
}
</script>

<style>

</style>
