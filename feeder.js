(function (global, $, undefined) {
    function main() {
        var $input = $('#textInput'),
            $results = $('#results');
        var ws = new WebSocket("ws://localhost:8080/ws");

        $input.keyup(function(ev) {
            var msg = { term: ev.target.value };
            ws.send(JSON.stringify(msg));
        });

        ws.onmessage = function(msg) {
            var value = JSON.parse(msg.data);
            if (value === "clear") {$results.empty(); return;}

            // Append the results
            $('<li><h3><a tabindex="-1" href="' + value.link +
                '">' + value.name +'</a></h3> <p> Description : ' + value.description +
                '</p><p> Language : ' + value.language +
                '</p><p> Stars : ' + value.stars + '</p></li>'
            ).appendTo($results);
            $results.show();
        }
    }
    main();
}(window, jQuery));

