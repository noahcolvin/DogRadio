'use strict';

var app = angular.module('radioControllers', []);

app.controller('radioController', ['$scope', 'Controls', 'Playlist', '$interval', 'uibButtonConfig', 'Power',
    function($scope, Controls, Playlist, $interval, uibButtonConfig, Power) {
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
            loadPowerStates();
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

        function loadPowerStates(){
            Power.getState(0)
                .then(function(data) {
                    var d = data.data;
                    switch(d){
                        case true:
                            $scope.speakerToggle = 'On';
                            break;
                        case false:
                            $scope.speakerToggle = 'Off';
                            break;
                    }
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });

            Power.getState(1)
                .then(function(data) {
                    var d = data.data;
                    switch(d){
                        case true:
                            $scope.lightToggle = 'On';
                            break;
                        case false:
                            $scope.lightToggle = 'Off';
                            break;
                    }
                })
                .catch(function(error) {
                    $scope.errorMessage = 'Error: ' + error.data;
                });
        }

        $scope.lightToggle = 'Auto';

        $scope.$watchCollection('lightToggle', function() {
            switch($scope.lightToggle){
                case 'On':
                    Power.setState(1, 'on');
                    break;
                case 'Off':
                    Power.setState(1, 'off');                
                    break;
                case 'Auto':
                    break;
            }
        });

        $scope.speakerToggle = 'Auto';

        $scope.$watchCollection('speakerToggle', function() {
            switch($scope.speakerToggle){
                case 'On':
                    Power.setState(0, 'on');
                    break;
                case 'Off':
                    Power.setState(0, 'off');                
                    break;
                case 'Auto':
                    break;
            }
        });

        uibButtonConfig.activeClass = 'btn-primary';

        $interval(updateStatus, 60000); // 1 minute

        updateStatus();
    }]);