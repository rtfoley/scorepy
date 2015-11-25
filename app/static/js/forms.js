// Use new select2 control for team or round
$( document ).ready(function() {
    // Don't set a placeholder on the select fields if this is an edit form
    if($('.form').attr("action") != "edit") {
        $("#team_id").prepend("<option value='' selected='selected'></option>");
        $("#round_number").prepend("<option value='' selected='selected'></option>");
    }

    $("#team_id").selectize({
        placeholder: "Select a team",
        selectOnTab: true
    });

    $("#round_number").selectize({
        placeholder: "Select a round",
        selectOnTab: true
    });
});