function darkMode() {
    var element = document.body;
    element.classList.toggle('dark-mode');
    element.getElementsByClassName("table").toggle('dark-mode');
}

// function that calculates the bmr based on what has been passed, via view
function bmrCalculation(bmr)
{
    var bmrPreCalc = parseFloat(bmr) || 0;
    var select = document.getElementById('exerciseFormControlSelect');
    switch (select.options[select.selectedIndex].text) {
        case "Sedentry":
            bmrPreCalc *= 1.2;
            break;
        case "Moderately active":
            bmrPreCalc *= 1.55;
            break;
        case"Highly active":
            bmrPreCalc *= 1.75;
            break;
    }

    document.getElementById('bmr').innerHTML = "BMR = " + bmrPreCalc + " calories";

}

// Function that is used to calcuate the calorie deficit that the user should be in to meet their goals
function weightToLose()
{
    var select = document.getElementById('weightFormControlSelect');
    switch (select.options[select.selectedIndex].value) {
        case "+2pw":
            document.getElementById('calorieDeficit').innerHTML = "need to be in a 1000 calorie surplus per day";
            break;
        case"+1pw":
            document.getElementById('calorieDeficit').innerHTML = "need to be in a 500 calorie surplus per day";
            break;
        case "0pw":
            document.getElementById('calorieDeficit').innerHTML = "need to be in 0 calorie deficit per day";
            break;
        case "-1pw":
            document.getElementById('calorieDeficit').innerHTML = "need to be in a 500 calorie deficit per day";
            break;
        case"-2pw":
            document.getElementById('calorieDeficit').innerHTML = "need to be in a 1000 calorie deficit per day";
            break;
    }
}