function darkMode() {
    var element = document.body;
    element.classList.toggle('dark-mode');
    element.getElementsByClassName("table").toggle('dark-mode');
}