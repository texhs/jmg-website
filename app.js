//angular.module('myApp', ['ui.bootstrap']);
var app = angular.module('plunker', ['ui.bootstrap']);

// Controller  for Carousel
function CarouselCtrl($scope) {

// initializing the time Interval
  $scope.myInterval = 5000;

 // Initializing  slide rray
$scope.slides = [
{image:'http://www.wetwebmedia.com/fwsubwebindex/Cyprinodontiform%20PIX/Platy%20PIX/Xiphophorus%20maculatusAQ%20Neon%20female.jpg',text:'Cute Fish'},
{image:'http://www.wetwebmedia.com/fwsubwebindex/Cyprinodontiform%20PIX/Platy%20PIX/Xiphophorus%20maculatusAQ%20Neon%20female.jpg',text:'Image2'},
{image:'http://www.wetwebmedia.com/fwsubwebindex/Cyprinodontiform%20PIX/Swordtail%20PIX/Xiphophorus%20helleriAQ%20Hifin%20Black%20males.jpg',text:'Image3'},
{image:'http://www.wetwebmedia.com/fwsubwebindex/Cyprinodontiform%20PIX/Platy%20PIX/Xiphophorus%20maculatusAQ%20Neon%20female.jpg',text:'Image4'}
                      ];

  var slides = $scope.slides;
  console.log(slides);

} // Controller Ends here
