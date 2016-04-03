'use strict';

var app = angular.module('radioServices', []);

app.factory('Playlist', ['$http', '$q',
    function($http, $q) {
        function play(index) {
            var deferred = $q.defer();

            $http.post('/control/play/' + (parseInt(index) + 1))
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

            $http.delete('/playlist', { data: { 'url': url }, headers: { 'Content-Type': 'application/json' } })
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

            $http.post('/playlist', { 'url': url }, { headers: { 'Content-Type': 'application/json' } })
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

            $http.get('/playlist')
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

            $http.post('control/' + command)
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

            $http.put('volume/' + value)
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

            $http.get('status')
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

            $http.get('playlist')
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