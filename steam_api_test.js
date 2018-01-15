var SteamApi = require('steam-api');
var fs = require('fs');

var app = new SteamApi.App("");

 
// // App Methods
// app.appDetails(661920).done(function(result){
//   console.log(result);
// });
 
app.GetAppList().done(function(result){
  console.log(result);
  fs.writeFileSync('./data.json', result.join(',') , 'utf-8'); 
  fs.writeFileSync("app_list.txt", result);
});
