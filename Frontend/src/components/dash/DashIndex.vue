<template>
<div id="dash container-fluid">
	<div class="row">
		<nav id="sidebarMenu" class="col-md-3 col-lg-2 d-md-block sidebar collapse" style="height:640px;background-color:#0dcaf0 ">
			<div class="flex-shrink-0 " style="background-color:#a3eeff">
				<a href="/" class="d-flex align-items-center pt-3 pb-2 mb-3 link-dark text-decoration-none border-bottom">
					<svg class="bi me-2" width="30" height="24">
						<use href="#" />
					</svg>
					<span class="fs-4 fw-semibold">Menu</span>
				</a>
				<ul class="list-unstyled ps-0">
					<li class="mb-1">
						<button class="btn btn-toggle align-items-left rounded collapsed" data-bs-toggle="collapse" data-bs-target="#home-collapse" aria-expanded="true"> Home </button>
						<div class="collapse show" id="home-collapse">
							<ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
								<li><a href="#" class="link-dark rounded">Overview</a></li>
								<li><a href="#" class="link-dark rounded">Updates</a></li>
								<li><a href="#" class="link-dark rounded">Reports</a></li>
							</ul>
						</div>
					</li>
					<li class="mb-1">
						<button class="btn btn-toggle align-items-left rounded collapsed" data-bs-toggle="collapse" data-bs-target="#dashboard-collapse" aria-expanded="false"> Dashboard </button>
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

<style>
body {
  min-height: 100vh;
  min-height: -webkit-fill-available;
}

html {
  height: -webkit-fill-available;
}

main {
  display: flex;
  flex-wrap: nowrap;
  height: 100vh;
  height: -webkit-fill-available;
  max-height: 100vh;
  overflow-x: auto;
  overflow-y: hidden;
}

.b-example-divider {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
  background-color: rgba(0, 0, 0, .1);
  border: solid rgba(0, 0, 0, .15);
  border-width: 1px 0;
  box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);
}

.bi {
  vertical-align: -.125em;
  pointer-events: none;
  fill: currentColor;
}

.dropdown-toggle { outline: 0; }

.nav-flush .nav-link {
  border-radius: 0;
}

.btn-toggle {
  display: inline-flex;
  align-items: flex-start;
  padding: .25rem .5rem;
  font-weight: 600;
  color: rgba(0, 0, 0, .65);
  background-color: transparent;
  border: 0;
}
.btn-toggle:hover,
.btn-toggle:focus {
  color: rgba(0, 0, 0, .85);
  background-color: #d2f4ea;
}

.btn-toggle::before {
  width: 1.25em;
  line-height: 0;
  content: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='rgba%280,0,0,.5%29' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 14l6-6-6-6'/%3e%3c/svg%3e");
  transition: transform .35s ease;
  transform-origin: .5em 50%;
}

.btn-toggle[aria-expanded="true"] {
  color: rgba(0, 0, 0, .85);
}
.btn-toggle[aria-expanded="true"]::before {
  transform: rotate(90deg);
}

.btn-toggle-nav a {
  display: inline-flex;
  padding: .1875rem .5rem;
  margin-top: .125rem;
  margin-left: 1.25rem;
  text-decoration: none;
}
.btn-toggle-nav a:hover,
.btn-toggle-nav a:focus {
  background-color: #d2f4ea;
}

.scrollarea {
  overflow-y: auto;
}

.fw-semibold { font-weight: 600; }
.lh-tight { line-height: 1.25; }

</style>
