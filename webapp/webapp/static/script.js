//App

// angularjs app
var printerApp = angular.module("printerApp", []);

// function to create the jobs service. Depends on $http service
function jobsService($http)
{
	// the object that will be the service
	var service = new Object();
	
	// Array that holds the job objects
	service.jobs = [];
	
	// Function that gets the jobs from the server
	service.getJobs = function() {
		// Do AJAX GET.
		$http.get("jobs.json").success(function(data) {
			// Returned JSON is an array of jobs. All we have to do is put the results in our jobs arrays
			service.jobs = data;
		});
	};
	
	service.getJobs();
	
	return service;
}

//register our service
printerApp.service("jobsService", ["$http", jobsService]);

function printersService($http)
{
	// the object that will be the service
	var service = new Object();
	
	// Array that holds the printer objects
	service.printers = [];
	
	// The chosen printer
	service.selectedPrinter = null;
	
	// Function that gets the printers from the server
	service.getPrinters = function() {
		// Do AJAX GET.
		$http.get("printers.json").success(function(data) {
			// Returned JSON is an array of printers. All we have to do is put the results in our arrays
			service.printers = data;
			
			//also choose a default printer
			service.selectedPrinter = service.printers[0];
		});
	};
	
	service.getPrinters();
	
	return service;
}

//register service
printerApp.service("printersService", ["$http", printersService]);

function userService($http)
{
	// the object that will be the service
	var service = new Object();
	
	// Array that holds the users objects
	service.user = {};
	
	// Function that gets the users from the server
	service.getUser = function() {
		// Do AJAX GET.
		$http.get("users.json").success(function(data) {
			// Returned JSON a user object
			service.user = data;
		});
	};
	
	service.getUser();
	
	return service;
}

//register service
printerApp.service("userService", ["$http", userService]);

// Function to create controller to display the jobs
// Depends on jobs service and scope service
function jobsController($scope, jobsService, printersService, userService)
{
	$scope.service = jobsService; //expose jobsService as "service" in the html
	$scope.printersService = printersService; // also need printers service
	$scope.userService = userService; // also also need users service
	$scope.getMonth = function(date) {
		date = date.replace(/-/g,"/");
		var d = new Date(date);
		var month = new Array();
		month[0] = "JAN";
		month[1] = "FEB";
		month[2] = "MAR";
		month[3] = "APR";
		month[4] = "MAY";
		month[5] = "JUN";
		month[6] = "JUL";
		month[7] = "AUG";
		month[8] = "SEP";
		month[9] = "OCT";
		month[10] = "NOV";
		month[11] = "DEC";
		var n = month[d.getMonth()];
		return n;
	};
	$scope.getDay = function(date) {
		date = date.replace(/-/g,"/");
		var d = new Date(date);
		var day = d.getDate();
		return day;
	};
	$scope.getTime = function(date) {
		date = date.replace(/-/g,"/");
		var d = new Date(date);
		var h = d.getHours();
		var m = d.getMinutes();
		var s = d.getSeconds();
		h = h % 12;
		h = h ? h : 12; // the hour '0' should be '12'
		var ampm = h >= 12 ? 'PM' : 'AM';
		m = m < 10 ? '0'+m : m;
		s = s <10 ? '0'+s: s;
		// add a zero in front of numbers<10

		return h+':'+m+':'+s+' '+ampm;
	};
	
	$scope.getPrice = function(job) {
		var printer = $scope.printersService.selectedPrinter;
		if (!printer)
			return 0;
		var price = job.pages * printer.costPerPage + job.percentC * printer.costC + job.percentY * printer.costY + job.percentM * printer.costM + job.percentK * printer.costK;
		return price.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
	};
	
	$scope.getBalance = function() {
		if ($scope.userService.user.balance == null)
			return 0;
		return $scope.userService.user.balance.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
	};
}

/* function printersController($scope, jobsService, printersService, userService)
{
	$scope.service = jobsService; //expose jobsService as "service" in the html
	$scope.printersService = printersService; // also need printers service
	$scope.userService = userService; // also also need users service
} */

// register controller
printerApp.controller("jobsController", ["$scope", "jobsService", "printersService", "userService", jobsController]);

$(window).load(function() {
	$('.jobtitle').textfill({ maxFontPixels: 22 });
});
