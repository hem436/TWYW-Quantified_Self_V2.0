var that=this;
const stopwatch=
{
hour:0,sec:0,min: 0,
dispHour:0,
  dispMin:0,
  dispSec:0,timeoutId:null,
timer: function(that) {
  that.sec++;
  if (that.sec / 60 == 1) {
    that.min++;
    that.sec = 0;
    if (that.min / 60 == 1) {
      that.hour++;
      that.min = 0;
    }
  }
  if (that.sec < 10) {
    that.dispSec = "0" + that.sec.toString();
  } else {
    that.dispSec = that.sec.toString();
  }
  if (that.min < 10) {
    that.dispMin = "0" + that.min.toString();
  } else {
    that.dispMin = that.min.toString();
  }
  if (that.hour < 10) {
    that.dispHour = "0" + that.hour.toString();
  } else {
    that.dispHour = that.hour.toString();
  }
  document.getElementById("timer").innerHTML =
    that.dispHour + ":" + that.dispMin + ":" + that.dispSec;
},
start: function(that) {
  console.log("watch");
  that.timeoutId = window.setInterval(that.timer, 1000);
  document.getElementById("start").innerHTML = "Stop";
},
stop: function() {
  window.clearInterval(that.timeoutId);
  document.getElementById("start").innerHTML = "Start";
},
reset: function(that) {
  window.clearInterval(that.timeoutId);
  (that.sec = 0), (that.min = 0), (that.hour = 0);
  document.getElementById("timer").innerHTML = "00:00:00";
  document.getElementById("start").innerHTML = "Start";
}
}
export default stopwatch;
