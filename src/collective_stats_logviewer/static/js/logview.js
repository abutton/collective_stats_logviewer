jQuery(document).ready(function() {
    $(document).on('ready', function(){
        $('dl.url-details dd').hide();
    });
    $(document).on('click', 'dt.url-help', function(){
        // Finds all the sibling dd elements of the link
        // clicked and toggles them as showing or not showing
        $(this).parents('dl').find('dd').toggle()
        // Grabs the url of the link that was clicked
        url = $(this).find('a').text()
        // Assigns graph_div to the corresponding div that will be used
        // to render the graph for the link
        graph_div =  $(this).parents('dl').find('div.graph-placeholder').first()
        plot(graph_div, url);
        // Need a fix so that ajax isn't called each time the dt.url-help link is clicked
    });
});

function plot(graph_div, url){
	var options = {
		lines: {
			show: true,
		},
		points: {
			show: true,
            fillColor: "#0062E3",
		},
        xaxis: { mode: "time",
                 timeformat: "%M:%S",
                 minTickSize: [1, "second"]
        },
        yaxis: {
            ticks: [0,0.5,1,2,3,4,6,10],
        },
        legend: {
            show: true
        }
	};

    var data = [];
    function onDataReceived(response) {
        $.each(response.graph_data, function(key, value){
            time = parseFloat(value.render_time);
            timestamp = (new Date(value.timestamp)).getTime();
            data.push([timestamp, time]);
        });

		$.plot(graph_div, [
        {
            label: "Render Time",
            data: data,
            color: "#0062E3",
        }
    ], options);

        // Find the <span>s for the link that was clicked and populated them with their
        // respective stats which were received during the ajax request.
        graph_div.parents('dl').find('.num-hits').text(response.stats_data.num_hits)
        graph_div.parents('dl').find('.cached-benefit').text(response.stats_data.cached_benefit)
        // For these next 2, jquery won't be able to find span.overall for a server choker,
        // or a span.avg for a slow page (since the avg is already set by Python as it's a header).
        // Doesn't seem to cause any problems, but is allowinig it to fail like this good practice?
        graph_div.parents('dl').find('.overall').text(response.stats_data.overall)
        graph_div.parents('dl').find('.avg').text(response.stats_data.avg)
	};

	$.ajax({
		url: '/reponse_time_details/',
		type: "GET",
        data: {'url': url},
		dataType: "json",
		success: onDataReceived
	});
}
