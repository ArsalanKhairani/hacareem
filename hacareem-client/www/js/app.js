// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
angular.module('starter', ['ionic'])

.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})
  .controller('mapController', function($scope) {

    var marker = {};
    $scope.longitude = 0;
    $scope.latitude = 0;

    $scope.initMap = function() {
      var mylocation = {lat: 24.86146, lng: 67.00994};
      var map = new google.maps.Map(document.getElementById("googleMap"), {
        center: mylocation,
        zoom: 17
      });

      addMarker(mylocation, 'Hello World', map);

      // marker = new google.maps.Marker({
      //   position: mylocation,
      //   map: map,
      //   title: 'Hello World!'
      // });

      // navigator.geolocation.getCurrentPosition(function(position) {
      //   console.log(position);
      // });

    };

    function addMarker(latlng,title,map) {
      var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        title: title,
        draggable:true
      });

      marker.addListener('drag', handleEvent);
      marker.addListener('dragend', handleEvent);
    }

    function handleEvent(pos) {
      if (pos) {
        $scope.longitude = pos.latLng.lng();
        $scope.latitude = pos.latLng.lat();
        callETA();
      }
    }

    function callETA() {

    }

    $scope.initMap();



    // function initGeolocation() {
    //   if(navigator.geolocation) {
    //     // Call getCurrentPosition with success and failure callbacks
    //     navigator.geolocation.getCurrentPosition(success, fail);
    //   }
    // }
    //
    // function success(position) {
    //   document.getElementById('long').value = position.coords.longitude;
    //   document.getElementById('lat').value = position.coords.latitude;
    // }
    // function fail() {}

  });


