/**
 * Created by paulguichon on 29/07/2015.
 */

var statControlers = angular.module('statControlers', []);

statControlers.controller('StatListCtrl', ['$scope',  'Stat', '$modal',
    function ($scope,  Stat, $modal) {


            $scope.etapes = Stat.query();




    }]);

