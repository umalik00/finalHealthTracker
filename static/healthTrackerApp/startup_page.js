var timeoutScreen;

function loadingFunction() {
    timeoutScreen = setTimeout(showPage, 3000);
}

function showPage() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("hiddenDiv").style.display = "block";
}