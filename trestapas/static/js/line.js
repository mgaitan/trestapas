var dataSet = [
	['date', '20130101', '20130102', '20130103', '20130104','20130105', '20130106', '20130107', '20130108'],
	['clarin', 30, 200, 100, 400, 30, 200, 100, 400],
	['la nacion', 50, 20, 10, 40,50, 20, 10, 40],
	['ambito', 70, 10, 40, 70,70, 10, 40, 70]
]

c3.generate({
		bindto: '#chart',
    data: {
				x : 'date',
        x_format : '%Y%m%d',
        columns: dataSet 
    },
		axis: {
    	x: {
      	type: 'timeseries', // x axis will be shown as timeseries
				tick : {
					format : "%e %b %y" // https://github.com/mbostock/d3/wiki/Time-Formatting#wiki-format
        }
    	}
  	}
});