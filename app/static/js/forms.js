// Use new select2 control for team or round
$( document ).ready(function() {
    $("#team_id").selectize({
        placeholder: "Select a team",
        selectOnTab: true
    });

    $("#round_number").selectize({
        placeholder: "Select a round",
        selectOnTab: true
    });
});