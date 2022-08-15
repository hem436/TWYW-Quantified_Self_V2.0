<template>
<div id="dash container-fluid">
	<div class="row">
		<nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block bg-light sidebar collapse">
			<div class="flex-shrink-0 p-2 bg-white" style="width: 280px;">
				<a href="/" class="d-flex align-items-center pt-3 pb-2 mb-3 link-dark text-decoration-none border-bottom">
					<svg class="bi me-2" width="30" height="24">
						<use href="#" />
					</svg>
					<span class="fs-4 fw-semibold">Menu</span>
				</a>
				<ul class="list-unstyled ps-0">
					<li class="mb-1">
						<button class="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse" data-bs-target="#home-collapse" aria-expanded="true"> Home </button>
						<div class="collapse show" id="home-collapse">
							<ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
								<li><a href="#" class="link-dark rounded">Overview</a></li>
								<li><a href="#" class="link-dark rounded">Updates</a></li>
								<li><a href="#" class="link-dark rounded">Reports</a></li>
							</ul>
						</div>
					</li>
					<li class="mb-1">
						<button class="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse" data-bs-target="#dashboard-collapse" aria-expanded="false"> Dashboard </button>
						<div class="collapse" id="dashboard-collapse">
							<ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
								<li><a href="#" class="link-dark rounded">Overview</a></li>
								<li><a href="#" class="link-dark rounded">Weekly</a></li>
								<li><a href="#" class="link-dark rounded">Monthly</a></li>
								<li><a href="#" class="link-dark rounded">Annually</a></li>
							</ul>
						</div>
					</li>
					<li class="mb-1">
						<button class="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse" data-bs-target="#orders-collapse" aria-expanded="false"> Orders </button>
						<div class="collapse" id="orders-collapse">
							<ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
								<li><a href="#" class="link-dark rounded">New</a></li>
								<li><a href="#" class="link-dark rounded">Processed</a></li>
								<li><a href="#" class="link-dark rounded">Shipped</a></li>
								<li><a href="#" class="link-dark rounded">Returned</a></li>
							</ul>
						</div>
					</li>
					<li class="border-top my-3"></li>
					<li class="mb-1">
						<button class="btn btn-toggle align-items-center rounded collapsed" data-bs-toggle="collapse" data-bs-target="#account-collapse" aria-expanded="false"> Account </button>
						<div class="collapse" id="account-collapse">
							<ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
								<li><a href="#" class="link-dark rounded">New...</a></li>
								<li><a href="#" class="link-dark rounded">Profile</a></li>
								<li><a href="#" class="link-dark rounded">Settings</a></li>
								<li><a href="#" class="link-dark rounded">Sign out</a></li>
							</ul>
						</div>
					</li>
				</ul>
			</div>
		</nav>
		<div class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
			<div class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom">
				<h1 class="h2">Dashboard</h1>
				<div class="btn-toolbar mb-2 mb-md-0">
					<div class="btn-group me-2">
						<button type="button" class="btn btn-sm btn-outline-secondary">Share</button>
						<button type="button" class="btn btn-sm btn-outline-secondary">Export</button>
					</div>
					<button type="button" class="btn btn-sm btn-outline-secondary dropdown-toggle">
						<span data-feather="calendar"></span> This week </button>
				</div>
			</div>
			<button type="button" name="button" @click="req('hem')">query</button>
			{{info}}
			<router-view />
		</div>
	</div>
</div>
</template>

<script>
export default {
	data() {
		return {
			info: ""
		}
	},
	methods: {
		req: function(user) {
			let self = this
			console.log(this.$Ciphers.encode("Vigenere Cipher", "Hello, World!@#$%^&*()_+-=", ["Pwd"]))
			let a = fetch("http://localhost:5000/api/user/" + user, {
				method: 'GET',
				headers: {
					// "A-T": atob(self.$cookies.get("user")).split(";")[1]
					"A-T": self.$Ciphers.decode("Vigenere Cipher", self.$cookies.get("user"),
						["Pwd"]).split(";")[1]
					// "A-T": "WyJiJyQyYiQxMiRDR3l1UXVETmhIRzBqRFR4YjRLYXNPJyJd.YveGPg.l7f2Wb1aaxZDX4EDkLySBAQBXpA"
					// WyJiJyQyYiQxMiRDR3l1UXVETmhIRzBqRFR4YjRLYXNPJyJd.YveH - w.p_Axi4m2ECFQE8fCrtXlRtQSkwA
				}
			})
			a.then(response => response.json()).then(function(res) {
				console.log(res);
				self.info = res;
			}).catch(rej => console.log(rej))
		}
	}
}
</script>
