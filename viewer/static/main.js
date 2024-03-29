var GLOBAL_DATA_STATS = {};

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

function plot_graph(container, f_append, name, unit, y_array, x_array, color, start, stop) {

    let data = filter_arrays(y_array, x_array);

    let graph_data = {
        labels: data[0],
        datasets: [{
            label: name,
            fill: true,
            backgroundColor: color,
            borderColor: color,
            pointRadius: 0,
            data: data[1]
        }]
    };

    if (start > 0) {
        let grey = window.chartColors.grey;
        let data_race = [];
        let data_segment = [];

        for (let i = 0; i < data[0].length; i++) {
            let lbl = data[0][i];

            if (lbl < start || lbl > stop) {
                data_race.push(data[1][i]);
                data_segment.push(NaN);
            } else {
                data_segment.push(data[1][i]);
                data_race.push(NaN);
            }
        }

        let datasets = [
            {
                label: "Race's " + name,
                fill: true,
                backgroundColor: grey,
                borderColor: grey,
                pointRadius: 0,
                data: data_race
            },
            {
                label: "Segment's " + name,
                fill: true,
                backgroundColor: color,
                borderColor: color,
                pointRadius: 0,
                data: data_segment
            }
        ];

        graph_data["datasets"] = datasets;
    }


    let config = {
        type: 'line',
        data: graph_data,
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
        },
        plugins: [{
            beforeRender: function (x, options) {
                for (let i = 0; i < x.data.datasets.length; i++) {
                    var c = x.chart;
                    var dataset = x.data.datasets[i];

                    let color = x.data.datasets[i].backgroundColor;

                    var gradientFill = c.ctx.createLinearGradient(0, 0, 0, c.height);
                    gradientFill.addColorStop(0, color);
                    gradientFill.addColorStop(1, 'white');

                    var model = x.data.datasets[i]._meta[Object.keys(dataset._meta)[0]].dataset._model;
                    model.backgroundColor = gradientFill;
                }
            }
        }]
    };

    let canvas = $('<canvas>').attr("width", "450").attr("height", "450");

    f_append(canvas, container);

    window.myLine = new Chart(canvas, config);
}

function add_table_stats(data, container, comparison=false) {

    container.find(".table-stats").empty();

    let table = $('<table>').addClass('table');
    let thead = $('<thead>').addClass('thead-dark');
    let tr = $('<tr>').append($('<th>').attr('scope', 'col').text("Stats"))
        .append($('<th>').attr('scope', 'col').text("Values"));

    if (comparison){
        tr.append($('<th>').attr('scope', 'col').text("Values compared race"));
        var second_race_data = data["seg2"];
        data = data["seg1"];
    }

    let tbody = $('<tbody>');

    thead.append(tr);
    table.append(thead);

    $.each(data, function (i, item) {

        let row = $('<tr>');
        let title = $('<td>').text(i);
        let content = $('<td>').text(item);

        row.append(title).append(content);

        if (comparison){
            let content2 = $('<td>').text(second_race_data[i]);
            row.append(content2);
        }

        tbody.append(row);
    });

    table.append(tbody);

    let row_table = container.find('.table-stats');
    let col = $('<div>').addClass("col-12");

    col.append(table);
    row_table.append(col);
}

function add_graphs_stats(container, f_append, distances, speeds, bpms, heights, start = -1, stop = Number.MAX_SAFE_INTEGER) {

    container.find(".graphs-stats").empty();

    plot_graph(container, f_append, "Speed", "(km/h)", speeds, distances, window.chartColors.red, start, stop);
    plot_graph(container, f_append, "BPM", "", bpms, distances, window.chartColors.blue, start, stop);
    plot_graph(container, f_append, "Height", "(m)", heights, distances, window.chartColors.green, start, stop);
}

function call_stats(container, f_append) {

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

        GLOBAL_DATA_STATS = JSON.parse(JSON.stringify(data)); //deep copy

        let distances = pop('distances', data);
        let speeds = pop('speeds', data);
        let bpms = pop('bpms', data);
        let heights = pop('heights', data);

        add_table_stats(data, container);

        add_graphs_stats(container, f_append, distances, speeds, bpms, heights);
    });
}

function add_segments_list(data) {
    let container = $('#segments-comparison');

    container.empty();

    let row = $('<div>').addClass("row h-100 justify-content-center");
    let col_button = $('<div>').addClass("col-2");
    let col_select = $('<div>').addClass("col-10");
    let button = $('<button>').addClass("btn btn-primary my-1").text("Compare");
    let select = $('<select>').addClass("custom-select my-1 mr-sm-2").attr("id", "select-segments");

    button.one("click", function () {
        call_comparison_visualisation();
        call_comparison_table();
        call_comparison_graphs();
    });

    $.each(data, function (i, item) {
        let comparison_race = item[0];
        let segment_type = item[1];

        let option = $('<option>').attr("value", comparison_race + "/" + segment_type)
            .text(comparison_race + "/" + segment_type);

        select.append(option);
    });

    col_button.append(button);
    col_select.append(select);
    row.append(col_button);
    row.append(col_select);
    row.css("margin-top", "50%");
    container.append(row);
}

function call_comparison_segments() {

    var url = "/race-detail/comparison_segments";
    var FD = new FormData();
    FD.append("race_name", race_name);

    $.ajax({
        url: url,
        type: 'POST',
        data: FD,
        processData: false,
        contentType: false
    }).done(function (data) {
        add_segments_list(data);
    });
}

function call_comparison_graphs() {

    let selected_segment = $("#select-segments option:selected").text();
    selected_segment = selected_segment.split('/');

    let comparison_race_name = selected_segment[0];
    let segment_type = selected_segment[1];

    var url = "/race-detail/comparison_graphs";
    var FD = new FormData();
    FD.append("race_name", race_name);
    FD.append("comparison_race_name", comparison_race_name);
    FD.append("segment_type", segment_type);

    $.ajax({
        url: url,
        type: 'POST',
        data: FD,
        processData: false,
        contentType: false
    }).done(function (data) {
        var container = $("#container-comparison");

        function f_append(canvas) {
            let row = $('<div>').addClass("row");
            let col = $('<div>').addClass("col-8");
            col.css("margin-left", "8%");
            col.append(canvas);
            row.append(col);
            container.find(".graphs-stats").append(row);
        }

        let start = data['start'];
        let stop = data['stop'];

        let distances = pop('distances', GLOBAL_DATA_STATS);
        let speeds = pop('speeds', GLOBAL_DATA_STATS);
        let bpms = pop('bpms', GLOBAL_DATA_STATS);
        let heights = pop('heights', GLOBAL_DATA_STATS);

        add_graphs_stats(container, f_append, distances, speeds, bpms, heights, start, stop)
    });
}

function call_comparison_table() {

    let selected_segment = $("#select-segments option:selected").text();
    selected_segment = selected_segment.split('/');

    let comparison_race_name = selected_segment[0];
    let segment_type = selected_segment[1];

    var url = "/race-detail/comparison_table";
    var FD = new FormData();
    FD.append("race_name", race_name);
    FD.append("comparison_race_name", comparison_race_name);
    FD.append("segment_type", segment_type);

    $.ajax({
        url: url,
        type: 'POST',
        data: FD,
        processData: false,
        contentType: false
    }).done(function (data) {
        let container = $("#container-comparison");
        add_table_stats(data, container, true);
    });
}

function call_comparison_visualisation() {

    let selected_segment = $("#select-segments option:selected").text();
    selected_segment = selected_segment.split('/');

    let comparison_race_name = selected_segment[0];
    let segment_type = selected_segment[1];

    var url = "/race-detail/comparison_visualisation";
    var FD = new FormData();
    FD.append("race_name", race_name);
    FD.append("comparison_race_name", comparison_race_name);
    FD.append("segment_type", segment_type);

    $.ajax({
        url: url,
        type: 'POST',
        data: FD,
        processData: false,
        contentType: false
    }).done(function (data) {

        let container = $('#segments-comparison');
        container.empty();

        let return_button = $('<button>').addClass("btn btn-primary my-1").text("Return");
        let form = $('<form>').attr("action", "/race-detail").attr("method", "post");
        let comparison_race_button = $('<button>').attr("type", "submit").addClass("btn btn-primary my-1").text(comparison_race_name);
        let hidden_input = $('<input>').attr("type", "hidden").attr("value", comparison_race_name).attr("name", "races");

        form.append(comparison_race_button);
        form.append(hidden_input);

        return_button.one("click", function () {
            call_comparison_segments();
            call_comparison_stats();
        });

        let object = $('<object>')
            .attr('type', "text/html")
            .attr('width', "650")
            .attr("height", "650")
            .attr('data', data['filename']);

        let row = $('<div>').addClass("row");
        let col_return = $('<div>').addClass("col-2");
        let col_form = $('<div>').addClass("col-3");

        col_return.append(return_button);
        col_form.append(form);

        row.append(col_return);
        row.append(col_form);

        container.append(row);
        container.append(object);
    });
}

function call_comparison_stats() {
    let container = $("#container-comparison");
    container.css("display", "flex");

    function f_append(canvas) {
        let row = $('<div>').addClass("row");
        let col = $('<div>').addClass("col-8");
        col.css("margin-left", "8%");
        col.append(canvas);
        row.append(col);
        container.find(".graphs-stats").append(row);
    }

    call_stats(container, f_append);
}

function show_stats() {
    var container = $("#container-stats");

    function f_append(canvas) {
        let row = container.find(".graphs-stats");
        let col = $('<div>').addClass("col-3");
        col.append(canvas);
        row.append(col);
    }

    call_stats(container, f_append);
}

function show_comparison() {
    call_comparison_stats();
    call_comparison_segments();
}

function show_visualisation() {
    $('#nav-visualisation').empty();

    let url = "/race-detail/visualisation";
    let FD = new FormData();
    FD.append("race_name", race_name);

    $.ajax({
        url: url,
        type: 'POST',
        data: FD,
        processData: false,
        contentType: false
    }).done(function (data) {
        let object = $('<object>')
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
