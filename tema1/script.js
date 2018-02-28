document.getElementById('btn').addEventListener('click', function (e) {

    e.preventDefault;
    var input = document.getElementById('artist').value;

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "https://rest.bandsintown.com/artists/" + input + "?app_id=p",
        "method": "GET"

    }

    $.ajax(settings).done(function (response) {


        document.getElementById('name').textContent = response.name;
        document.getElementById('photo').innerHTML = '<a target="_blank" href =' + response.facebook_page_url + '><img class="overlay" src = ' + response.image_url + ' alt =' + response.name + ' href = ' + response.facebook_page_url + ' height = "400"></a>'


        artist_name = response.name;

        var settings = {
            "async": true,
            "crossDomain": true,
            "url": "https://itunes.apple.com/search?term=" + artist_name,
            "method": "GET"
        }

        $.ajax(settings).done(function (response) {
            json = JSON.parse(response);





            document.getElementById('table').innerHTML = '<br><table class="table table-bordered"><thead><tr><th>Song</th><th>Release date</th><th>Price (USD)</th><th>PRICE (RON) </th></tr></thead><tbody id="table_body">';
            for (i in json.results) {



                let track = json.results[i];


                var settings = {
                  "async": true,
                  "crossDomain": true,
                  "url": "https://api.fixer.io/latest?base="+track.currency,
                  "method": "GET"
                };

                $.ajax(settings).done(function (response) {


                    document.getElementById('table_body').innerHTML += '<tr><td>' + track.trackName + '</td><td>' + track.releaseDate.substring(0, 10) + '</td><td>' + track.trackPrice + '</td><td>  ' + track.trackPrice * response.rates.RON +' </td></tr>'

                });

                                    // document.getElementById('table_body').innerHTML += '<tr><td>' + track.trackName + '</td><td>' + track.releaseDate.substring(0, 9) + '</td><td>' + track.trackPrice + '</td><td>  ' + track.trackPrice+' </td></tr>'


            }

            document.getElementById('table').innerHTML += '</tbody></table>';
        });


    });


});


function getEuroPrice(currency){

}
