"use strict";(self["webpackChunkvue_test"]=self["webpackChunkvue_test"]||[]).push([[10],{9010:function(t,e,s){s.r(e),s.d(e,{default:function(){return h}});var a=function(){var t=this,e=t._self._c;return e("div",{staticClass:"trackdetail"},[e("div",{staticClass:"row"},[e("div",{staticClass:"col-sm-10 offset-sm-1 col-lg-8 offset-lg-2 justify-content-center"},[e("h4",[t._v("Trend")]),t._m(0),e("div",{staticClass:"h4 d-flex"},[t._v("Log Entries")]),e("div",{staticClass:"table-responsive"},[e("table",{staticClass:"table"},[t._m(1),e("tbody",t._l(t.tracker.log_objects,(function(a,i){return e("tr",{key:a.log_datetime},[e("td",[t._v(t._s(i))]),e("td",[t._v(t._s(t._f("date_format")(a.log_datetime)))]),e("td",[t._v(t._s(a.log_value))]),e("td",[t._v(t._s(a.note))]),e("td",[e("div",{staticClass:"action d-flex"},[e("router-link",{attrs:{to:{name:"log.update",params:{id:a.log_id}}}},[e("img",{attrs:{src:s(9855),"data-bs-toggle":"tooltip",title:"Edit log"}})]),e("a",{on:{click:function(e){return e.preventDefault(),t.del(a.log_id)}}},[e("img",{attrs:{src:s(1734),"data-bs-toggle":"tooltip",title:"Delete log"}})])],1)])])})),0)])])]),e("div",{staticClass:"col",attrs:{align:"right"}},[e("router-link",{attrs:{to:{name:"log.add.id",params:{id:t.tracker_id}}}},[e("img",{attrs:{src:s(8112),width:"40",alt:"add log","data-bs-toggle":"tooltip",title:"Add log"}})]),t._m(2)],1)]),e("div",{staticClass:"offcanvas offcanvas-end",attrs:{tabindex:"-1",id:"alert","aria-labelledby":"alertLabel"}},[t._m(3),e("div",{staticClass:"offcanvas-body"},[e("form",{attrs:{id:"s_option"}},[e("div",{staticClass:"h5"},[t._v(" Schedule name: "+t._s(this.current_s.definition.name)+" "),e("button",{staticClass:"h6 m-2 btn btn-outline-danger",attrs:{type:"button"},on:{click:t.test_alert}},[t._v(" test now ")])]),e("div",{staticClass:"form-check form-switch"},[e("label",{staticClass:"form-check-label",attrs:{for:"switch"}},[t._v("On/Off")]),e("input",{directives:[{name:"model",rawName:"v-model",value:t.sw,expression:"sw"}],staticClass:"form-check-input",attrs:{type:"checkbox",role:"switch",name:"switch"},domProps:{checked:Array.isArray(t.sw)?t._i(t.sw,null)>-1:t.sw},on:{change:function(e){var s=t.sw,a=e.target,i=!!a.checked;if(Array.isArray(s)){var r=null,n=t._i(s,r);a.checked?n<0&&(t.sw=s.concat([r])):n>-1&&(t.sw=s.slice(0,n).concat(s.slice(n+1)))}else t.sw=i}}})]),e("div",{staticClass:"btn-group my-4"},[e("input",{staticClass:"btn-check",attrs:{type:"radio",name:"vbtn-radio",id:"Every hour"},on:{change:function(e){return t.onChange(e)}}}),e("label",{staticClass:"btn btn-outline-info",attrs:{for:"Every hour"}},[t._v("Every hour")]),e("input",{staticClass:"btn-check",attrs:{type:"radio",name:"vbtn-radio",id:"Every day"},on:{change:function(e){return t.onChange(e)}}}),e("label",{staticClass:"btn btn-outline-info",attrs:{for:"Every day"}},[t._v("Every day")]),e("input",{staticClass:"btn-check",attrs:{type:"radio",name:"vbtn-radio",id:"Every week"},on:{change:function(e){return t.onChange(e)}}}),e("label",{staticClass:"btn btn-outline-info",attrs:{for:"Every week"}},[t._v("Every week")]),e("input",{staticClass:"btn-check",attrs:{type:"radio",name:"vbtn-radio",id:"Every month"},on:{change:function(e){return t.onChange(e)}}}),e("label",{staticClass:"btn btn-outline-info",attrs:{for:"Every month"}},[t._v("Every month")]),e("input",{staticClass:"btn-check",attrs:{type:"radio",name:"vbtn-radio",id:"Every year"},on:{change:function(e){return t.onChange(e)}}}),e("label",{staticClass:"btn btn-outline-info",attrs:{for:"Every year"}},[t._v("Every year")])]),e("div",{staticClass:"my-3",attrs:{align:"center"}},[e("button",{staticClass:"btn btn-outline-primary",attrs:{type:"button",name:"button"},on:{click:t.schedule_alert}},[e("img",{attrs:{src:s(3613),"data-bs-toggle":"tooltip",title:"Schedule alert"}}),t._v("Schedule an alert ")])])])])])])},i=[function(){var t=this,e=t._self._c;return e("div",{staticClass:"container border mb-5"},[e("div",{staticClass:"chart",attrs:{id:"myChart"}})])},function(){var t=this,e=t._self._c;return e("thead",[e("tr",[e("th",[t._v("S.no")]),e("th",[t._v("Timestamp")]),e("th",[t._v("Value")]),e("th",[t._v("Note")]),e("th",[t._v("Actions")])])])},function(){var t=this,e=t._self._c;return e("a",{staticClass:"m-2",attrs:{type:"button","data-bs-toggle":"offcanvas","data-bs-target":"#alert","aria-controls":"alert"}},[e("img",{attrs:{src:s(6378),width:"40",alt:"alert","data-bs-toggle":"tooltip",title:"Schedule alert"}})])},function(){var t=this,e=t._self._c;return e("div",{staticClass:"offcanvas-header"},[e("div",{staticClass:"h3 m-4 ps-4",attrs:{id:"alertLabel"}},[t._v(" Scheduling an alert ")]),e("button",{staticClass:"btn-close text-reset",attrs:{type:"button","data-bs-dismiss":"offcanvas","aria-label":"Close"}})])}];let r=function(){var t=[];for(let n of this.tracker.log_objects){let e=new Date(n.log_datetime);t.push([+e,n.log_value])}t=t.sort((function(t,e){return e[0]-t[0]}));var e,s=this.$echarts,a=document.getElementById("myChart"),i=s.init(a,null,{renderer:"svg",useDirtyRect:!1});if(e={title:{text:this.tracker.tracker_name,left:"center"},grid:{bottom:100},toolbox:{feature:{dataZoom:{yAxisIndex:"none"},restore:{},saveAsImage:{}}},tooltip:{trigger:"axis",axisPointer:{type:"shadow"}},legend:{data:["Log value"],left:10},dataZoom:[{show:!0,realtime:!0,start:0,end:100},{type:"inside",realtime:!0,start:0,end:100}],xAxis:[{name:"Timestamp",nameLocation:"center",nameGap:30,type:"time",boundaryGap:!1}],yAxis:[{name:"Value",nameGap:20,type:"value",axisLine:{show:!0}}],series:[{name:"Log value",type:"line",lineStyle:{width:1},data:t}]},window.addEventListener("resize",i.resize),"Time"===this.tracker.tracker_type)e.series[0].data=e.series[0].data.map((function(t){return console.log(t[1].split(":")+" "+t[1].split(":")[1]),[t[0],3600*+t[1].split(":")[0]+60*+t[1].split(":")[1]+ +t[1].split(":")[2]]})),e.yAxis[0].axisLabel={formatter:"{value} sec"},e.series[0].type="line";else if("Multiple-choice"===this.tracker.tracker_type){let t=[];for(var r of(e.xAxis[0]={name:"Count",nameLocation:"center",nameGap:30,type:"value",boundaryGap:!1},e.dataZoom=[],e.yAxis=[{type:"category",inverse:!0}],this.tracker.settings.split(",")))t.push([this.tracker.log_objects.reduce((function(t,e){return e.log_value==r?++t:t}),0),r]);e.series[0]={name:"Log value",type:"bar",data:t}}e&&i.setOption(e)};var n=r,o={data(){return{tracker_id:this.$route.params.id,tracker:"",sw:"",s_option:"",current_s:{definition:{name:"no schedule"}}}},methods:{refresh(){var t=this;fetch("http://localhost:5000/api/tracker/"+this.tracker_id,{method:"GET",headers:{"A-T":t.$Ciphers.decode("Vigenere Cipher",t.$cookies.get("user")||"",["Pwd"]).split(";")[2]||""}}).then((t=>{if(t.ok&&!t.redirected)return t.json();throw{e_code:t.status,error:t.statusText}})).then((t=>{this.tracker=t})).catch((e=>{console.log(e.error+" kindly re-login"),t.$router.push("/login")})),fetch("http://localhost:5000/alert/"+this.tracker_id+"?switch="+this.sw,{method:"GET",headers:{"A-T":this.$Ciphers.decode("Vigenere Cipher",this.$cookies.get("user")||"",["Pwd"]).split(";")[2]||""}}).then((t=>{if(t&&t.ok)return t.json();throw t})).then((t=>{this.current_s=t.schedule,this.s_option=t.schedule.definition.args[1],this.sw=t.schedule.definition.enabled,document.getElementById(this.s_option).checked=!0})).catch((t=>{console.log(t.statusText),console.log(t.status+" kindly re-login")}))},del(t){if(window.confirm("Want to delete this log?")){let e=this;fetch("http://localhost:5000/api/log/"+t,{method:"DELETE",headers:{"A-T":e.$Ciphers.decode("Vigenere Cipher",e.$cookies.get("user")||"",["Pwd"]).split(";")[2]||""}}).then((t=>{if(t.ok&&!t.redirected)return this.refresh(),"";throw{e_code:t.status,error:t.statusText}})).catch((t=>{console.log(t.error+" kindly re-login")}))}},onChange(t){this.s_option=t.target.id,this.sw=!0},schedule_alert(){let t={schedule:this.s_option};fetch("http://localhost:5000/alert/"+this.tracker_id+"?switch="+this.sw,{method:"POST",headers:{"Content-Type":"application/json","A-T":this.$Ciphers.decode("Vigenere Cipher",this.$cookies.get("user")||"",["Pwd"]).split(";")[2]||""},body:JSON.stringify(t)}).then((t=>{if(t&&t.ok)return t.json();throw t})).then((t=>{this.current_s=t.schedule,this.sw=t.schedule.definition.enabled,document.getElementById(this.s_option).checked=!0,alert("scheduled")})).catch((t=>{400==t.status&&alert("select a schedule first")}))},test_alert(){let t={schedule:"now"};fetch("http://localhost:5000/alert/"+this.tracker_id,{method:"POST",headers:{"Content-Type":"application/json","A-T":this.$Ciphers.decode("Vigenere Cipher",this.$cookies.get("user")||"",["Pwd"]).split(";")[2]||""},body:JSON.stringify(t)}).then((t=>{if(t&&t.ok)return t.text()})).then((t=>{alert(t)})).catch((t=>{console.log(t),console.log(t.error+" kindly re-login")}))}},watch:{tracker:function(t){t.log_objects.length>0&&n.bind(this)()}},mounted(){this.refresh()}},l=o,c=s(1001),d=(0,c.Z)(l,a,i,!1,null,"3e1efa08",null),h=d.exports},8112:function(t,e,s){t.exports=s.p+"img/add.6684ef44.svg"},6378:function(t,e,s){t.exports=s.p+"img/alert.30b2aacc.svg"},1734:function(t,e,s){t.exports=s.p+"img/delete.b715afa5.svg"},9855:function(t,e,s){t.exports=s.p+"img/edit.5f32dc82.svg"},3613:function(t,e,s){t.exports=s.p+"img/timer.7afe14d4.svg"}}]);
//# sourceMappingURL=10.5031c5d8.js.map