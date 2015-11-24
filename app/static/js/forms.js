// Use new select2 control for team or round
$( document ).ready(function() {
    // TODO setup fancy select fields
    $("#team_id").prepend("<option value='' selected='selected'></option>");
    $("#team_id").selectize({
        placeholder: "Select a team",
        openOnFocus: false,
        selectOnTab: true
    });


    $("#round_number").prepend("<option value='' selected='selected'></option>");
    $("#round_number").selectize({
        placeholder: "Select a round",
        openOnFocus: false,
        selectOnTab: true
    });

    // Focus on first element in the form
    $(":input:visible:first").focus();
});