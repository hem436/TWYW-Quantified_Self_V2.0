let mychart=function(){
// var filter=this.$options.filters.date_format;
var xy = [];
var ylabel = [];
for (let i of this.tracker.log_objects) {
  let date= new Date(i.log_datetime)
  console.log(+date)
  xy.push([+date,i.log_value]);
  ylabel.push(i.log_value);
}
var echarts = this.$echarts;
var chartDom = document.getElementById("myChart");
var myChart = echarts.init(chartDom, null, {
  renderer: "svg",
  useDirtyRect: false
});
var option;
option = {
  title: {
    text: "Log Values",
    left: "center"
  },
  grid: {
    bottom: 100
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: "none"
      },
      restore: {},
      saveAsImage: {}
    }
  },
  tooltip: {
    trigger: "axis",
    axisPointer: {
      type: "cross",
      animation: false,
      label: {
        backgroundColor: "#505765"
      }
    }
  },
  legend: {
    data: ["Flow"],
    left: 10
  },
  dataZoom: [
    {
      show: true,
      realtime: true,
      start: 0,
      end: 100
    },
    {
      type: "inside",
      realtime: true,
      start: 0,
      end: 100
    }
  ],
  xAxis: [
    {
      type: "time",
      boundaryGap: false,
      // axisLine: { onZero: false },
      // prettier-ignore
      // data: xlabel
      // .map(function (str) {
      //       return str.replace(' ', '\n').slice(0,-7);
      //   })
    }
  ],
  yAxis: [
    {
      name: "Flow(m^3/s)",

      type: "value"
    }
  ],
  series: [
    {
      name: "Flow",
      type: "line",
      // areaStyle: {},
      lineStyle: {
        width: 1
      },
      // emphasis: {
      //   focus: "series"
      // },
      // markArea: {
      //   silent: true,
      //   itemStyle: {
      //     opacity: 0.3
      //   },
      //   data: [
      //     [
      //       {
      //         xAxis: "2009/9/12\n7:00"
      //       },
      //       {
      //         xAxis: "2009/9/22\n7:00"
      //       }
      //     ]
      //   ]
      // },
      // prettier-ignore
      data:xy
    }
  ]
};
window.addEventListener("resize", myChart.resize);
if((this.tracker.tracker_type=== "Time" ) || (this.tracker.tracker_type==="Multiple-choice")){
  console.log(option)
  option.yAxis[0].type='time';
  option.series[0].type='scatter';

}
option && myChart.setOption(option);
}

export default mychart;
