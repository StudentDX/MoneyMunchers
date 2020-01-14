var amount_field = document.getElementById('amount');
amount_field.setAttribute('class','form-control');
amount_field.setAttribute('step','.01');
amount_field.setAttribute('type','number');
amount_field.setAttribute('placeholder','0.00');

var location_field = document.getElementById('location');
location_field.setAttribute('class','form-control');
location_field.setAttribute('placeholder','Whole Foods');

var datetime_field = document.getElementById('datetime');
datetime_field.setAttribute('class','form-control');
datetime_field.setAttribute('placeholder','2020-1-16 12:00:00');

var type_field = document.getElementById('type');
type_field.setAttribute('class','form-control');
type_field.setAttribute('placeholder','Groceries');

var button = document.getElementById('submit');
button.setAttribute('class','btn btn-primary');