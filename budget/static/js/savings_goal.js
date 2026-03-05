/* OPEN MODAL */
function openModal(){
document.getElementById("goalModal").style.display="flex"
}

function goBack(){
window.history.back()
}

/* CLOSE MODAL */
function closeModal(){
document.getElementById("goalModal").style.display="none"
}

/* COLOR SELECT */

let selectedColor="#6c63ff"

function selectColor(element,color){

selectedColor=color

document.getElementById("goalColor").value=color

const colors=document.querySelectorAll(".color")

colors.forEach(c=>{
c.classList.remove("active")
})

element.classList.add("active")

}

/* ADD MONEY */

function addMoney(goalId,amount){

fetch(`/budget/add_money/${goalId}/${amount}/`,{
method:"GET"
})
.then(response=>response.json())
.then(data=>{
location.reload()
})

}

/* DELETE GOAL */

function deleteGoal(goalId){

if(!confirm("Delete this goal?")) return

fetch(`/budget/delete_goal/${goalId}/`,{
method:"GET"
})
.then(response=>response.json())
.then(data=>{
location.reload()
})

}

/* PROGRESS LIMIT FUNCTION (MAX 100%) */

function updateProgress(saved,goal,barId,textId){

let percent=(saved/goal)*100

/* LIMIT TO 100% */
percent=Math.min(percent,100)

document.getElementById(barId).style.width=percent+"%"

document.getElementById(textId).innerText=percent.toFixed(1)+"% achieved"

}

/* CLOSE MODAL CLICK OUTSIDE */

window.onclick=function(event){

const modal=document.getElementById("goalModal")

if(event.target===modal){
modal.style.display="none"
}

}
