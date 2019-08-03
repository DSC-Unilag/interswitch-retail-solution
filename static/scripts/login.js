let manufacturer = document.getElementById("manufacturer");
let consumer = document.getElementById("consumer");
manufacturer.addEventListener("click", changeToManufacturer);
consumer.addEventListener("click", changeToConsumer);

function changeToConsumer() {
   let x = document.getElementsByTagName("p");
   let y = document.getElementsByTagName("button");
   manufacturer.style.fontWeight = "normal";
   consumer.style.fontWeight = "bold";
   for(let i =0; i < x.length; i++){
    x[i].style.color = "#083A55";
   }
   for(let i =0; i < y.length; i++){
    y[i].style.background = "#083A55";
   }
}

function changeToManufacturer() {
    let x = document.getElementsByTagName("p");
    let y = document.getElementsByTagName("button");
    manufacturer.style.fontWeight = "bold";
   consumer.style.fontWeight = "normal";
    for(let i =0; i < x.length; i++){
     x[i].style.color = "#169FE9";
    }
    for(let i =0; i < y.length; i++){
     y[i].style.background = "#169FE9";
    }
 }
