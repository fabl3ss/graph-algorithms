function SendFormWithAlgo(obj) {
    SetAlgorithm(obj);
    document.getElementById('form').submit();
}

function SetAlgorithm(obj) {
     document.getElementById('algorithm').value = obj;
}
