
function showTime(){
    var d = new Date();
    var year = d.getFullYear();
    var month = d.getMonth();
    var date = d.getDate();
    var hour = d.getHours();
    var min = d.getMinutes();
    var sec = d.getSeconds();


    hour = ("0" + hour).slice(-2);
    min = ("0" + min).slice(-2);
    sec = ("0" + sec).slice(-2);
    
    if(noclock !== null){
        var currentDateTime = d;
 
        var trainingYear = trainingDateTime.getFullYear();
        var trainingMonth = trainingDateTime.getMonth();
        var trainingDay = trainingDateTime.getDate();


        var diff = Math.abs(currentDateTime.getTime() - trainingDateTime.getTime());
        var diffHours = Math.floor(diff / 1000 / 60 / 60);
        diff -= diffHours * 1000 * 60 * 60;
        var diffMinutes = Math.floor(diff / 1000 / 60);

        

        noclock.innerHTML = diffHours+':'+diffMinutes;
        trainingMonth += 1;
        tDate.innerHTML = trainingDay+'-'+trainingMonth+'-'+trainingYear;
        
    }
    else{
        month += 1;
        clock.innerHTML = hour.padStart(2, '0')+':'+min.padStart(2, '0')+':'+sec.padStart(2, '0');
        cDate.innerHTML = date+'-'+month+'-'+year;
    }
}

var noclock = document.getElementById("noclock");
var clock = document.getElementById("clock");
var tDate = document.getElementById("training_date");
var cDate = document.getElementById("date");


if(noclock !== null){
    var tDateTime = document.getElementById("datetime").innerHTML;
    trainingDateTime = new Date(tDateTime);
}

showTime();
setInterval(showTime,1000);
        
        
        