- [ ] playlist
- [ ] db
- [X] refactor to this module
- [ ] radio
- [ ] youtube playlist
- [ ] save to db

!play [youtube_link string]
input: music_player object, youtube_link string
workflow: 
    check if youtube_link is correct
        if false: exit
    check if music_player.player is alive
        if true:
            kill music_player.player
    set music_player.playing_now to youtube_link
    create music_player.player and play youtube_link            
    print "playing now youtube_link"
    exit    
output: NULL

!add [youtube_link string]
input: music_player object, youtube_link string
workflow: 
    check if youtube_link is correct
        if fasle: exit
    append youtube_link to music_player.playlist
    print "added youtube_link to playlist"
    exit    
output: NULL

!next
input: music_player object
workflow: 
    check if music_player.player is alive
        if true:
            kill music_player.player
    check music_player.playlist size
        if 0:
            print "playlist is empty"
            exit
    pop first record from playlist
    set music_player.playing_now to first_record
    create music_player.player and play first_record            
    print "playing now first_record"
    exit     
output: NULL

!pause
input: music_player object
workflow: 
    check if music_player.player is alive
        if true:
            send pause to music_player.player
        if false:
            print "nothing is playing now"
    exit     
output: NULL

!stop
input: music_player object
workflow: 
    check if music_player.player is alive
        if true:
            kill music_player.player
        if false:
            print "nothing is playing now"
    exit     
output: NULL

!resume
input: music_player object
workflow: 
    check if music_player.player is alive
        if true:
            send resume to music_player.player
        if false:
            check if music_player.playing_now is string
                if true:
                    create music_player.player and play first_record
                if false:
                    print "nothing is playing now"
    exit     
output: NULL


