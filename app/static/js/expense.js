var amount_field = document.getElementById('amount');
amount_field.setAttribute('class','form-control');
amount_field.setAttribute('step','.01');
amount_field.setAttribute('type','number');
amount_field.setAttribute('placeholder','0.00');

var location_field = document.getElementById('location');
location_field.setAttribute('class','form-control');
location_field.setAttribute('placeholder','Whole Foods');

var date_field = document.getElementById('date');
date_field.setAttribute('class','form-control');
date_field.setAttribute('type','date');

var time_field = document.getElementById('time');
time_field.setAttribute('class','form-control');
time_field.setAttribute('type','time');
time_field.setAttribute('step','1');

var type_field = document.getElementById('type');
type_field.setAttribute('class','form-control');
type_field.setAttribute('placeholder','Groceries');

var button = document.getElementById('submit');
button.setAttribute('class','btn btn-primary');