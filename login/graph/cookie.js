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
        ['airbnb.com', 3, 8, 29, 32],
        ['bestbuy.com', 0, 1, 8, 108],
        ['facebook.com', 2, 6, 6, 209],
        ['gmail.com', 4, 7, 38, 106],
        ['newlook.dteenergy.com', 9, 4, 55, 37],
        ['amazon.com', 1, 0, 0, 96],
        ['drive.google.com', 9, 0, 24, 57],
        ['github.com', 2, 1, 3, 10],
        ['linkedin.com', 2, 12, 15, 39],
        ['yelp.com', 4, 1, 4, 45],
        ['netflix.com', 2, 3, 5, 32],
        ['us-east-2.console.aws.amazon.com', 0, 2, 1, 42],
        ['dropbox.com', 3, 1, 114, 5],
        ['att.com/my', 1, 0, 10, 2]

    ]);

    var options = {
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
        ['airbnb.com', 0, 8, 32, 32],
        ['bestbuy.com', 0, 2, 13, 120],
        ['facebook.com', 2, 13, 2, 196],
        ['gmail.com', 3, 5, 34, 101],
        ['newlook.dteenergy.com', 8, 2, 56, 35],
        ['amazon.com', 4, 1, 37, 242],
        ['drive.google.com', 10, 2, 34, 63],
        ['github.com', 1, 2, 3, 10],
        ['linkedin.com', 7, 17, 48, 73],
        ['yelp.com', 1, 1, 8, 96],
        ['netflix.com', 0, 3, 6, 15],
        ['us-east-2.console.aws.amazon.com', 0, 3, 2, 42],
        ['dropbox.com', 3, 2, 113, 5],
        ['att.com/my', 0, 0, 11, 2]

    ]);

    var options = {
        height: 1000,
        legend: { position: 'top', maxLines: 3 },
        bar: { groupWidth: '60%' },
        isStacked: true,
        bars: 'horizontal'
    };
    var chart = new google.visualization.BarChart(document.getElementById('chart_div2'));
    chart.draw(data, options);
}

function draw3() {
    var data = google.visualization.arrayToDataTable([
        ['Genre', 'Document', 'Image', 'Script', 'Fetch', 'XHR', 'Stylesheet'],
        ['airbnb.com', 1,0,0,5,0,0],
        ['bestbuy.com', 1,0,1,14,0,0],
        ['facebook.com', 1,0,0,0,9,0],
        ['gmail.com', 4,1,2,0,1,0],
        ['newlook.dteenergy.com', 1,9,0,0,0,0],
        ['amazon.com', 1,0,1,0,0,0],
        ['drive.google.com', 1,0,2,0,10,0],
        ['github.com', 1,1,0,1,0,0],
        ['linkedin.com', 3,4,0,0,26,0],
        ['yelp.com', 2,0,0,1,1,0],
        ['netflix.com', 2,0,0,0,1,0],
        ['us-east-2.console.aws.amazon.com', 2,0,0,0,0,0],
        ['dropbox.com', 1,1,0,0,0,0],
        ['att.com/my', 1,0,0,0,0,0],
        ['mail.qq.com', 4,1,0,0,0,1]

    ]);

    var options = {
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
    draw3();
}