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

// document.onclick = function(obj){
//     if (!document.querySelector(".layout .sortlist").contains.obj.target){
//         document.querySelector(".layout .sortlist").classList.toggle("show");
//     }
// }
// document.addEventListener("click", function(event) {
//     if (event.target !== sortlist && !sortlist.contains(targetElement)) {
//         document.querySelector(".layout .sortlist").style.display = "none";
//     }
// });

// document.addEventListener("click", function(event) {
//     var sortlist = document.getElementById("sortlist");
//     var targetElement = event.target; 

//     if (targetElement.id !== "sorticon" && !sortlist.contains(targetElement)) {
//         sortlist.style.display = "none";
//     }
// });
