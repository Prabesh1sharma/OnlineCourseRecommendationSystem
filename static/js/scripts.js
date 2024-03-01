console.log("js connected")

function showCourseDetails(courseId) {
    // Make an AJAX request to retrieve course details
    fetch(`/coursedetails/?ID=${courseId}`)
        .then(response => response.json())
        .then(data => {
            // Update the popup content with the retrieved course details
            document.querySelector('.layout .viewcoursedetails .headingcontainer h2').innerText = data['course name'];
            var paymentStatusElement = document.querySelector('.layout .viewcoursedetails .text');

                // Checking the value of data['is_paid']
                if (data['is-paid'] === true) {
                    paymentStatusElement.innerText = 'PAID';
                } else {
                    paymentStatusElement.innerText = 'FREE';
                }
            document.querySelector('.layout .viewcoursedetails .details .column1').innerHTML = `
                Genre : ${data.genre} <br>
                Source : ${data.source} <br>
                Level : ${data.level} <br>
                Published Year : ${data['published year']} <br>
                Instructor : ${data.Instructor} <br>
            `;
            document.querySelector('.layout .viewcoursedetails .details .column2').innerHTML = `
                Duration : ${data['duration(hr)']} hrs <br>
                No of Enrollments : ${data['no of enrollments']} <br>
                Ratings : ${data.rating} <br>
                No of Reviews : ${data.review} <br>
            `;
            var openCourseButton = document.querySelector('.layout .viewcoursedetails .open');
            openCourseButton.href = data.Url;
            

            // Display the popup
            document.querySelector('.layout .viewcoursedetails').style.display = 'flex';
        })
        .catch(error => {
            console.error('Error fetching course details:', error);
        });
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
