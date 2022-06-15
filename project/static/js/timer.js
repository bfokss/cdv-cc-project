function formatDate(dateTime){
    return outputDate = String(dateTime.getDate()).padStart(2, '0')+"-"+String(dateTime.getMonth()+1).padStart(2, '0')+"-"+String(dateTime.getFullYear()).padStart(2, '0');
}

function formatTime(dateTime){
    return outputTime = String(dateTime.getHours()).padStart(2, '0')+":"+String(dateTime.getMinutes()).padStart(2, '0')+":"+String(dateTime.getSeconds()).padStart(2, '0');
}


function showTime(){
    var currentDateTime = new Date();
 
    if(noclock !== null){

        var diff = Math.abs(currentDateTime.getTime() - trainingDateTime.getTime());
        var diffHours = Math.floor(diff / 1000 / 60 / 60);
        diff -= diffHours * 1000 * 60 * 60;
        var diffMinutes = Math.floor(diff / 1000 / 60);


        noclock.innerHTML = String(diffHours).padStart(2, '0')+':'+String(diffMinutes).padStart(2, '0');
        tDate.innerHTML = formatDate(trainingDateTime);
        
    }
    else{
        clock.innerHTML = formatTime(currentDateTime);
        cDate.innerHTML = formatDate(currentDateTime);
    }
}


var noclock = document.getElementById("noclock");
var clock = document.getElementById("clock");
var tDate = document.getElementById("training_date");
var cDate = document.getElementById("date");


if(noclock !== null){
    var tDateTime = document.getElementById("datetime").innerHTML;
    var trainingDateTime = new Date(tDateTime);
}

showTime();
setInterval(showTime,1000);
        
        
        