google.charts.load('current', { packages: ['corechart', 'bar'] });
google.charts.setOnLoadCallback(draw);

function draw0() {
    var data = google.visualization.arrayToDataTable([
        ['Genre', 'Diff with login cookie', "Diff with unlogin cookie", 'Same between login/unlogin cookie', 'No Cookie header'],
        ['airbnb.com', 0, 8, 32, 98],
        ['bestbuy.com', 0, 1, 12, 113],
        ['facebook.com', 2, 2, 10, 160],
        ['gmail.com', 2, 6, 34, 101],
        ['newlook.dteenergy.com', 8, 2, 56, 34],
        ['amazon.com', 1, 2, 18, 253],
        ['drive.google.com', 4, 2, 22, 37],
        ['github.com', 1, 2, 3, 11],
        ['linkedin.com', 4, 18, 18, 46],
        ['yelp.com', 0, 3, 6, 98],
        ['netflix.com', 1, 3, 5, 92],
        ['us-east-2.console.aws.amazon.com', 0, 2, 1, 40],
        ['dropbox.com', 2, 2, 113, 5],
        ['att.com/my', 0, 0, 11, 2]

    ]);

    var options = {
        title: 'Best',
        height: 1000,
        legend: { position: 'top', maxLines: 3 },
        bar: { groupWidth: '60%' },
        isStacked: true,
        bars: 'horizontal'
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
    chart.draw(data, options);
}

function draw1() {
    var data = google.visualization.arrayToDataTable([
        ['Genre', 'Diff with login cookie', "Diff with unlogin cookie", 'Same between login/unlogin cookie', 'No Cookie header'],
        ['airbnb.com', 3, 8, 27, 89],
        ['bestbuy.com', 0, 3, 6, 91],
        ['facebook.com', 4, 8, 2, 238],
        ['gmail.com', 2, 6, 24, 95],
        ['newlook.dteenergy.com', 9, 2, 52, 33],
        ['amazon.com', 6, 0, 18, 202],
        ['drive.google.com', 1, 1, 7, 21],
        ['github.com', 2, 1, 3, 10],
        ['linkedin.com', 6, 16, 16, 45],
        ['yelp.com', 4, 2, 2, 112],
        ['netflix.com', 1, 2, 6, 78],
        ['us-east-2.console.aws.amazon.com', 0, 2, 1, 43],
        ['dropbox.com', 2, 1, 115, 4],
        ['att.com/my', 0, 0, 11, 2],
        ['tumblr.com', 1, 0, 80, 24]

    ]);

    var options = {
        title: "Requests",
        height: 1000,
        legend: { position: 'top', maxLines: 3 },
        bar: { groupWidth: '60%' },
        isStacked: true,
        bars: 'horizontal'
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div1'));
    chart.draw(data, options);
}

function draw2() {
    var data = google.visualization.arrayToDataTable([
        ['Genre', 'Diff with login cookie', "Diff with unlogin cookie", 'Same between login/unlogin cookie', 'No Cookie header'],
        ['airbnb.com', 1, 8, 29, 89],
        ['bestbuy.com', 0, 2, 7, 91],
        ['facebook.com', 3, 4, 7, 238],
        ['gmail.com', 1, 4, 27, 95],
        ['newlook.dteenergy.com', 8, 2, 53, 33],
        ['amazon.com', 2, 2, 20, 202],
        ['drive.google.com', 0, 1, 8, 21],
        ['github.com', 1, 2, 3, 10],
        ['linkedin.com', 4, 18, 16, 45],
        ['yelp.com', 3, 1, 4, 112],
        ['netflix.com', 0, 3, 6, 78],
        ['us-east-2.console.aws.amazon.com', 0, 2, 1, 43],
        ['dropbox.com', 1, 2, 115, 4],
        ['att.com/my', 0, 0, 11, 2],
        ['tumblr.com', 0, 1, 80, 24],

    ]);

    var options = {
        title: "Requests + tf-idf",
        height: 1000,
        legend: { position: 'top', maxLines: 3 },
        bar: { groupWidth: '60%' },
        isStacked: true,
        bars: 'horizontal'
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div2'));
    chart.draw(data, options);
}

// function draw3() {
//     var data = google.visualization.arrayToDataTable([
//         ['Genre', 'Document', 'Image', 'Script', 'Fetch', 'XHR', 'Stylesheet'],
//         ['airbnb.com', 1,0,0,5,0,0],
//         ['bestbuy.com', 1,0,1,14,0,0],
//         ['facebook.com', 1,0,0,0,9,0],
//         ['gmail.com', 4,1,2,0,1,0],
//         ['newlook.dteenergy.com', 1,9,0,0,0,0],
//         ['amazon.com', 1,0,1,0,0,0],
//         ['drive.google.com', 1,0,2,0,10,0],
//         ['github.com', 1,1,0,1,0,0],
//         ['linkedin.com', 3,4,0,0,26,0],
//         ['yelp.com', 2,0,0,1,1,0],
//         ['netflix.com', 2,0,0,0,1,0],
//         ['us-east-2.console.aws.amazon.com', 2,0,0,0,0,0],
//         ['dropbox.com', 1,1,0,0,0,0],
//         ['att.com/my', 1,0,0,0,0,0],
//         ['mail.qq.com', 4,1,0,0,0,1]

//     ]);

//     var options = {
//         height: 1000,
//         legend: { position: 'top', maxLines: 3 },
//         bar: { groupWidth: '60%' },
//         isStacked: true,
//         bars: 'horizontal'
//     };
//     var chart = new google.visualization.BarChart(document.getElementById('chart_div3'));
//     chart.draw(data, options);
// }

function draw4() {
    var data = google.visualization.arrayToDataTable([
        ['Genre', 'Diff with login cookie', "Diff with unlogin cookie", 'Same between login/unlogin cookie', 'No Cookie header'],
        ['airbnb.com', 2.418, 12.569, 296.765, 3144.225],
        ['bestbuy.com', 0.0, 1.665, 71.013, 2803.522],
        ['facebook.com', 45.526, 2.803, 54.959, 4284.422],
        ['gmail.com', 4.191, 156.444, 1374.053, 235.372],
        ['newlook.dteenergy.com', 131.072, 0.992, 3467.439, 381.971],
        ['amazon.com', 3.537, 121.778, 199.051, 2892.602],
        ['drive.google.com', 0.0, 62.544, 780.739, 150.98],
        ['github.com', 0.969, 20.921, 27.931, 354.366],
        ['linkedin.com', 25.476, 73.842, 18.817, 2035.223],
        ['yelp.com', 0.711, 0.776, 58.99, 3451.927],
        ['netflix.com', 1.959, 75.612, 9.575, 3106.043],
        ['us-east-2.console.aws.amazon.com', 0.0, 54.058, 1.618, 827.858],
        ['dropbox.com', 11.704, 87.428, 1098.505, 372.181],
        ['att.com/my', 0.0, 0.0, 115.853, 3.453],
        ['tumblr.com', 0.0, 103.434, 11308.062, 4088.222]


    ]);

    var options = {
        title: "Requests + tf-idf (KBytes)",
        height: 1000,
        legend: { position: 'top', maxLines: 3 },
        bar: { groupWidth: '60%' },
        isStacked: true,
        bars: 'horizontal'
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div3'));
    chart.draw(data, options);
}


function draw(){
    draw0();
    draw1();
    draw2();
    draw4();
}