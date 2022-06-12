
function showTime(){
    var d = new Date();
    var year = d.getFullYear();
    var month = d.getMonth();
    var date = d.getDate();
    var day =d.getDay();
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


        var diff = currentDateTime.getTime() - trainingDateTime.getTime();
        var diffHours = Math.floor(diff / 1000 / 60 / 60);
        diff -= diffHours * 1000 * 60 * 60;
        var diffMinutes = Math.floor(diff / 1000 / 60);

        if(diffHours <= 0){
            diffHours = 24 + diffHours;
        }

        noclock.innerHTML = diffHours+':'+diffMinutes;
        trainingMonth += 1;
        console.log(trainingMonth);
        tDate.innerHTML = trainingDay+'-'+trainingMonth+'-'+trainingYear;
        
    }
    else{
        month += 1;
        clock.innerHTML = hour+':'+min+':'+sec;
        cDate.innerHTML = date+'-'+month+'-'+year;
    }
    
    //console.log(d);
    //console.log(trainingDateTime);
    

}

noclock = document.getElementById("noclock");
clock = document.getElementById("clock");
tDate = document.getElementById("training_date");
cDate = document.getElementById("date");


if(noclock !== null){
    var tYear = document.getElementById("year").innerHTML;
    var tMonth = document.getElementById("month").innerHTML;
    var tDay = document.getElementById("day").innerHTML;
    var tHour = document.getElementById("hour").innerHTML;
    var tMinute = document.getElementById("minute").innerHTML;
    var tSecond = document.getElementById("second").innerHTML;
    getTrainingDateTime = tYear+'-'+tMonth+'-'+tDay+' '+tHour+':'+tMinute+':'+tSecond;
    trainingDateTime = new Date(getTrainingDateTime);
}

showTime()
setInterval(showTime,1000);
        
        
        