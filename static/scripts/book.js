var main_checkbox = document.querySelector("input[id='main']");
var all_checkbox = document.querySelectorAll("input[type=checkbox]");
var table = document.querySelector("#table");
var price = Object.assign({"main": 0}, pricing, additional_services)
var div_sum = document.querySelector('.sub_total');
var div_tax = document.querySelector('.tax');
var div_total = document.querySelector('.end_sum')
var tax = 0.13


main_checkbox.addEventListener('change', function() {
    if (this.checked) {
        all_checkbox.forEach(element => {
            element.checked = true;
        });
    } else {
        all_checkbox.forEach(element => {
            element.checked = false;
        });
    }
});

table.addEventListener('change', function() {
    sum = 0;
    all_checkbox.forEach(element => {
        if(element.checked == false){
            main_checkbox.checked = false;
        }else{
            sum += price[element.id];
        }
    });
    div_sum.innerHTML = "SUB-TOTAL: $" + sum;
    div_tax.innerHTML = "SALES TAX: $" + Math.round((sum * 0.13)*100)/100;
    div_total.innerHTML = '$' + Math.round((sum * (1 + tax))*100)/100;
    
    console.log(sum);
})

