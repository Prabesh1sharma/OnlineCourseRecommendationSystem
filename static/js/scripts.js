console.log("js connected")
function showCourseDetails(){
    document.querySelector(".layout .viewcoursedetails").style.display = "flex";
}
function hideCourseDetails(){
    document.querySelector(".layout .viewcoursedetails").style.display = "none";
}
function showhideSortList(){
    document.querySelector(".layout .sortlist").classList.toggle("show");
}
function showhideUserProfile(){
    document.querySelector("#dropdown").classList.toggle("show");
}
function showhideNavContents(){
    document.querySelector("nav .navcontents").classList.toggle("showblock");
}
function showRating(){
    document.querySelector(".layout .sortlist li.rating").classList.toggle("show");
    document.querySelector(".layout .sortlist li.rating2").classList.toggle("show");
}
function showLevel(){
    document.querySelector(".layout .sortlist li.level").classList.toggle("show");
    document.querySelector(".layout .sortlist li.level2").classList.toggle("show");
}
function showDuration(){
    document.querySelector(".layout .sortlist li.duration").classList.toggle("show");
    document.querySelector(".layout .sortlist li.duration2").classList.toggle("show");
}

