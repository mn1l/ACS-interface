fetch('/krijg-temperatuur-json')
  .then(response => response.json())
  .then(data => {
    var config = {
      data: data,
      xkey: 'y',
      ykeys: ['a', 'b'],
      labels: ['Luchttemperatuur', 'Gevoelstemperatuur'],
      fillOpacity: 0.6,
      hideHover: 'auto',
      behaveLikeLine: true,
      resize: true,
      parseTime: false,
      pointFillColors:['#ffffff'],
      pointStrokeColors: ['black'],
      lineColors:['blue','green']
    };
    config.element = 'line-chart';
    Morris.Line(config);
  });