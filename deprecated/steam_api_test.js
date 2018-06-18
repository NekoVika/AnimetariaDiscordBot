var SteamApi = require('steam-api');
const https = require("https");
var fs = require('fs');

code_sapi=fs.readFileSync('sapi.txt').toString()
var app = new SteamApi.App(code_sapi);

 
//App Methods
app.appDetails(661920).done(function(result){
  console.log(result);
});
 
// app.GetAppList().done(function(result){
//   console.log(result);
// });

// https.get("https://store.steampowered.com/appreviews/70?json=1", res => {
//   res.setEncoding("utf8");
//   let body = "";
//   res.on("data", data => {
//     body += data;
//   });
//   res.on("end", () => {
//     body = JSON.parse(body);
//     console.log(body
//     );
//   });
// });