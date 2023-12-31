let variable1=document.querySelector("#variable1");
let condition1=document.querySelector("#condition1");
let value1=document.querySelector("#value1");
let variable2=document.querySelector("#variable2");
let condition2=document.querySelector("#condition2");
let value2=document.querySelector("#value2");
let constraint=document.querySelector("#constraint");
let button=document.querySelector("#sub");

button.addEventListener("click", function(e){
    e.preventDefault();
    let a1=document.createElement("p");
    a1.innerText = "Enter " + variable1.value + " & " + variable2.value;

    let newForm = document.createElement("form");
    var input1 = document.createElement("input");
    input1.type = "text";
    input1.id = "text1";
    var input2 = document.createElement('input');
    input2.type = 'text';
    input2.id = "text2";
    var input3 = document.createElement('input');
    input3.type = 'submit';
    input3.id = "sub1";

    newForm.appendChild(input1);
    newForm.appendChild(input2);
    newForm.appendChild(input3);

    document.body.appendChild(a1);
    document.body.appendChild(newForm);

    let val1=document.querySelector("#text1");
    let val2=document.querySelector("#text2");



});