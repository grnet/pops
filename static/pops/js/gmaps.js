$(function () {
    var $map = $('#map-canvas');
    var $menu = $('.menu');
    var $popup  = $('.locations-details .box');
    var $filter = $('.location-index form');
    var $body = $('body');
    var tag = '';
    var pinDescriptionHeaderTemplate = _.template($popup.data('template-header'));
    var pinDescriptionTemplate = _.template($popup.data('template'));
    var active_links = [];
    var remote_locations = [];
    var markers = [];



    if ($map.length > 0 ) {
        var icons = $map.data('media') + '/icons/maps/';
        var mapOptions = {};
        var globalUrl = $map.data('view');
        var initialUrl = $map.data('initial');


        var gmapIcons = new Object();
        gmapIcons = {
            'grnet-access-l2': new google.maps.MarkerImage(
                icons + 'grnet-access-l2.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)
            ),
            'grnet-access-optical': new google.maps.MarkerImage(
                icons + 'grnet-access-optical.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'grnet-core': new google.maps.MarkerImage(
                icons + 'grnet-core.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'grnet-distribution': new google.maps.MarkerImage(
                icons + 'grnet-distribution.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (16, 50),
                new google.maps.Point (68, 50)

            ),
            'pass-through': new google.maps.MarkerImage(
                icons + 'pass-through.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-core': new google.maps.MarkerImage(
                icons + 'commercial-core.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-distribution': new google.maps.MarkerImage(
                icons + 'commercial-distribution.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'pass-through': new google.maps.MarkerImage(
                icons + 'pass-through.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-access-l2': new google.maps.MarkerImage(
                icons + 'commercial-access-l2.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-access-optical': new google.maps.MarkerImage(
                icons + 'commercial-access-optical.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-access-l2': new google.maps.MarkerImage(
                icons + 'customer-access-l2.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-access-optical': new google.maps.MarkerImage(
                icons + 'customer-access-optical.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer2': new google.maps.MarkerImage(
                icons + 'customer2.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-core': new google.maps.MarkerImage(
                icons + 'customer-core.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-distribution': new google.maps.MarkerImage(
                icons + 'customer-distribution.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'pass-through': new google.maps.MarkerImage(
                icons + 'pass-through.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'unknown': new google.maps.MarkerImage(
                icons + 'unknown.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'grnet-access-l2-thumb': new google.maps.MarkerImage(
                icons + 'grnet-access-l2-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)
            ),
            'grnet-access-optical-thumb': new google.maps.MarkerImage(
                icons + 'grnet-access-optical-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'grnet-core-thumb': new google.maps.MarkerImage(
                icons + 'grnet-core-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'grnet-distribution-thumb': new google.maps.MarkerImage(
                icons + 'grnet-distribution-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (16, 50),
                new google.maps.Point (68, 50)

            ),
            'pass-through-thumb': new google.maps.MarkerImage(
                icons + 'pass-through-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-core-thumb': new google.maps.MarkerImage(
                icons + 'commercial-core-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-distribution-thumb': new google.maps.MarkerImage(
                icons + 'commercial-distribution-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'pass-through-thumb': new google.maps.MarkerImage(
                icons + 'pass-through-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-access-l2-thumb': new google.maps.MarkerImage(
                icons + 'commercial-access-l2-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'commercial-access-optical-thumb': new google.maps.MarkerImage(
                icons + 'commercial-access-optical-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-access-l2-thumb': new google.maps.MarkerImage(
                icons + 'customer-access-l2-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-access-optical-thumb': new google.maps.MarkerImage(
                icons + 'customer-access-optical-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer2-thumb': new google.maps.MarkerImage(
                icons + 'customer2-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-core-thumb': new google.maps.MarkerImage(
                icons + 'customer-core-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'customer-distribution-thumb': new google.maps.MarkerImage(
                icons + 'customer-distribution-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'pass-through-thumb': new google.maps.MarkerImage(
                icons + 'pass-through-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            ),
            'unknown-thumb': new google.maps.MarkerImage(
                icons + 'unknown-thumb.png',
                new google.maps.Size (50, 68),
                new google.maps.Point (68, 50),
                new google.maps.Point (68, 50)

            )
        };


        var infowindow = new google.maps.InfoWindow({
            content: ""
        });

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


        var route = [
            new google.maps.LatLng(39.5044, 20.2653),
            new google.maps.LatLng(36.4293, 28.2263)
        ];


        function createMarkerLite(location) {
            var exists = false;
            for (var marker=0; marker < markers.length; marker++) {
                if (parseFloat(Number(markers[marker].getPosition().lat()).toFixed(4)) === location.lat && parseFloat(Number(markers[marker].getPosition().lng()).toFixed(4)) == location.lng) {
                    exists = true;
                }
            }
            if (!exists) {
                var marker = new google.maps.Marker({
                    position: new google.maps.LatLng(location.lat, location.lng),
                    map: map,
                    title: location.name,
                    short_description: location.name,
                    icon: gmapIcons[location.image + '-thumb'].url,
                    details: location.details_url,
                    short_description: pinDescriptionHeaderTemplate({'pin': location})
                });
                addInfoToMarker(map, marker);
                remote_locations.push(marker);
                google.maps.event.addListener(marker, 'click', function() {
                    load_location(marker.details, marker.short_description)
                });
            }
        }

        function load_location(url, description) {
            $body.addClass('loading');
            $.getJSON(url, function(data) {
                pin = data;
                description = description + pinDescriptionTemplate({'pin': pin});
                var path;
                var pin_paths = [];
                var pin_dotted_paths = [];
                for (var link=0; link < active_links.length; link++) {
                    active_links[link].setMap(null);
                }
                for (var link=0; link < remote_locations.length; link++) {
                    remote_locations[link].setMap(null);
                }

                for (var member=0; member < pin.members_in_this_location.length; member++) {
                    for (var through=0; through < pin.members_in_this_location[member].through.length; through++) {
                        dotted_path = [];
                        dotted_path.push(new google.maps.LatLng(pin.members_in_this_location[member].through[through].lat, pin.members_in_this_location[member].through[through].lng));
                        dotted_path.push(new google.maps.LatLng(pin.lat, pin.lng));
                        pin_dotted_paths.push(dotted_path);
                        createMarkerLite(pin.members_in_this_location[member].through[through]);
                    }
                    for (var through=0; through < pin.members_in_this_location[member].site_connects_through.length; through++) {
                        dotted_path = [];
                        dotted_path.push(new google.maps.LatLng(pin.members_in_this_location[member].site_connects_through[through].lat, pin.members_in_this_location[member].site_connects_through[through].lng));
                        dotted_path.push(new google.maps.LatLng(pin.lat, pin.lng));
                        pin_dotted_paths.push(dotted_path);
                        createMarkerLite(pin.members_in_this_location[member].site_connects_through[through]);
                    }
                }
                var connections = []
                for (var equipment=0; equipment < pin.equipment.length; equipment++) {
                    if (pin.equipment[equipment].ifces) {
                        for (var ifce=0; ifce < pin.equipment[equipment].ifces.length; ifce++) {
                            connections.push({'from': pin.equipment[equipment].name, 'to':pin.equipment[equipment].ifces[ifce].name});
                            path = [];
                            path.push(new google.maps.LatLng(pin.equipment[equipment].ifces[ifce].lat, pin.equipment[equipment].ifces[ifce].lng));
                            path.push(new google.maps.LatLng(pin.lat, pin.lng));
                            pin_paths.push(path);
                            createMarkerLite(pin.equipment[equipment].ifces[ifce]);
                        }
                        for (var ifce=0; ifce < pin.equipment[equipment].connected_here.length; ifce++) {
                            path = [];
                            path.push(new google.maps.LatLng(pin.equipment[equipment].connected_here[ifce].lat, pin.equipment[equipment].connected_here[ifce].lng));
                            path.push(new google.maps.LatLng(pin.lat, pin.lng));
                            pin_paths.push(path);
                            createMarkerLite(pin.equipment[equipment].connected_here[ifce]);
                        }
                    }
                }
                if (pin.connecting){
                    for (var member=0; member < pin.connecting.length; member++) {
                        path = [];
                        path.push(new google.maps.LatLng(pin.connecting[member].lat, pin.connecting[member].lng));
                        path.push(new google.maps.LatLng(pin.lat, pin.lng));
                        pin_paths.push(path);
                        createMarkerLite(pin.connecting[member]);
                    }
                }
                $popup.html('<div class="close">X</div>' + description);
                $popup.addClass('active')
                for (var path=0; path < pin_paths.length; path++) {
                    var link = new google.maps.Polyline({
                        path: pin_paths[path],
                        geodesic: true,
                        strokeColor: '#009999',
                        strokeOpacity: 0.5,
                        strokeWeight: 4
                    });
                    active_links.push(link);
                    link.setMap(map);
                };
                var lineSymbol = {
                    path: 'M 0,-1 0,2',
                    strokeOpacity: 0.5,
                    scale: 3
                };
                for (var path=0; path < pin_dotted_paths.length; path++) {
                    var link = new google.maps.Polyline({
                        path:  pin_dotted_paths[path],
                        strokeOpacity: 0,
                        icons: [{
                          icon: lineSymbol,
                          offset: '0',
                          repeat: '20px'
                        }]
                    });
                    active_links.push(link);
                    link.setMap(map);
                };
                $body.removeClass('loading');
            });
        }

        function addInfoToMarker(map, loc) {
            google.maps.event.addListener(loc, 'mouseover', function() {
                infowindow.setOptions({maxWidth: 500});
                infowindow.setContent('<div style="overflow:hidden;line-height:1.35;min-width:200px;">' + loc.short_description + '</div>');
                infowindow.open(map, loc);
            });
            google.maps.event.addListener(loc, 'mouseout', function() {
                infowindow.close();
            });
        }

        function addMarkerToEvents(loc) {
            if (typeof loc.url !== 'undefined') {
                google.maps.event.addListener(loc, 'click', function() {
                    map.setCenter(loc.getPosition());
                    InitData(loc.url);
                    $('.location-index .locations-details ul.locations').text('loading...');
                });
            } else {
                google.maps.event.addListener(loc, 'click', function(){
                    load_location(loc.details, loc.description)
                });
            }
        }


        $('.location-index .locations-details ul.locations').on('click', 'li', function () {
            if (typeof($(this).data('details')) !== 'undefined') {
                load_location($(this).data('details'), $(this).data('description'));
            }
        });

        function createMarker(pin, data) {
            var options = {
                title: pin.name,
                pin_paths: []
            };
            options.short_description = '';
            if (initialUrl !== data.url) {
                options.position = new google.maps.LatLng(pin.lat, pin.lng),
                options.short_description = pinDescriptionHeaderTemplate({pin: pin});
                options.description = options.short_description;
                options.details = pin.details_url;
            } else {
                options.position = new google.maps.LatLng(pin.geolat, pin.geolng),
                options.short_description += '<h4>' + pin.name + '</h4>';
                options.short_description+= '<strong>Number of PoPs: </strong>' + pin.locations;
            }
            if (typeof pin.url !== 'undefined') {
                options.url = pin.url;
            }
            if (typeof pin.image !== 'undefined') {
                    options.icon = gmapIcons[pin.image + '-thumb'].url;
            }
            var loc = new google.maps.Marker(options);
            addInfoToMarker(map, loc);
            addMarkerToEvents(loc);
            return loc;
        }

        $filter.find('.reset').on('click', function () {
            if ($(this).parent().find('.search').val() !== '') {
                $(this).parent().find('.search').val('');
                $(this).parent().submit();
            }
        });

        // get urls vars
        function getUrlVars() {
            var vars = {};
            var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
                vars[key] = value;
            });
            return vars;
        }


        function InitData(url) {
            var fromUrl = false;
            tag = getUrlVars()['tag'];
            if (tag == undefined) {
                tag = $filter.find('input.search').val();
            } else {
                fromUrl = true
                $filter.find('input.search').val(tag);
            }
            if (tag == undefined) {
                tag = '';
            }
            if (tag !== '' && !fromUrl) {
                url += '?tag=' + tag;
            }
            $body.addClass('loading');
            $.getJSON(url, {}, function(data) {
                markers = [];
                if (data.pins.length === 0 ) {
                    // tag = '';
                    // $filter.find('input.search').val('');
                    $popup.html('<div class="close">X</div>Could not find any pops here.');
                    $popup.addClass('active error');
                } else {
                    var bounds = new google.maps.LatLngBounds(
                        new google.maps.LatLng(data.coords.minlat, data.coords.minlng),
                        new google.maps.LatLng(data.coords.maxlat, data.coords.maxlng)
                    )
                    mapOptions = {
                        center: new google.maps.LatLng(38.6149263, 24.085843),
                        zoom: 7,
                        styles: styleArray
                    };
                    var displayUrl = data.url.replace('/api', '');
                    if (document.referrer !== displayUrl) {
                        history.pushState({index: ''}, '', displayUrl);
                    }
                    var sidebar = $('.location-index .locations-details ul.locations');
                    sidebar.text('');
                    map = new google.maps.Map($map.get(0), mapOptions);
                    map.fitBounds(bounds);
                    if (data.city) {
                        $('.locations-details h3').text('PoPs in ' + data.city);
                    } else {
                        $('.locations-details h3').text('Cities with PoPs');
                    }
                    if (tag) {
                        $('.locations-details h5').text('with tag: ' + tag);
                    } else {
                        $('.locations-details h5').text('');
                    }
                    for (var i=0; i<data.pins.length; i++) {
                        var loc = createMarker(data.pins[i], data);
                        markers.push(loc);
                        loc.setMap(map);
                        if (data.pins[i].url) {
                            sidebar.append('<li><a href="' + data.pins[i].url.replace('api/', '') + '">' + data.pins[i].name + '</a></li>')
                        } else {
                            sidebar.append('<li data-details="' + data.pins[i].details_url + '" data-description="' + loc.description + '"">' + data.pins[i].name + '</li>')
                        }

                    }

                }
                $body.removeClass('loading');
            }).fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
            });
        }

        // whenever back button is pressed
        window.onpopstate = function() {
            var path_name = location.pathname.replace('/maps', '/api/maps');
            InitData(path_name);
        };

        $popup.on('click', '.close', function() {
            $popup.removeClass('active error');
        });

        $('.locations-details ul').on('click', 'a', function(e) {
            e.preventDefault();
            document.location = this.href + '?tag=' + tag;
        });

        $filter.on('submit', function(e) {

            e.preventDefault();
            tag = $(this).find('input[type="text"]').val();
            InitData(globalUrl)
        });

        InitData(globalUrl);

        $('.location-index .box').on('click', '.accordeon li h4', function () {
            $(this).parent().toggleClass('open');
        });
    }
});
