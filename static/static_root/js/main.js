function closeProgram(){
    let elem;
    let element;
    elem = document.getElementById("sp");
    element = document.getElementById("us")
    elem.style.display = "none";    
    element.style.display = "block";
};
function showQuotes(){
    let elem;
    let elem1;
    let elem2;
    elem = document.getElementById("hidden-q");
    elem1 = document.getElementById("hidden-goods");
    elem2 = document.getElementById("hidden-sers");
    elem1.style.display = "none";  
    elem2.style.display = "none";
    elem.style.display = "block";
};
function showGoods(){
    let elem;
    let elem1;
    let elem2;
    elem = document.getElementById("hidden-goods");
    elem1 = document.getElementById("hidden-q");
    elem2 = document.getElementById("hidden-sers");
    elem1.style.display = "none";  
    elem2.style.display = "none";
    elem.style.display = "block";
};
function showSers(){
    let elem;
    let elem1;
    let elem2;
    elem = document.getElementById("hidden-sers");
    elem1 = document.getElementById("hidden-goods");
    elem2 = document.getElementById("hidden-q");
    elem1.style.display = "none";  
    elem2.style.display = "none";
    elem.style.display = "block";
};
function show_Quotes(){
    let elem;
    let elem1;
    let elem2;
    let elem3;
    elem3 = document.getElementById("hidden-ar");
    elem = document.getElementById("hidden-qo");
    elem1 = document.getElementById("hidden-g");
    elem2 = document.getElementById("hidden-serv");
    elem3.style.display = "none"; 
    elem1.style.display = "none";  
    elem2.style.display = "none";
    elem.style.display = "block";
};
function show_Goods(){
    let elem;
    let elem1;
    let elem2;
    let elem3;
    elem3 = document.getElementById("hidden-ar");
    elem = document.getElementById("hidden-g");
    elem1 = document.getElementById("hidden-qo");
    elem2 = document.getElementById("hidden-serv");
    elem3.style.display = "none"; 
    elem1.style.display = "none";  
    elem2.style.display = "none";
    elem.style.display = "block";
};
function show_Sers(){
    let elem;
    let elem1;
    let elem2;
    let elem3;
    elem3 = document.getElementById("hidden-ar");
    elem = document.getElementById("hidden-serv");
    elem1 = document.getElementById("hidden-g");
    elem2 = document.getElementById("hidden-qo");
    elem3.style.display = "none"; 
    elem1.style.display = "none";  
    elem2.style.display = "none";
    elem.style.display = "block";
};
function show_Articles(){
    let elem;
    let elem1;
    let elem2;
    let elem3;
    elem3 = document.getElementById("hidden-ar");
    elem = document.getElementById("hidden-serv");
    elem1 = document.getElementById("hidden-g");
    elem2 = document.getElementById("hidden-qo");
    elem3.style.display = "block"; 
    elem1.style.display = "none";  
    elem2.style.display = "none";
    elem.style.display = "none";
};