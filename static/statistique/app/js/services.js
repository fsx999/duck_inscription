/**
 * Created by paulguichon on 29/07/2015.
 */
var statServices = angular.module('statServices', ['ngResource']);

statServices.factory('Stat', ['$resource',
    function ($resource) {

        return $resource('/api/v1/statistique_inscription/:etapeId', {}, {
            query: {method: 'GET', params: {etapeId: '@etapeId'}, isArray: true}

        });
    }]);
