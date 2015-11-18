$(document).ready(function () {
    // Initialize the DataTable component
    var myTable = $('#teamsTable').DataTable({
        "searching": false,
        "ordering":  false,
        "lengthChange": false,
        "ajax": {
            "url": "/scores/api",
            "dataSrc": "ranks",
            "error": function() {
                alert("Unable to get data from server");
            }
        },
        "columns": [
            { "data": "rank", "class": "align_center" },
            { "data": "number", "class": "align_center"},
            { "data": "name", "class": "align_center" },
            { "data": "affiliation", "class": "align_center" },
            { "data": "round1", "class": "align_center" },
            { "data": "round2", "class": "align_center" },
            { "data": "round3", "class": "align_center" },
            { "data": "bestScore", "class": "align_center" }
        ],
        "info": false
    });

    // Set up the page looping
    var page = 1;
    var pageCount = myTable.page.info().pages;

    // Auto-advance through the datatable pages
    var page_advance = setInterval(function() {

        // If on the final page, reload the data then start again
        if(page >= pageCount) {
            console.log("reloading data");
            myTable.ajax.reload();
            myTable.page(0).draw(false);
            pageCount = myTable.page.info().pages;
            page = 0;
        }

        // Set the table page and redraw
        myTable.page(page).draw(false);
        page++;
    }, 10000);
});