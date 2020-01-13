var fields = document.getElementsByTagName('input');
for (field of fields) {
    if (field.getAttribute('id') == 'amount') {
        field.setAttribute('class','form-control');
        field.setAttribute('step','.01');
        field.setAttribute('type','number');
        field.setAttribute('placeholder','0.00');
    }
}