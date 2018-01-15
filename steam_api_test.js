var SteamApi = require('steam-api');
var fs = require('fs');

code_sapi=fs.readFileSync('sapi.txt').toString()
var app = new SteamApi.App(code_sapi);

 
// // App Methods
// app.appDetails(661920).done(function(result){
//   console.log(result);
// });
 
app.GetAppList().done(function(result){
  console.log(result);
});
