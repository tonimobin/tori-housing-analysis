window.myNamespace = Object.assign({}, window.myNamespace, {  
    mySubNamespace: {  
        pointToLayer: function(feature, latlng, context) {  
            return L.circleMarker(latlng)  
        }  
    }  
});

L.geoJSON(seine_mar,{
    onEachFeature: function(feature, layer){
      layer.bindTooltip('Hi there', {permanent: true}).openTooltip(); 
      // or over a feature property layer.bindTooltip(feature.properties.customTitle)
    }
   }).addTo(map)