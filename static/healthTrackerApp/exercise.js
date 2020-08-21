function darkMode() {
    var element = document.body;
    element.classList.toggle('dark-mode');
    element.getElementsByClassName("table").toggle('dark-mode');
}

$(document).ready(function() {
    $('#ExerciseType').change(function() {
        if ($(this).val() === "Choose from List") {
            $("#cardioForm").hide();
            $("#bodyWeightForm").hide();
            $("#weightliftForm").hide();
        };
        if ($(this).val() === "Cardio") {
            $("#cardioForm").show();
            $("#bodyWeightForm").hide();
            $("#weightliftForm").hide();
        };
        if ($(this).val() === "Weight Lifting") {
            $("#weightliftForm").show();
            $("#cardioForm").hide();
            $("#bodyWeightForm").hide();
        };
        if ($(this).val() === "Body Weight") {
            $("#bodyWeightForm").show();
            $("#cardioForm").hide();
            $("#weightliftForm").hide();


        };

    });
    // Body Weight show/hide box
    $('input[name=completedWithWeights]').on("change", function() {
        if ($(this).val() === "True") {
            $("#howHeavyWereWeights").show();
        }
        if ($(this).val() === "False"){
             $("#howHeavyWereWeights").hide();
        }
    });
    // Weight Lifting show/hide box
    $('input[name=completedWeightExercises]').on("change", function() {
        if ($(this).val() === "True") {
            $("#heavinessOfWeight").show();
        }
        if ($(this).val() === "False"){
             $("#heavinessOfWeight").hide();
        }
    });
    // By default hiding all input forms unless user clicks on a specific one
    $("#cardioForm").hide();
    $("#bodyWeightForm").hide();
    $("#weightliftForm").hide();
    $("#howHeavyWereWeights").hide();
    $("#heavinessOfWeight").hide();
});
