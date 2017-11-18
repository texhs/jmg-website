(function () {
    var app = angular.module('yt', []);

    app.controller('YTController', ['$http', function ($http) {
        this.videos = [];
        /*this.video1;
        this.video2;
        this.video3;
        this.video4;
        this.video5;*/
        this.playlists = [];
        var yt = this;
        yt.videos = [];
        $http.get('https://tg22k03n1m.execute-api.sa-east-1.amazonaws.com/WebsiteJMG').success(function(data) {
            yt.videos = data;

            /*var sortedData = data.sort(function(obj1, obj2) {
                    console.log(obj1.lastName);
                    return obj1.lastName - obj2.lastName;
                })*/

            /*yt.video1 = data.video1;
            yt.video2 = data.video2;
            yt.video3 = data.video3;
            yt.video4 = data.video4;
            yt.video5 = data.video5;*/
        });
    }]);

    app.controller('PanelController', function () {
        this.tab = 1;

        this.selectTab = function(setTab) {
            this.tab = setTab;
        }

        this.isSelected = function(checkTab) {
            return this.tab === checkTab;
        }
    });

})();
