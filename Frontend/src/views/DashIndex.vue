false<template>
  <div id="dash container-fluid">
    <div class="row d-flex">
      <nav
        id="sidebarMenu"
        class=" border col-md-3 col-lg-2 d-md-block sidebar collapse"
      >
        <div class="">
          <a
            href="#"
            class="d-flex align-items-center pt-4 pb-3 link-dark text-decoration-none border-bottom"
          >
            <svg class="bi me-2" width="30" height="24">
              <use href="@/assets/svg/details.svg" />
            </svg>
            <span class="fs-4 fw-semibold">Menu</span>
          </a>
          <ul class="list-unstyled ps-0">
            <li class="mb-1">
              <button
                class="btn btn-toggle align-items-left rounded collapsed"
                data-bs-toggle="collapse"
                data-bs-target="#dashboard-collapse"
                aria-expanded="true"
              >
                Dashboard
              </button>
              <div class="collapse show" id="dashboard-collapse">
                <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                  <li>
                    <router-link to="/dashboard">Overview</router-link>
                  </li>
                  <!-- <li>
                    <a href="#" class="link-dark rounded">Activity</a>
                  </li> -->
                  <li>
                    <router-link to="/report">Reports</router-link>
                  </li>
                </ul>
              </div>
            </li>
            <li class="mb-1">
              <button
                class="btn btn-toggle align-items-center rounded collapsed"
                data-bs-toggle="collapse"
                data-bs-target="#tracker-collapse"
                aria-expanded="true"
              >
                Trackers
              </button>
              <div class="collapse show" id="tracker-collapse">
                <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                  <li>
                    <router-link to="/tracker/add">New</router-link>
                  </li>

                  <li>
                    <router-link to="/import/tracker">Import</router-link>
                  </li>
                  <!-- <li><a href="#" class="link-dark rounded">Generate report</a></li> -->
                </ul>
              </div>
            </li>
            <li class="mb-1">
              <button
                class="btn btn-toggle align-items-center rounded collapsed"
                data-bs-toggle="collapse"
                data-bs-target="#log-collapse"
                aria-expanded="true"
              >
                Logs
              </button>
              <div class="collapse show" id="log-collapse">
                <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                  <li>
                    <router-link to="/log/add" class="link-dark rounded">
                      New
                    </router-link>
                  </li>

                  <li>
                    <router-link to="/import/log">Import</router-link>
                  </li>
                  <!-- <li><a href="#" class="link-dark rounded">Generate report</a></li> -->
                </ul>
              </div>
            </li>
            <li class="border-top my-3"></li>
            <li class="mb-1">
              <button
                class="btn btn-toggle align-items-center rounded collapsed"
                data-bs-toggle="collapse"
                data-bs-target="#account-collapse"
                aria-expanded="false"
              >
                Account ({{ username }})
              </button>
              <div class="collapse" id="account-collapse">
                <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">
                  <li>
                    <router-link to="/signup"> New...</router-link>
                  </li>
                  <li>
                    <router-link to="/profile"> Profile</router-link>
                  </li>
                  <li>
                    <a @click="signout" class="link-dark rounded">Sign out</a>
                  </li>
                </ul>
              </div>
            </li>
          </ul>
        </div>
      </nav>
      <div class="col-md-9 ms-sm-auto col-lg-10 px-md-4">
        <div
          class="d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom"
        >
          <h1 class="h2">Dashboard</h1>
          <div class="p-2">
            <a class="px-1" type="button" @click="$router.go()">
              <img
                src="@/assets/svg/refresh.svg"
                width="35"
                alt="refresh"
                data-bs-toggle="tooltip"
                title="refresh"
              />
            </a>
            <a
              class="px-1"
              type="button"
              tooltip="go back"
              @click="$router.go(-1)"
            >
              <img
                src="@/assets/svg/back.svg"
                width="35"
                alt="back"
                data-bs-toggle="tooltip"
                title="go back"
              />
            </a>

            <a
              class="px-1"
              type="button"
              tooltip="forward"
              @click="$router.go(1)"
            >
              <img
                src="@/assets/svg/next.svg"
                width="35"
                alt="next"
                data-bs-toggle="tooltip"
                title="go next"
              />
            </a>
          </div>
        </div>
        <router-view :key="$route.fullPath" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: this.$store.state.user,
      update: 0
    };
  },
  methods: {
    force_update() {
      this.update++;
    },
    signout() {
      this.$cookies.remove("user");
      this.$router.push("/login");
    }
  }
};
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
  /* flex-wrap: nowrap;
	height: 100vh;
	height: -webkit-fill-available;
	max-height: 100vh;
	overflow-x: auto;
	overflow-y: hidden; */
}
a {
  color: #000000;
  text-decoration: none;
}
.b-example-divider {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.1);
  border: solid rgba(0, 0, 0, 0.15);
  border-width: 1px 0;
  box-shadow: inset 0 0.5em 1.5em rgba(0, 0, 0, 0.1),
    inset 0 0.125em 0.5em rgba(0, 0, 0, 0.15);
}

.bi {
  vertical-align: -0.125em;
  pointer-events: none;
  fill: currentColor;
}

.dropdown-toggle {
  outline: 0;
}

.btn-toggle {
  display: inline-flex;
  align-items: flex-start;
  padding: 0.25rem 0.5rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.65);
  background-color: transparent;
  border: 0;
}

.btn-toggle:hover,
.btn-toggle:focus {
  color: rgba(0, 0, 0, 0.85);
  background-color: #d2f4ea;
}

.btn-toggle::before {
  width: 1.25em;
  line-height: 0;
  content: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 16 16'%3e%3cpath fill='none' stroke='rgba%280,0,0,.5%29' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M5 14l6-6-6-6'/%3e%3c/svg%3e");
  transition: transform 0.35s ease;
  transform-origin: 0.5em 50%;
}

.btn-toggle[aria-expanded="true"] {
  color: rgba(0, 0, 0, 0.85);
}

.btn-toggle[aria-expanded="true"]::before {
  transform: rotate(90deg);
}

.btn-toggle-nav a {
  display: inline-flex;
  padding: 0.1875rem 0.5rem;
  margin-top: 0.125rem;
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

.fw-semibold {
  font-weight: 600;
}

.lh-tight {
  line-height: 1.25;
}
</style>
