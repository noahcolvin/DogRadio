'use strict';

var app = angular.module('radioControllers', []);

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