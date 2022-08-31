let mychart=function(){
// var filter=this.$options.filters.date_format;

var xy = [];
for (let i of this.tracker.log_objects) {
  let date= new Date(i.log_datetime)
  xy.push([+date,i.log_value]);
}
var echarts = this.$echarts;
// console.log(echarts)
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
      type: 'shadow'
    }
    // axisPointer: {
    //   type: "cross",
    //   animation: false,
    //   label: {
    //     backgroundColor: "#505765"
    //   }
    // }
  },
  legend: {
    data: ["Log value"],
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
      name:"Timestamp",
      nameLocation:"center",
      nameGap:30,
      type: "time",
      boundaryGap: false,
      // axisLine: { onZero: false },
    }
  ],
  yAxis: [
    {
      name: "Log_value",
      nameGap:20,
      type: "value",
      axisLine:{
        show:true
      }
    }
  ],
  series: [
    {
      name: "Log value",
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

if(this.tracker.tracker_type=== "Time" ){
  option.series[0].data=option.series[0].data.map(function(a){
    console.log(a[1].split(':')+" "+a[1].split(':')[1])
    return [a[0],+a[1].split(':')[0]*3600+ +a[1].split(':')[1]*60+ +a[1].split(':')[2]]
  })
  option.yAxis[0].axisLabel= {
  formatter: '{value} sec'
  }
  option.series[0].type='line';
}

else if(this.tracker.tracker_type==='Multiple-choice'){
  let xy=[]
  option.xAxis[0]={
    name:"Count",
    nameLocation:"center",
    nameGap:30,
    type: "value",
    boundaryGap: false,
  }
  option.dataZoom=[]
  option.yAxis=[{
    type:'category',
    inverse:true
  }]
  for(var i of this.tracker.settings.split(',')){
    xy.push([this.tracker.log_objects.reduce(function(s,c){
      // console.log(i==c.log_value?s:"hey")
      return (c.log_value==i?++s:s)
    },0),i])
  }
// console.log(xy);
  option.series[0]={
    name:"Log value",
    type:"bar",
    data:xy
  }
}
// console.log(option)
option && myChart.setOption(option);
}

export default mychart;
