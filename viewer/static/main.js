function pop(elem, data) {
    let array = "";

    $.each(data, function (i, item) {
        if (elem === i) {
            delete data[elem];
            array = item;
        }
    });

    return array;
}

function filter_arrays(y_array, x_array) {
    let array = [[], []];

    for (let i = 0; i < y_array.length; i++) {
        let y_value = y_array[i];
        let x_value = x_array[i];

        if (y_value > 0) {
            array[0].push(parseFloat(x_value).toFixed(2));
            array[1].push(y_value.toFixed(2));
        }
    }

    return array;
}

function plot_graph(div, f_append, name, unit, y_array, x_array, color) {

    let data = filter_arrays(y_array, x_array);

    let config = {
        type: 'line',
        data: {
            labels: data[0],
            datasets: [{
                label: name,
                fill: true,
                backgroundColor: color,
                borderColor: color,
                pointRadius: 0,
                data: data[1],
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: name + " graph"
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Distance (km)'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: name + " " + unit
                    }
                }]
            }
        }
    };

    let id_name = name + "_" + div;

    let canvas = $('<canvas>').attr("id", id_name);

    f_append(canvas, div);

    let ctx = id_name;

    window.myLine = new Chart(ctx, config);
}

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

        var distances = pop('distances', data);
        var speeds = pop('speeds', data);
        var bpms = pop('bpms', data);
        var heights = pop('heights', data);


        var table = $('<table>').addClass('table');
        var thead = $('<thead>').addClass('thead-dark');
        var tr = $('<tr>').append($('<th>').attr('scope', 'col').text("Stats"))
            .append($('<th>').attr('scope', 'col').text("Values"));
        var tbody = $('<tbody>');

        thead.append(tr);
        table.append(thead);

        $.each(data, function (i, item) {

            let row = $('<tr>');
            let title = $('<td>').text(i);
            let content = $('<td>').text(item);

            row.append(title).append(content);

            tbody.append(row);
        });

        table.append(tbody);

        let container = $('<div>').addClass("container-full").attr("id", "stats_content");

        let row = $('<div>').addClass("row");
        let col = $('<div>').addClass("col-12");

        let div_id = "stats_graphs";
        let row_graphs = $('<div>').addClass("row justify-content-center").attr("id", div_id);

        col.append(table);
        row.append(col);

        container.append(row);
        container.append(row_graphs);

        $('#nav-stats').append(container);

        function f_append(canvas, div) {
            let col = $('<div>').addClass("col-3");
            col.append(canvas);
            $("#" + div).append(col);
        }

        plot_graph(div_id, f_append, "Speed", "(km/h)", speeds, distances, window.chartColors.red);
        plot_graph(div_id, f_append, "BPM", "", bpms, distances, window.chartColors.blue);
        plot_graph(div_id, f_append, "Height", "(m)", heights, distances, window.chartColors.green);
    });
}

function show_comparison() {
    $('#nav-comparison').empty();

    var head_title = $('<h3>').text("Comparison of " + race_name + " with others");

    $('#nav-comparison').append(head_title);
}

function show_visualisation() {
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
}

$(document).ready(function () {

    $('a[href="#nav-stats"]').trigger("click");
    show_stats();

    $('a[id="nav-stats-tab"]').on('shown.bs.tab', function (e) {
        show_stats();
    });

    $('a[id="nav-comparison-tab"]').on('shown.bs.tab', function (e) {
        show_comparison();
    });

    $('a[id="nav-visualisation-tab"]').on('shown.bs.tab', function (e) {
        show_visualisation();
    });
});
