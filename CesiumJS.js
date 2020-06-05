/* If you're feeling fancy you can add interactivity 
    to your site with Javascript */

// prints "hi" in the browser's dev tools console
// console.log("hi");
/* Set the width of the side navigation to 250px and the left margin of the page content to 250px and add a black background color to body */

Cesium.Ion.defaultAccessToken =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI0Mjg2MWMxMS1jOWExLTRjNzctODcyYS1jOTAxMTdlYmM0ZjYiLCJpZCI6MjU2ODYsInNjb3BlcyI6WyJhc3IiLCJnYyJdLCJpYXQiOjE1ODY0MDU3MjB9.LZF2OJLOQa9qyjuDzwWGpdZ3S-0TzhruwZsXO0aWzjI";
let viewer = null;
let options = {};
let dataSourcesArray = [];
let planesInterval = null;
let camera = viewer.camera;

camera.percentageChanged = 0.001;
camera.changed.addEventListener(
  function()
  {
   //view rectangle
   let posUL = cam.pickEllipsoid(new Cesium.Cartesian2(0, 0), Cesium.Ellipsoid.WGS84);
   let posLR = cam.pickEllipsoid(new Cesium.Cartesian2(viewer.canvas.width, viewer.canvas.height), Cesium.Ellipsoid.WGS84);
   let posLL = cam.pickEllipsoid(new Cesium.Cartesian2(0, viewer.canvas.height), Cesium.Ellipsoid.WGS84);
   let posUR = cam.pickEllipsoid(new Cesium.Cartesian2(viewer.canvas.width, 0), Cesium.Ellipsoid.WGS84);

   //north
   cartographic = ellipsoid.cartesianToCartographic(posUL);
   maxLat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(2);
   
   //east
   cartesian = rotate(cartesian,rotatee,Math.PI/2); //rotatee now rotater
   cartographic = ellipsoid.cartesianToCartographic(posUR);
   maxLon = Cesium.Math.toDegrees(cartographic.longitude).toFixed(2);
   
   //south
   cartesian = rotate(cartesian,rotatee,Math.PI/2); //rotatee now rotater
   cartographic = ellipsoid.cartesianToCartographic(posLR);
   minLat = Cesium.Math.toDegrees(cartographic.latitude).toFixed(2);
   
   //west
   cartesian = rotate(cartesian,rotatee,Math.PI/2); //rotatee now rotater
   cartographic = ellipsoid.cartesianToCartographic(posLL);
   minLon = Cesium.Math.toDegrees(cartographic.longitude).toFixed(2);
   }.bind(camera));


const checkAppliedDataSources = (type) => {
  let found  = false;
  let ob = null;
  dataSourcesArray.forEach((itm, idx) => {
    if (!found) {
      if (itm.type == type) {
        ob = {
          item: itm,
          arrIdx: idx
        };
        found = true;
      }
    }
  });
  return ob;
};

const removeArrDataSource = (idx) => {
  let tmp = [];
  dataSourcesArray.forEach((item, index) => {
    if (index != idx) {
      tmp.push(item);
    }
  });
  dataSourcesArray = tmp;
};


const openNav = () => {
  document.getElementById("mySidenav").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
  document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
};

/* Set the width of the side navigation to 0 and the left margin of the page content to 0, and the background color of body to white */
const closeNav = () => {
  document.getElementById("mySidenav").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
  document.body.style.backgroundColor = "white";
};

const obj = item => {
  console.log("obj click", item);
};

const updatePlanes = () => {
  console.log('interval test');
}

const displayPlanes = () => {
    console.log("function called");
    // let planesData = "https://cdn.glitch.com/23e583bd-d43a-4df9-b6a8-e287510e0e72%2Fka2007-opensky.kml?v=1589280285541";
    let planesData = "FlightPath.czml";
    var checkbox = document.getElementById("planes");
    // Checkbox state changed.
    if (checkbox.checked) {
      // Show if not shown.
      //if (!viewer.dataSources.contains(satData)) {
      console.log("checked");
      viewer.dataSources.add(Cesium.CzmlDataSource.load(planesData)).then(datasource => {
          let tmpItm = {
            type: 'planes',
            data: datasource
          };
          dataSourcesArray.push(tmpItm);
          viewer.flyTo(datasource);
          viewer.zoomTo(datasource);
          console.log('dataSourcesArray', dataSourcesArray);
          planesInterval = setInterval(updatePlanes, 30000);
      });
      //}
    } else {
      // Hide if currently shown.
      console.log("unchecked");
      let src = checkAppliedDataSources('planes');
      console.log('src', src);
      if (src != null) {
        viewer.dataSources.remove(src.item.data);
        removeArrDataSource(src.arrIdx);
        clearInterval(planesInterval);
        planesInterval = null;
      }
    }
  };

const displaySat = () => {
  console.log("function called");
  let satData = "SatellitePath.czml";
  var checkbox = document.getElementById("sat");
  // Checkbox state changed.
  if (checkbox.checked) {
    // Show if not shown.
    //if (!viewer.dataSources.contains(satData)) {
    console.log("checked");
    viewer.dataSources.add(Cesium.CzmlDataSource.load(satData)).then(datasource => {
        let tmpItm = {
          type: 'satelite',
          data: datasource
        };
        dataSourcesArray.push(tmpItm);
        viewer.flyTo(datasource);
        viewer.zoomTo(datasource);
        console.log('dataSourcesArray', dataSourcesArray);
    });
    //}
  } else {
    // Hide if currently shown.
    console.log("unchecked");
    let src = checkAppliedDataSources('satelite');
    console.log('src', src);
    if (src != null) {
      viewer.dataSources.remove(src.item.data);
      removeArrDataSource(src.arrIdx);
    }
  }
};

//$('.cesium-viewer-toolbar').addClass('d-none');
//$('.cesium-viewer-animationContainer').addClass('d-none');
//$('.cesium-viewer-timelineContainer').addClass('d-none');
//$('.cesium-widget-credits').addClass('d-none');

const init = () => {
    dataSourcesArray = [];
    viewer = new Cesium.Viewer("cesiumContainer");
    options = {
        camera: viewer.scene.camera,
        canvas: viewer.scene.canvas
    };
    displaySat();
    displayPlanes();    
};

init();

