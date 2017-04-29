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
    var map = {};
    $scope.longitude = 67.00994;
    $scope.latitude = 24.86146;
    $scope.phoneNumber = '';
    $scope.carType = '';
    $scope.pickUp = '';
    $scope.dropOff = '';
    $scope.promoCode = '';
    $scope.isSMSSend = false;
    $scope.isRideValid = false;
    $scope.locations = [{title: 'Wajih'}, {title: 'Arsalan'}];
    $scope.carTypes = [];
    $scope.fairEstimate = '-';

    $scope.etaInfo = {};
    $scope.etaText = 'Wajih';

    var loadingTemplate = '<ion-spinner icon="ios"></ion-spinner>';

    var baseURL = 'https://ck4s04794j.execute-api.us-east-1.amazonaws.com/prod/';

    var urlMap = {
      GEN_AUTH_TOKEN: baseURL + 'generate_auth_token/',
      BOOK_RIDE: baseURL + '',
      ETA: baseURL + 'get_eta_time/',
      ETA_PRICE: '',
      LOCATIONS: baseURL + 'getLocations/',
      GET_PRODUCTS: baseURL + 'get_products/'
    };


    $scope.initMap = function() {
      var mylocation = {lat: 24.86146, lng: 67.00994};

      map = new google.maps.Map(document.getElementById("googleMap"), {
        center: mylocation,
        zoom: 17
      });

      addMarker(mylocation, $scope.etaText, map);

      getProducts(mylocation);

      // marker = new google.maps.Marker({
      //   position: mylocation,
      //   map: map,
      //   title: 'Hello World!'
      // });

      // navigator.geolocation.getCurrentPosition(function(position) {
      //   console.log(position);
      // });

    };

    function getProducts(location) {
      $http.get(urlMap.GET_PRODUCTS, {params: location})
        .success(function (data, status, headers, config) {
          if (data && data.products) {
            angular.forEach(data.products, function (val, key) {
              if (val.availibility_now) {
                $scope.carTypes.push({title: val.display_name, product_id: val.product_id});
              }
            });
          }
          hideLoading();
        }, function errorCallback() {
          hideLoading();
        });
    }

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
        getETA();
      }
    }

    function getETAObject() {
      return {
        lat: $scope.latitude,
        long: $scope.longitude,
        p_id: $scope.carType.product_id
      };
    }

    function getETA(carType) {
      $http.get(urlMap.ETA, {params: getETAObject()})
        .success(function (data) {
          if (data && data.times) {
            angular.forEach(data.times, function (val, key) {
              $scope.etaInfo[val.display_name] = (val.eta / 60);
            });

            if (carType) {
              $scope.etaText = $scope.etaInfo[carType.title];
              addMarker({lng: $scope.longitude, lat: $scope.latitude}, 'ETA for '+carType.title+' is : ' + $scope.etaText.toFixed(2) + 'seconds', map);
            }

            hideLoading();
          }
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

      $http.post(urlMap.BOOK_RIDE, params).then(function (response) {
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
          if (data && data.message && data.message.enc_auth_token) {
            $scope.isRideValid = true;
            $scope.verificationCode = data.enc_auth_token;
            hideLoading();
          }
        })
        .error(function errorCallback(response) {
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

    $scope.setPickupLocation = function (loc) {
      $scope.pickUp = loc;
      getEta();
    };

    $scope.setDropoffLocation = function (loc) {
      $scope.dropOff = loc;
      getEta();
    };

    $scope.setCarType = function (carType) {
      $scope.carType = carType;
      getETA(carType);
    };

    $scope.initMap();
    showLoading();

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


