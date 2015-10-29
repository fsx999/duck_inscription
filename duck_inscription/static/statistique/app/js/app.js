/**
 * Created by paulguichon on 29/07/2015.
 */
var statistiqueApp = angular.module('statistiqueApp', [
    'ngRoute',
    'statControlers',
    'statServices',
    'ui.bootstrap'
]);

statistiqueApp.config(['$routeProvider', '$httpProvider',
    function ($routeProvider, $httpProvider) {
        $routeProvider.
            when('/piel', {
                templateUrl: '/static/statistique/app/partials/statistiques.html',
                controller: 'StatListCtrl'
            }).
            //when('/personnels/:personelId', {
            //    templateUrl: '/static/personnel/app/partials/personne-detail.html',
            //    controller: 'PersonneCtrl'
            //}).
            otherwise({
                redirectTo: '/piel'
            });
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    }]);
