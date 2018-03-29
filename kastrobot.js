const Discord = require('discord.js');
const client = new Discord.Client();
const removeEmptyLines = require("remove-blank-lines");

var sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database('animeretardia.sqlite', (err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to the animeretardia database.');
});

const MH_GUILD_ID = '270727104319062026';

const user_list={"Lier": "270723318427025418",//Lier
                 "Vika": "270911343274491905",//Vika
                 "Mudj": "271006635126816778",//Mudj
                 "Kaastro": "270974444871221259"//Volera
}

var kastrords = [/k(a*)ts[^\s]+/gi,/k(a*)str[^\s]+/gi,/к(а*)стр[^\s]+/gi,/к(а*)тс[^\s]+/gi,/в(а*)лер[^\s]+/gi,/v(a*)ler[^\s]+/gi];

var madjords = [/m[a|u|y]+dj\w*/gi,/м[у|а|ю|я|о|е|ы|э|и|і]+дж\w*/gi,/мудж\w*/gi];

// Word parts for Mudj
var madj_1 = ["Мун","Мня","Мин","Маа","Минин","Муа","Мюн"]
var madj_2 = ["адж","нядж","идж","ядж","удж","юдж","ньдж","ажд","няжд","ижд","яжд","ужд","южд","ньжд"]


client.on("ready", () => {
    client.user.setUsername("CHOPK");
    MH_GUILD = client.guilds.get(MH_GUILD_ID);
    GUILD_CH = MH_GUILD.channels.find(ch => ch.name === 'guild');
    G_RANG_CH = MH_GUILD.channels.find(ch => ch.name === 'g-rank');

    // This event will run if the bot starts, and logs in, successfully.
    console.log(`Bot has started, with ${client.users.size} users, in ${client.channels.size} channels of ${client.guilds.size} guilds.`); 
    // Example of changing the bot's playing game to something useful. `client.user` is what the
    // docs refer to as the "ClientUser".
    client.user.setGame(`with himself`);
  });



client.on("presenceUpdate", (old, new_) => {
    if (Object.values(user_list).indexOf(new_.user.id)>=0){
        //console.log(old.presence.status, new_.presence.status, ['idle', 'online', 'dnd'].indexOf(new_.presence.status));
        if (old.presence.status == 'offline' && ['idle', 'online', 'dnd'].indexOf(new_.presence.status) >= 0){
            G_RANG_CH.send(new_.user.username+' logged in!');
            if (new_.user.id == user_list['Kaastro']){
                GUILD_CH.send('Бажаємо здоров\'я, товаришу Кааастро!')
            }
        }
    }
});
client.on("message", async message => {
    if(message.author.bot) return;
    if (message.content.startsWith('!')){
        const args = message.content.slice(1).trim().split(/ +/g);
        const command = args.shift().toLowerCase();
        switch(command){
            case 'games':{
                if (args.length==0){
                    message.channel.send("В лол скатайте");
                }
                else if (args[0]=="coop"){
                db.all(`SELECT * FROM games_features WHERE CategoryCoop='True' ORDER BY RANDOM() LIMIT 1;`, [], (err, rows) => {
                    if (err) {
                      throw err;
                    }
                    //console.log(rows);
                    message.channel.send(rows[0].QueryName+" http://store.steampowered.com/app/"+rows[0].QueryID);
                  });
                break;
                }
            }

        }
        return;
    }
    for(i=0,x=kastrords.length;i<x;i++){
        if(message.content.toLowerCase().search(kastrords[i])>=0){            
            message.channel.send("Слався Кааастризм его великий! Да прибудет воля Кааастро!");
            break;
        };
    };

    for(i=0,x=madjords.length;i<x;i++){
        var found_w=message.content.match(madjords[i]);
        if(found_w){
            var right_madj = madj_1[Math.floor((Math.random() * madj_1.length))]+madj_2[Math.floor((Math.random() * madj_2.length))]
            message.channel.send("`>>"+found_w[0]+"` Возможно, вы имели ввиду "+right_madj+"?");            
        }
    };

    

    
    // const words = message.content.trim().split(/ +/g);
    // const check_words = words.shift().toLowerCase();
    // console.log(check_words);
});

var fs = require('fs');
code_l=removeEmptyLines(fs.readFileSync('./cd.txt').toString().replace(/\r?\n|\r/g,""))
client.login(code_l);




