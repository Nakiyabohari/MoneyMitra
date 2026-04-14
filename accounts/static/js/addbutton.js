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

const overlay = document.querySelector(".page-overlay");
const sheet = document.querySelector(".bottom-sheet");

function openSheet(){
    overlay.classList.add("active");
    sheet.classList.add("active");
    document.body.classList.add("no-scroll"); // 🔥 stops scroll
}

function closeSheet(){
    overlay.classList.remove("active");
    sheet.classList.remove("active");
    document.body.classList.remove("no-scroll"); // 🔥 enable scroll back
}