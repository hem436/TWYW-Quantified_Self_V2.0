"use strict";(self["webpackChunkvue_test"]=self["webpackChunkvue_test"]||[]).push([[166],{3166:function(e,t,r){r.r(t),r.d(t,{default:function(){return u}});var s=function(){var e=this,t=e._self._c;return t("div",{staticClass:"loginform"},[e._m(0),t("br"),t("div",{staticClass:"row"},[t("div",{staticClass:"form col-sm-6 offset-sm-3"},[t("h3",[e._v("User Login")]),t("label",{attrs:{for:"username"}},[e._v("Username:")]),t("br"),t("input",{directives:[{name:"model",rawName:"v-model",value:e.username,expression:"username"}],staticClass:"form-control",attrs:{type:"text",name:"username",required:""},domProps:{value:e.username},on:{input:function(t){t.target.composing||(e.username=t.target.value)}}}),t("br"),e.username_validate?e._e():t("h6",{staticStyle:{"font-family":"zillaslab,palatino,Palatino Linotype,serif",color:"red"}},[e._v(e._s(e.error.u))]),e._v(" "),t("br"),t("label",{attrs:{for:"password"}},[e._v("Enter your password:")]),t("br"),t("input",{directives:[{name:"model",rawName:"v-model",value:e.password,expression:"password"}],staticClass:"form-control",attrs:{type:"password",name:"password",required:""},domProps:{value:e.password},on:{input:function(t){t.target.composing||(e.password=t.target.value)}}}),t("br"),t("button",{attrs:{type:"button"},on:{click:e.login}},[e._v("Login")]),t("br"),e.password_validate?e._e():t("h6",{staticStyle:{"font-family":"zillaslab,palatino,Palatino Linotype,serif",color:"red"}},[e._v(e._s(e.error.p))]),e._v(" Not a member? "),t("a",{attrs:{href:"/signup"}},[e._v("Sign Up")])])])])},o=[function(){var e=this,t=e._self._c;return t("div",{staticClass:"row",attrs:{align:"center"}},[t("h1",[e._v("Welcome to TWYW")]),t("br"),t("br")])}],a={name:"LogIn",data(){return{username:"",password:"",error:{u:"",p:""}}},methods:{gen_uerror:function(e){this.error.u=e},gen_perror:function(e){this.error.p=e},login:function(){let e=this;if(this.username_validate&&this.password_validate){let t={username:this.username,password:this.password};console.log("going to login"),fetch("http://127.0.0.1:5000/api/login",{method:"POST",credentials:"include",headers:{"Content-Type":"application/json","Access-Control-Allow-Credentials":!0,"Access-Control-Allow-Origin":"http://localhost:8080"},body:JSON.stringify(t)}).then((function(e){if(e.ok)return e.json();throw"no response"})).then((function(t){e.$cookies.set("data",t.auth_token),console.log(t.auth_token),e.$cookies.set("user",e.$Ciphers.encode("Vigenere Cipher",t.username+";"+t.auth_token,["Pwd"])),window.location.href="/Dashboard"})).catch((e=>console.log(e)))}else alert("Invalid username or password")}},computed:{username_validate:function(){let e=/^[0-9a-zA-Z]*$/;return this.username.match(e)&&this.username.length>0?(this.gen_uerror(""),!0):(this.gen_uerror("Username must be alphanumeric"),!1)},password_validate:function(){let e=/^(?=.*).{8,}$/;return this.password.match(e)?(this.gen_perror(""),!0):(this.gen_perror("Password should be atleast 8 characters"),!1)}}},n=a,i=r(1001),l=(0,i.Z)(n,s,o,!1,null,null,null),u=l.exports}}]);
//# sourceMappingURL=166.1a7597e0.js.map