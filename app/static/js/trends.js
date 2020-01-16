var options = document.getElementsByTagName('option');
var interval = document.getElementById('hidden').innerHTML;
for (option of options) {
    if (interval.includes(option.getAttribute('value'))) {
        option.setAttribute('selected','');
    }
}