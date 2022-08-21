<template>
<div class="trackers align-items-center">
	<!-- <table class='table table-bordered tracker_table'>
		<thead>
			<tr>
				<th>S.no</th>
				<th>Tracker name (last log time)</th>
				<th>Tracker description</th>
				<th>Add new log</th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody v-for="(t,index) in trackers" :key='t.tracker_id'>
			<tr>
				<td>{{index}}</td>
				<td><a :href="'/tracker/'+t.tracker_id">{{t.tracker_name}}</a> <span v-if="t.last_updated">({{t.last_updated | capitalize}})</span><span v-else> (-/-/- -:-:-)</span></td>
				<td>{{t.tracker_description}}</td>
				<td><a :href="'/'+t.tracker_id+'/log/add'">{{t.tracker_type}}+</a></td>
				<td>
					<button type="button" value="edit"><a :href="'/tracker/'+t.tracker_id+'/update'">Edit</a></button>
					<button type="button" value="delete"><a :href="'/tracker/'+t.tracker_id+'/delete'">Delete</a></button>
				</td>
			</tr>
		</tbody>
	</table> -->
	<div class="card-deck row row-cols-lg-3 row-cols-2 justify-content-center">
		<div class="col m-3" v-for="t in trackers" :key='t.tracker_id'>
			<div class="card border-success">
				<div class="card-header align-middle">
					<h4>{{t.tracker_id}}) {{t.tracker_name}}</h4>
				</div>
				<div class="card-body h5">
					<div class="card-title"></div>
					<div class="card-text"> Tracker type: {{t.tracker_type}}<br><br>
						<span v-if="t.tracker_description">Tracker description: {{t.tracker_description}}<br></span>
						<span class="text-muted" v-if='t.last_updated'><em>Last logged: {{t.last_updated|capitalize}}</em></span>
					</div>
				</div>
				<div class="card-footer collapse">
					<button type="button" value="edit"><a :href="'/tracker/'+t.tracker_id+'/update'">Edit</a></button>
					<button type="button" value="delete"><a :href="'/tracker/'+t.tracker_id+'/delete'">Delete</a></button>
				</div>
			</div>
		</div>
	</div>
</div>
</template>

<script>
import Vue from 'vue'
Vue.filter('capitalize', function(value) {
	if(!value) return ''
	value = value.toString()
	return value.slice(0, -7)
})
export default {
	data() {
		return {
			trackers: []
		}
	},
	beforeCreate() {
		let self = this
		fetch("http://localhost:5000/api/user/" + (self.$store.state.user), {
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
			for(let i of data.trackers) {
				self.trackers.push(i)
			}
		}).catch(rej => {
			console.log(rej.error + ' kindly re-login')
			self.$router.push('/login') //remember
		})
	},
}
</script>

<style scoped>
.table {
	border: hidden;
}

button {
	box-shadow: 0 6px 8px 0 rgba(0, 0, 0, 0.05), 0 6px 5px 0 rgba(0, 0, 0, 0.05);
	border-radius: 10px;
}

a {
	text-decoration: none;
}

.card {
	box-shadow: 0 6px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.1);
	background-color: #eb59e92e;
	border-radius: 15px;
	min-height: 15rem;
}

.card:hover {
	scale: 1.05;
	box-shadow: 0 0 0 2px #d0d0d0;
}

.card:hover .card-footer {
	display: inherit;
}
</style>
