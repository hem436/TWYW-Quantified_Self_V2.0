
const stopwatch=
{
hour:0,
sec:0,
min: 0,
dispHour:0,
dispMin:0,
dispSec:0,
timeoutId:null,
check:'start',
timer: function() {
  console.log("from timer")
  console.log(this)
  stopwatch.sec++;
  if (stopwatch.sec / 60 == 1) {
    stopwatch.min++;
    stopwatch.sec = 0;
    if (stopwatch.min / 60 == 1) {
      stopwatch.hour++;
      stopwatch.min = 0;
    }
  }
  if (stopwatch.sec < 10) {
    stopwatch.dispSec = "0" + stopwatch.sec.toString();
  } else {
    stopwatch.dispSec = stopwatch.sec.toString();
  }
  if (stopwatch.min < 10) {
    stopwatch.dispMin = "0" + stopwatch.min.toString();
  } else {
    stopwatch.dispMin = stopwatch.min.toString();
  }
  if (stopwatch.hour < 10) {
    stopwatch.dispHour = "0" + stopwatch.hour.toString();
  } else {
    stopwatch.dispHour = stopwatch.hour.toString();
  }
  document.getElementById("log_val").value =
    stopwatch.dispHour + ":" + stopwatch.dispMin + ":" + stopwatch.dispSec;
},
start: function() {
  if(this.check==='start'){
  this.timeoutId = window.setInterval(this.timer, 1000);
  document.getElementById("start").innerHTML = "Stop";
this.check='stop'}
  else{
  window.clearInterval(this.timeoutId);
  document.getElementById("start").innerHTML = "Start";
this.check='start'}
},
reset: function() {
  window.clearInterval(this.timeoutId);
  (this.sec = 0), (this.min = 0), (this.hour = 0);
  document.getElementById("log_val").value = "00:00:00";
  document.getElementById("start").innerHTML = "Start";
}
}
export default stopwatch;
