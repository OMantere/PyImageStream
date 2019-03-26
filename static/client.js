var img = document.getElementById("liveImg");
var ws = new WebSocket("ws://localhost:8002/");
ws.binaryType = 'arraybuffer';

function requestImage() {
    ws.send('more');
}

ws.onopen = function() {
    console.log("connection was established");
    requestImage();
};

ws.onmessage = function(evt) {
    var arrayBuffer = evt.data;
    var blob  = new Blob([new Uint8Array(arrayBuffer)], {type: "image/jpeg"});
    img.src = window.URL.createObjectURL(blob);
    requestImage();
};
