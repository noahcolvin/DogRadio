'use strict';

var app = angular.module('radioApp', ['ngResource', 'ui.bootstrap']);

app.controller('radioController', ['$scope', 'Controls', 'Playlist', '$interval',
    function($scope, Controls, Playlist, $interval) {
        $scope.volumeLevel = 0;

        $scope.sendCommand = function(command) {
            Controls.run(command)
                .then(function(data) {
                    updateStatus();
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });
        }

        $scope.setRelativeVolume = function(offset) {
            Controls.setVolume(offset)
                .then(function(data) {
                    var d = data.data;
                    $scope.volumeLevel = d.volume;
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });
        }

        $scope.playlistPlay = function(index) {
            Playlist.play(index)
                .then(function(data) {
                    updateStatus();
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });
        }

        $scope.playlistDelete = function(index) {
            var playlistUrl = $scope.playlist[index];

            Playlist.delete(playlistUrl)
                .then(function(data) {
                    updateStatus();
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });
        }

        $scope.playlistAdd = function(station) {
            Playlist.addStation(station)
                .then(function(data) {
                    updateStatus();
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });
        }

        function updateStatus() {
            $scope.errorMessage = undefined;

            Controls.getStatus()
                .then(function(data) {
                    var d = data.data;
                    $scope.volumeLevel = d.volume;
                    $scope.playMode = d.playMode;
                    $scope.title = d.title;
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });

            loadPlaylist();
        }

        function loadPlaylist() {
            Playlist.getPlaylist()
                .then(function(data) {
                    var d = data.data;
                    $scope.playlist = d;
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });
        }

        $interval(updateStatus, 60000); // 1 minute

        updateStatus();
    }]);

app.factory('Playlist', ['$http', '$q',
    function($http, $q) {
        function play(index) {
            var deferred = $q.defer();

            $http.post('http://192.168.1.239:5000/control/play/' + (parseInt(index) + 1))
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        function deleteStation(url) {
            var deferred = $q.defer();

            $http.delete('http://192.168.1.239:5000/playlist', { data: { 'url': url }, headers: { 'Content-Type': 'application/json' } })
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        function addStation(url) {
            var deferred = $q.defer();

            $http.post('http://192.168.1.239:5000/playlist', { 'url': url }, { headers: { 'Content-Type': 'application/json' } })
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        function getPlaylist() {
            var deferred = $q.defer();

            $http.get('http://192.168.1.239:5000/playlist')
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        return {
            play: play,
            delete: deleteStation,
            addStation: addStation,
            getPlaylist: getPlaylist
        };
    }]);



app.factory('Controls', ['$http', '$q',
    function($http, $q) {
        function runCommand(command) {
            var deferred = $q.defer();

            $http.post('http://192.168.1.239:5000/control/' + command)
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        function setVolume(value) {
            var deferred = $q.defer();

            $http.put('http://192.168.1.239:5000/volume/' + value)
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        function getStatus(command) {
            var deferred = $q.defer();

            $http.get('http://192.168.1.239:5000/status')
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        function getPlaylist() {
            var deferred = $q.defer();

            $http.get('http://192.168.1.239:5000/playlist')
                .then(function(data) {
                    deferred.resolve(data);
                },
                function(err) {
                    deferred.reject(err);
                });

            return deferred.promise;
        }

        return {
            run: runCommand,
            setVolume: setVolume,
            getStatus: getStatus,
            getPlaylist: getPlaylist
        };
    }]);

