$(document).ready(function () {

    $('a[href="#nav-stats"]').trigger("click");
    show_stats();

    $('a[id="nav-stats-tab"]').on('shown.bs.tab', function (e) {
        show_stats();
    });

    $('a[id="nav-comparison-tab"]').on('shown.bs.tab', function (e) {
        $('#nav-comparison').empty();

        var head_title = $('<h3>').text("Comparison of " + race_name + " with others");
        $('#nav-comparison').append(head_title);
    });

    $('a[id="nav-visualisation-tab"]').on('shown.bs.tab', function (e) {
        $('#nav-visualisation').empty();

        var url = "/race-detail/visualisation";
        var FD = new FormData();
        FD.append("race_name", race_name);

        $.ajax({
            url: url,
            type: 'POST',
            data: FD,
            processData: false,
            contentType: false
        }).done(function (data) {
            var object = $('<object>')
                .attr('type', "text/html")
                .attr('width', "750")
                .attr("height", "750")
                .attr('data', data['filename']);

            $('#nav-visualisation').append(object);
        });
    });
});

function show_stats() {
    $('#nav-stats').empty();

    var url = "/race-detail/statistics";
    var FD = new FormData();
    FD.append("race_name", race_name);

    $.ajax({
        url: url,
        type: 'POST',
        data: FD,
        processData: false,
        contentType: false
    }).done(function (data) {

        var head_title = $('<h3>').text("Stats of " + race_name);

        var table = $('<table>').addClass('table');
        var thead = $('<thead>').addClass('thead-dark');
        var tr = $('<tr>').append($('<th>').attr('scope', 'col').text("Stats"))
            .append($('<th>').attr('scope', 'col').text("Values"));
        thead.append(tr);
        table.append(thead);

        var tbody = $('<tbody>');

        $.each(data, function (i, item) {

            let row = $('<tr>');
            let title = $('<td>').text(i);
            let content = $('<td>').text(item);

            row.append(title).append(content);

            tbody.append(row);
        });

        table.append(tbody);

        $('#nav-stats').append(head_title);
        $('#nav-stats').append(table);
    });
}

