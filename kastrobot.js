const Discord = require('discord.js');
const client = new Discord.Client();
const MH_GUILD_ID = '270727104319062026';

const user_list={"Lier": "270723318427025418",//Lier
                 "Vika": "270911343274491905",//Vika
                 "Mudj": "271006635126816778",//Mudj
                 "Kaastro": "270974444871221259"//Volera
}

var kastrords = [/k(a*)tso/g,/k(a*)stro/g,/к(а*)стро/g,/к(а*)тсо/g];

var madjords = [/madj/gi,/мадж/gi,/мудж/gi];

// Word parts for Mudj
var madj_1 = ["Мун","Мня","Мин","Маа","Минин"]
var madj_2 = ["адж","нядж","идж","ядж","удж"]


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


//todo on kaaastro login greet kaaastro
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
            message.channel.send(">"+found_w[0]+" Возможно вы имели ввиду "+right_madj);            
        }
    };

    
    // const words = message.content.trim().split(/ +/g);
    // const check_words = words.shift().toLowerCase();
    // console.log(check_words);
});

var fs = require('fs');
code_l=fs.readFileSync('cd.txt').toString()
client.login(code_l);




