"use strict";(self["webpackChunkvue_test"]=self["webpackChunkvue_test"]||[]).push([[635],{6635:function(t,s,a){a.r(s),a.d(s,{default:function(){return c}});var e=function(){var t=this,s=t._self._c;return s("div",{attrs:{id:"dash container-fluid"}},[s("div",{staticClass:"row d-flex"},[s("nav",{staticClass:"border col-md-3 col-lg-2 d-md-block sidebar collapse",attrs:{id:"sidebarMenu"}},[s("div",{},[s("a",{staticClass:"d-flex align-items-center pt-4 pb-3 link-dark text-decoration-none border-bottom",attrs:{href:"#"}},[s("svg",{staticClass:"bi me-2",attrs:{width:"30",height:"24"}},[s("use",{attrs:{href:a(6500)}})]),s("span",{staticClass:"fs-4 fw-semibold"},[t._v("Menu")])]),s("ul",{staticClass:"list-unstyled ps-0"},[s("li",{staticClass:"mb-1"},[s("button",{staticClass:"btn btn-toggle align-items-left rounded collapsed",attrs:{"data-bs-toggle":"collapse","data-bs-target":"#dashboard-collapse","aria-expanded":"true"}},[t._v(" Dashboard ")]),s("div",{staticClass:"collapse show",attrs:{id:"dashboard-collapse"}},[s("ul",{staticClass:"btn-toggle-nav list-unstyled fw-normal pb-1 small"},[s("li",[s("router-link",{attrs:{to:"/dashboard"}},[t._v("Overview")])],1),t._m(0),s("li",[s("router-link",{attrs:{to:"/report"}},[t._v("Reports")])],1)])])]),s("li",{staticClass:"mb-1"},[s("button",{staticClass:"btn btn-toggle align-items-center rounded collapsed",attrs:{"data-bs-toggle":"collapse","data-bs-target":"#tracker-collapse","aria-expanded":"true"}},[t._v(" Trackers ")]),s("div",{staticClass:"collapse show",attrs:{id:"tracker-collapse"}},[s("ul",{staticClass:"btn-toggle-nav list-unstyled fw-normal pb-1 small"},[s("li",[s("router-link",{attrs:{to:"/tracker/add"}},[t._v("New")])],1),s("li",[s("router-link",{attrs:{to:"/export/tracker"}},[t._v("Export")])],1),s("li",[s("router-link",{attrs:{to:"/import/tracker"}},[t._v("Import")])],1)])])]),s("li",{staticClass:"mb-1"},[s("button",{staticClass:"btn btn-toggle align-items-center rounded collapsed",attrs:{"data-bs-toggle":"collapse","data-bs-target":"#log-collapse","aria-expanded":"true"}},[t._v(" Logs ")]),s("div",{staticClass:"collapse show",attrs:{id:"log-collapse"}},[s("ul",{staticClass:"btn-toggle-nav list-unstyled fw-normal pb-1 small"},[s("li",[s("router-link",{staticClass:"link-dark rounded",attrs:{to:"/log/add"}},[t._v(" New ")])],1),t._m(1),t._m(2)])])]),s("li",{staticClass:"border-top my-3"}),s("li",{staticClass:"mb-1"},[s("button",{staticClass:"btn btn-toggle align-items-center rounded collapsed",attrs:{"data-bs-toggle":"collapse","data-bs-target":"#account-collapse","aria-expanded":"false"}},[t._v(" Account ("+t._s(t.username)+") ")]),s("div",{staticClass:"collapse",attrs:{id:"account-collapse"}},[s("ul",{staticClass:"btn-toggle-nav list-unstyled fw-normal pb-1 small"},[t._m(3),t._m(4),t._m(5),s("li",[s("a",{staticClass:"link-dark rounded",on:{click:t.signout}},[t._v("Sign out")])])])])])])])]),s("div",{staticClass:"col-md-9 ms-sm-auto col-lg-10 px-md-4"},[s("div",{staticClass:"d-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom"},[s("h1",{staticClass:"h2"},[t._v("Dashboard")]),s("div",{staticClass:"p-2"},[s("a",{staticClass:"px-1",attrs:{type:"button"},on:{click:function(s){return t.$router.go()}}},[s("img",{attrs:{src:a(4582),width:"35",alt:"refresh","data-bs-toggle":"tooltip",title:"refresh"}})]),s("a",{staticClass:"px-1",attrs:{type:"button",tooltip:"go back"},on:{click:function(s){return t.$router.go(-1)}}},[s("img",{attrs:{src:a(6781),width:"35",alt:"back","data-bs-toggle":"tooltip",title:"go back"}})]),s("a",{staticClass:"px-1",attrs:{type:"button",tooltip:"forward"},on:{click:function(s){return t.$router.go(1)}}},[s("img",{attrs:{src:a(3342),width:"35",alt:"next","data-bs-toggle":"tooltip",title:"go next"}})])])]),s("router-view",{key:t.$route.fullPath})],1)])])},l=[function(){var t=this,s=t._self._c;return s("li",[s("a",{staticClass:"link-dark rounded",attrs:{href:"#"}},[t._v("Activity")])])},function(){var t=this,s=t._self._c;return s("li",[s("a",{staticClass:"link-dark rounded",attrs:{href:"#"}},[t._v("Export")])])},function(){var t=this,s=t._self._c;return s("li",[s("a",{staticClass:"link-dark rounded",attrs:{href:"#"}},[t._v("Import")])])},function(){var t=this,s=t._self._c;return s("li",[s("a",{staticClass:"link-dark rounded",attrs:{href:"#"}},[t._v("New...")])])},function(){var t=this,s=t._self._c;return s("li",[s("a",{staticClass:"link-dark rounded",attrs:{href:"#"}},[t._v("Profile")])])},function(){var t=this,s=t._self._c;return s("li",[s("a",{staticClass:"link-dark rounded",attrs:{href:"#"}},[t._v("Settings")])])}],r={data(){return{username:this.$store.state.user,update:0}},methods:{force_update(){this.update++},signout(){this.$cookies.remove("user"),this.$router.go()}}},i=r,o=a(1001),n=(0,o.Z)(i,e,l,!1,null,null,null),c=n.exports},6781:function(t,s,a){t.exports=a.p+"img/back.0b3275c1.svg"},6500:function(t,s,a){t.exports=a.p+"img/details.036ec9eb.svg"},3342:function(t,s,a){t.exports=a.p+"img/next.e6185c42.svg"},4582:function(t,s,a){t.exports=a.p+"img/refresh.fbfe4bf2.svg"}}]);
//# sourceMappingURL=635.3876cb3a.js.map