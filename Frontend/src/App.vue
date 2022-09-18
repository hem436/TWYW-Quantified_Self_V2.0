<template>
  <div id="app">
    <header
      class="navbar navbar-dark  sticky-top bg-info flex-md-nowrap p-0 shadow"
    >
      <a
        class="fs-3  navbar-brand d-flex justify-content-center col-4 offset-4 px-3 "
        href="#"
        >TWYW-Quantified self</a
      >
      <button
        class="navbar-toggler position-absolute d-md-none collapsed"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#sidebarMenu"
        aria-controls="sidebarMenu"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <!-- <input class="form-control form-control-dark w-100" type="text" placeholder="Search" aria-label="Search"> -->
      <div class="btn-group">
        <button
          type="button"
          class="d-flex align-items-center justify-content-center p-3 link-dark text-decoration-none dropdown-toggle btn dropdown-toggle"
          data-bs-toggle="dropdown"
          data-bs-display="static"
          aria-expanded="false"
        >
          <img
            src="../public/img/userimg.png"
            alt="mdo"
            width="30"
            height="30"
            class="rounded-circle"
          />
        </button>

        <ul class="dropdown-menu dropdown-menu-end">
          <li>
            <router-link class="dropdown-item" to="/profile">
              Profile</router-link
            >
          </li>
          <hr class="dropdown-divider" />
          <li>
            <a @click="signout" class="dropdown-item" type="button">Sign out</a>
          </li>
        </ul>
      </div>
    </header>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
  methods: {
    signout() {
      this.$cookies.remove("user");
      this.$router.push("/login");
    }
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
