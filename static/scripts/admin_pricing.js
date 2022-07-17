pricing_s = pricing_s.replaceAll('&#34;', '"');
additional_services_s = additional_services_s.replaceAll('&#34;', '"');

var pricing =  JSON.parse(pricing_s);
var additional_services = JSON.parse(additional_services_s);
console.log(pricing);
console.log(additional_services);

const pricing_edit = new JSONEditor(document.getElementById("Pricing"), {})
const addit_edit = new JSONEditor(document.getElementById("Additional"), {}) 
// set json

pricing_edit.set(pricing)
addit_edit.set(additional_services)

// get json



function save(){
    var s_pricing = pricing_edit.get()
    var s_addi = addit_edit.get()
    $.ajax({
        type: "POST",
        url: '/adminka/pricing',
        data: JSON.stringify ({
            'pricing': s_pricing,
            'addit': s_addi
        }),
        success: alert,
        contentType: "application/json",
        dataType: 'json'
      });
}