function map(num, in_min, in_max, out_min, out_max) {
  return (num - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

function customSigmoid(num,min,max){
  num = map(num,min,max,-2,2);
  num = 1.0/(Math.exp(-1*num)+1.0);
  return num;
}

function heatMapColorforValue(value){
  var h = (1.0 - value) * 240
  return "hsl(" + h + ", 100%, 50%)";
}

function mode(arr){
    return arr.sort((a,b) =>
          arr.filter(v => v===a).length
        - arr.filter(v => v===b).length
    )[arr.length-1]
}

function EuclideanDist(x1,x2){
  var SSE = 0;
  for(var i = 0; i < x1.length; i++){
    SSE += (x1[i]-x2[i])*(x1[i]-x2[i]);
  }
  EuclideanDistance = Math.sqrt(SSE);
  return EuclideanDistance;
}

function getCounts(arr){
  var best_label = mode(arr);
  var best_count = 0;
  var new_arr = [];
  for(var i = 0; i < arr.length; i++){
    if(arr[i]!=best_label){
      new_arr.push(arr[i]);
    }else{
      best_count += 1;
    }
  }
  arr = new_arr;
  var labels = [best_label];
  while(true){
    var new_label = mode(arr);
    var new_count = 0;
    var new_arr = [];
    for(var i = 0; i < arr.length; i++){
      if(arr[i]!=new_label){
        new_arr.push(arr[i]);
      }else{
        new_count += 1;
      }
    }
    if(new_count==best_count){
      arr = new_arr;
      labels.push(new_label);
    }else{
      to_return = [labels,best_count];
      return to_return;
    }
  }
}
