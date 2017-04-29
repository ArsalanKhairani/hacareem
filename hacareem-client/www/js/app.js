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
  .controller('mapController', function($scope, $http, $ionicLoading) {

    var marker = {};
    $scope.longitude = 0;
    $scope.latitude = 0;
    $scope.phoneNumber = '';
    $scope.carType = '';
    $scope.pickUp = '';
    $scope.dropOff = '';
    $scope.promoCode = '';
    $scope.isSMSSend = false;
    $scope.isRideValid = false;
    $scope.locations = [];
    $scope.fairEstimate = '-';

    var loadingTemplate = '<ion-spinner icon="ios"></ion-spinner>';

    var urlMap = {
      GEN_AUTH_TOKEN: '',
      BOOK_RIDE: '',
      ETA: '',
      ETA_PRICE: '',
      LOCATIONS: ''
    };


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

    function showLoading() {
      $ionicLoading.show({template: loadingTemplate});
    }

    function hideLoading() {
      $ionicLoading.hide();
    }

    function addMarker(latlng, title, map) {
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
      $http.get('/api/v1/getEta')
        .success(function (data, status, headers, config) {

        }, function errorCallback() {
          hideLoading();
        });
    }

    function getBookings() {

    }

    function createRide() {
      var params = {
        longitude: $scope.longitude,
        latitude: $scope.latitude,
        promo_code: $scope.promo_code
      };

      $http.post('/api/v1/book_ride', params).then(function (response) {
          if (response && response.ok) {
            clearAllFields();
            hideLoading();
          }
      }, function errorCallback() {
        hideLoading();
      });
    }

    function clearAllFields() {
      angular.forEach($scope.params, function (val, key) {
          $scope.params[key] = '';
      });
    }

    $scope.verifyNumber = function (number) {
      showLoading();

      $scope.isSMSSend = !$scope.isSMSSend;
      $http.post(urlMap.GEN_AUTH_TOKEN, {number: number})
        .success(function(data, status, headers, config) {
          if (data && data.success) {
            $scope.isRideValid = true;
            createRide();
          }
        })
        .error(function errorCallback() {
          hideLoading();
        });
    };

    $scope.searchLocation = function (query) {
      $http.get(urlMap.LOCATIONS).then(function (response) {
        if (response && response.ok) {
          $scope.locations = response.locations;
        }
      }, function errorCallback() {
        hideLoading();
      });
    };

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


