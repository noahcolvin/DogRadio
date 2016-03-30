'use strict';

var app = angular.module('radioApp', ['ngResource', 'ui.bootstrap']);

app.controller('radioController', ['$scope', 'Controls', '$interval', function($scope, Controls, $interval) {
    $scope.sendCommand = function(command) {
        Controls.run(command)
            .then(function(data) {
                updateStatus();
            });;
    }

    $scope.setRelativeVolume = function(offset) {
        Controls.setVolume(offset)
            .then(function(data) {
                $scope.volumeLevel = data.volume;
            });
    }

    function updateStatus() {
        Controls.getStatus()
            .then(function(data) {
                $scope.volumeLevel = data.volume;
                $scope.playMode = data.playMode;
                $scope.title = data.title;
            });
    }
    
    $interval(updateStatus, 60000); // 1 minute

    updateStatus();
}]);

app.factory('Controls', ['$http', '$q', function($http, $q) {
    function runCommand(command) {
        var deferred = $q.defer();

        $http.post('http://192.168.1.239:5000/control/' + command)
            .success(function(data) {
                deferred.resolve(data);
            });

        return deferred.promise;
    }

    function setVolume(value) {
        var deferred = $q.defer();

        $http.put('http://192.168.1.239:5000/volume/' + value)
            .success(function(data) {
                deferred.resolve(data);
            });

        return deferred.promise;
    }

    function getStatus(command) {
        var deferred = $q.defer();

        $http.get('http://192.168.1.239:5000/status')
            .success(function(data) {
                deferred.resolve(data);
            });

        return deferred.promise;
    }

    return {
        run: runCommand,
        setVolume: setVolume,
        getStatus: getStatus
    };
}]);

