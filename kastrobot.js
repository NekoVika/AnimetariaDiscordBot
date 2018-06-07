const Discord = require('discord.js');
const yaml = require("js-yaml");
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

// lines var
var lines = {};
var config = {};

function id2name(id){
    return Object.keys(USERS).find(key => USERS[key] === id);
}

function name2id(name){
    return USERS[name];
}

function toArray(inst){
    if (!Array.isArray(inst)) inst = [inst];
    return inst;

}

function get_random_element(elements){
    return elements[Math.floor(Math.random()*elements.length)];
}


function load_yaml(path){
    try {
        config = yaml.safeLoad(fs.readFileSync(path, 'utf8'));
    } catch (e) {
        config = {};
        console.log("Can't load yaml file. Reason: "+e);
    }
    return config;
}

function configure(config){
    client.user.setUsername(config['NAME']);
    GUILD = client.guilds.get(config['GUILD_ID']);
    CHANNELS = {};
    var channels = config['CHANNELS'];
    for (chan in channels){
        CHANNELS[chan] = GUILD.channels.find(ch => ch.name === channels[chan]);
    }
    client.user.setGame(config['DEFAULT_GAME']);

    USERS = config['USERS'];

    ADDITIONAL = {};
    var added = config['ADDITIONAL_LOAD'];
    for (ad in added){
        ADDITIONAL[ad] = load_yaml('etc/'+added[ad]+'.yaml') // FIXME: Ugly. Need more gracefull way to load added configs
    }

}

client.on("ready", () => {

    config = load_yaml('etc/config.yaml')
    if (config){
        configure(config);
        // client.user.setUsername(config.get('NAME'));
        // guild = client.guilds.get(config.get('GUILD_ID'));

        // var channels = config.get('channels');

        // MH_GUILD = client.guilds.get(MH_GUILD_ID);
        // GUILD_CH = MH_GUILD.channels.find(ch => ch.name === 'guild');
        // G_RANG_CH = MH_GUILD.channels.find(ch => ch.name === 'g-rank');

        // // This event will run if the bot starts, and logs in, successfully.
        // console.log(`Bot has started, with ${client.users.size} users, in ${client.channels.size} channels of ${client.guilds.size} guilds.`); 
        // // Example of changing the bot's playing game to something useful. `client.user` is what the
        // // docs refer to as the "ClientUser".
        // client.user.setGame(`with himself`);
    }else{
        // TODO: handle when there is no config
    }
  });



client.on("presenceUpdate", (old, new_) => {
    //if (Object.values(ADDITIONAL.users).indexOf(new_.user.id)>=0){
        // Going online
    var user_name = id2name(new_.user.id);
    if (Object.keys(ADDITIONAL.lines.on_presence_update).indexOf(user_name)>=0 && 
        old.presence.status == 'offline' && ['idle', 'online', 'dnd'].indexOf(new_.presence.status) >= 0){

        var reaction = ADDITIONAL.lines.on_presence_update[user_name],
            messages = toArray(reaction.messages);
        
        messages.forEach(mes => {
            var channels = toArray(mes.channels),
                answer = get_random_element(toArray(mes.answers)),
                keys = mes.keys;
            console.log('##', answer, keys);
            if (keys != undefined){
                keys = reduce_dict(keys);
                answer = template_string(answer, keys);
            }
            channels.forEach(ch => {
                CHANNELS[ch].send(answer);
            })
        });
    }
});
client.on("message", async message => {
    if(message.author.bot) return;
    if (message.content.startsWith('!')){  // TODO: this part also
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
    // Answering to message by keywords
    var on_message = ADDITIONAL.lines.on_message;
    on_message.forEach(block => {
        var cond = block.conditions;
        if (!Array.isArray(cond)) cond = [cond];
        cond.forEach(elem => {
            elem = new RegExp(elem, 'gi');  // FIXME: figure out this is regex
            if(message.content.toLowerCase().search(elem) >=0 ){
                var reac = block.answers,
                    keys = block.keys;
                if (!Array.isArray(reac)) reac = [reac];
                var answer = reac[Math.floor(Math.random()*reac.length)];
                if (keys != undefined){
                    keys = reduce_dict(keys);
                    answer = template_string(answer, keys);
                }
                message.channel.send(answer);
            }
        });
    });
});

var reduce_dict = function(dict){
    var res = {};
    for (var key in dict) {
        if (dict.hasOwnProperty(key)) {
            var items = dict[key];
            if (!Array.isArray(items)) items = [items];
            var item = items[Math.floor(Math.random()*items.length)];
            res[key] = item;
        }
    }
    return res;
}

var template_string = function(template, keys){
    var result = template;
    RE = /{(\w*)}/g
    sk = template.match(RE);
    sk.forEach( elem => {
        var key = elem.replace(/{|}/g, ''), 
            value = keys[key];
        result = result.replace(elem, value);
    });
    return result;
}


var fs = require('fs');
code_l=removeEmptyLines(fs.readFileSync('./cd.txt').toString().replace(/\r?\n|\r/g,""))
client.login(code_l);




