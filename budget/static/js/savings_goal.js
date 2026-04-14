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


/* ADD MONEY QUICK BUTTON */

function addMoney(goalId,amount,target,current){

amount=Number(amount)
target=Number(target)
current=Number(current)

/* VALIDATION */

if(current + amount > target){
alert("Amount exceeds your savings goal")
return
}

fetch(`/budget/add_money/${goalId}/${amount}/`,{
method:"GET"
})
.then(response=>response.json())
.then(data=>{
location.reload()
})

}


/* ADD MONEY FROM INPUT */

function addMoneyInput(goalId,target,current){

let amount=document.getElementById("amountInput"+goalId).value

amount=Number(amount)
target=Number(target)
current=Number(current)

if(!amount || amount<=0){
alert("Enter valid amount")
return
}

/* CHECK LIMIT */

if(current + amount > target){
alert("Amount exceeds your savings goal")
return
}

fetch(`/budget/add_money/${goalId}/${amount}/`,{
method:"GET"
})
.then(response=>response.json())
.then(data=>{
location.reload()
})

}


/* REMOVE MONEY */

function removeMoneyInput(goalId,current){

let amount=document.getElementById("amountInput"+goalId).value

amount=Number(amount)
current=Number(current)

if(!amount || amount<=0){
alert("Enter valid amount")
return
}

/* CHECK SAVED LIMIT */

if(amount > current){
alert("You cannot remove more than saved amount")
return
}

fetch(`/budget/remove_money/${goalId}/${amount}/`,{
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