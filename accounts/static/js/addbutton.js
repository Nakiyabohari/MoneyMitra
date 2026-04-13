function openSheet(){
    document.getElementById("bottom-sheet").classList.add("active");
    document.querySelector(".page-overlay").classList.add("active");
}

function closeSheet(){
    document.getElementById("bottom-sheet").classList.remove("active");
    document.querySelector(".page-overlay").classList.remove("active");
}

function goTo(route){
    window.location.href = route;
}