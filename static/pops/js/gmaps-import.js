$(function () {
	var $map = $('#map-canvas');
	var icons = $map.data('media') + '/icons/';

	var gmapIcons = new Object();
	gmapIcons = {
		routersIcon : new google.maps.MarkerImage(
				icons + "routers.png", //image
			new google.maps.Size(30, 25), //size
			new google.maps.Point(15, 13), //origin point
			new google.maps.Point(20, -50) //anchor point
		),
		 routerIcon : new google.maps.MarkerImage(
			icons + "router.png",
			new google.maps.Size(30, 25),
			new google.maps.Point(0, 0),
			new google.maps.Point(15, 13)
		),
		 switchIcon : new google.maps.MarkerImage(
			icons + "switch.png",
			new google.maps.Size(30, 25),
			new google.maps.Point(0, 0),
			new google.maps.Point(15, 13)
		),
		 switchesIcon : new google.maps.MarkerImage(
			icons + "switches.png",
			new google.maps.Size(30, 24),
			new google.maps.Point(15, 12),
			new google.maps.Point(20, -50)
		),
		 termIcon : new google.maps.MarkerImage(
			icons + "ts.png",
			new google.maps.Size(40, 50),
			new google.maps.Point(20, 50),
			new google.maps.Point(20, -50)
		),
		 powerIcon : new google.maps.MarkerImage(
			icons + "power.png",
			new google.maps.Size(40, 50),
			new google.maps.Point(20, 50),
			new google.maps.Point(20, -50)
		),
		 adddropIcon : new google.maps.MarkerImage(
			icons + "add-droppin.png",
			new google.maps.Size (40, 60),
			new google.maps.Point (20, 60),
			new google.maps.Point (20, -50)
		),
		 regenIcon : new google.maps.MarkerImage(
			icons + "regenpin.png",
			new google.maps.Size (40, 60),
			new google.maps.Point (20, 60),
			new google.maps.Point (20, -50)
		),
		 lineampIcon : new google.maps.MarkerImage(
			icons + "lineamppin.png",
			new google.maps.Size (40, 60),
			new google.maps.Point (20, 60),
			new google.maps.Point (20, -50)
		),
		 infoIcon : new google.maps.MarkerImage(
			icons + "info3.png",
			new google.maps.Size (12, 12),
			new google.maps.Point (6, 6),
			new google.maps.Point (8, 0)
		),
		 redpinIcon : new google.maps.MarkerImage(
			icons + "optpin.png",
			new google.maps.Size (16, 19),
			new google.maps.Point (8, 19),
			new google.maps.Point (8, 0)
		),
		 redIcon : new google.maps.MarkerImage(
			icons + "cluster2.png",
			new google.maps.Size (34, 34),
			new google.maps.Point (17, 17),
			new google.maps.Point (8, 0)
		),
		cityIcon : new google.maps.MarkerImage(
			icons + "city.png",
			new google.maps.Size (32, 32),
			new google.maps.Point (0, 0),
			new google.maps.Point (16, 16)
		),
		 purpleIcon : new google.maps.MarkerImage(
			icons + "purple.png",
			new google.maps.Size (19, 21),
			new google.maps.Point (4, 21),
			new google.maps.Point (8, 0)
		),
		 grnetlocIcon : new google.maps.MarkerImage(
			icons + "grnet_loc.png",
			new google.maps.Size (32, 37),
			new google.maps.Point (16, 37),
			new google.maps.Point (8, 0)
		),
		 otelocIcon : new google.maps.MarkerImage(
			icons + "ote_loc.png",
			new google.maps.Size (32, 37),
			new google.maps.Point (16, 37),
			new google.maps.Point (8, 0)
		),
		 unilocIcon : new google.maps.MarkerImage(
			icons + "uni_loc.png",
			new google.maps.Size (32, 37),
			new google.maps.Point (16, 37),
			new google.maps.Point (8, 0)
		),
		 otherlocIcon : new google.maps.MarkerImage(
			icons + "other_loc.png",
			new google.maps.Size (32, 37),
			new google.maps.Point (16, 37),
			new google.maps.Point (8, 0)
		),
		 infodotIcon : new google.maps.MarkerImage(
			icons + "infodot.png",
			new google.maps.Size (26, 26),
			new google.maps.Point (13, 13),
			new google.maps.Point (8, 0)
		),
		 grnetcoverIcon : new google.maps.MarkerImage(
			icons + "GRNETLOGO.png",
			new google.maps.Size (50, 45),
			new google.maps.Point (25, 22),
			new google.maps.Point (8, 0)
		),
		 bluebulIcon : new google.maps.MarkerImage(
			icons + "blue_bul.png",
			new google.maps.Size (20, 20),
			new google.maps.Point (10, 10)
		),
		 redbulIcon : new google.maps.MarkerImage(
			icons + "red_bul.png",
			new google.maps.Size (12, 12),
			new google.maps.Point (6, 6)
		)
	};

	var styleArray = [
	    {
	        "featureType": "water",
	        "elementType": "all",
	        "stylers": [
	            {
	                "visibility": "simplified"
	            },
	            {
	                "hue": "#e9ebed"
	            },
	            {
	                "saturation": -78
	            },
	            {
	                "lightness": 67
	            }
	        ]
	    },
	    {
	        "featureType": "landscape",
	        "elementType": "all",
	        "stylers": [
	            {
	                "visibility": "simplified"
	            },
	            {
	                "hue": "#ffffff"
	            },
	            {
	                "saturation": -100
	            },
	            {
	                "lightness": 100
	            }
	        ]
	    },
	    {
	        "featureType": "road",
	        "elementType": "geometry",
	        "stylers": [
	            {
	                "visibility": "simplified"
	            },
	            {
	                "hue": "#bbc0c4"
	            },
	            {
	                "saturation": -93
	            },
	            {
	                "lightness": 31
	            }
	        ]
	    },
	    {
	        "featureType": "poi",
	        "elementType": "all",
	        "stylers": [
	            {
	                "visibility": "off"
	            },
	            {
	                "hue": "#ffffff"
	            },
	            {
	                "saturation": -100
	            },
	            {
	                "lightness": 100
	            }
	        ]
	    },
	    {
	        "featureType": "road.local",
	        "elementType": "geometry",
	        "stylers": [
	            {
	                "visibility": "simplified"
	            },
	            {
	                "hue": "#e9ebed"
	            },
	            {
	                "saturation": -90
	            },
	            {
	                "lightness": -8
	            }
	        ]
	    },
	    {
	        "featureType": "transit",
	        "elementType": "all",
	        "stylers": [
	            {
	                "visibility": "on"
	            },
	            {
	                "hue": "#e9ebed"
	            },
	            {
	                "saturation": 10
	            },
	            {
	                "lightness": 69
	            }
	        ]
	    },
	    {
	        "featureType": "administrative.locality",
	        "elementType": "all",
	        "stylers": [
	            {
	                "visibility": "on"
	            },
	            {
	                "hue": "#2c2e33"
	            },
	            {
	                "saturation": 7
	            },
	            {
	                "lightness": 19
	            }
	        ]
	    },
	    {
	        "featureType": "road",
	        "elementType": "labels",
	        "stylers": [
	            {
	                "visibility": "on"
	            },
	            {
	                "hue": "#bbc0c4"
	            },
	            {
	                "saturation": -93
	            },
	            {
	                "lightness": 31
	            }
	        ]
	    },
	    {
	        "featureType": "road.arterial",
	        "elementType": "labels",
	        "stylers": [
	            {
	                "visibility": "simplified"
	            },
	            {
	                "hue": "#bbc0c4"
	            },
	            {
	                "saturation": -93
	            },
	            {
	                "lightness": -2
	            }
	        ]
	    }
	]
});
