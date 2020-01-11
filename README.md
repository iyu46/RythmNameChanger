# RythmNameChanger
# This bot changes the Rythm music bot's nickname in a Discord server based on what's currently playing.
### Fully operational (according to original planned specification), but performance is hampered by a bug in the Discord client software.

## Requirements
``` pip install -r requirements.txt ```


idea for workflow:

1. necessitate `!settings announcesongs on` for Rythm bot
2. have commands such as `!mbnc active [on|off], !mbnc deletemsgs [on|off]`\*
3. use Rythm's  `announcesongs` feature and watch the music channel for Now Playing messages, and change Rythm's nickname to the video title string (or concatenate so that it fits)

note 1. store original nickname (nickname given to Rythm before music activity) and reset nickname to that stored string once Rythm is kicked from channel or disconnects from inactivity

\*note 2. use `!mbnc deletemsgs [on|off]` to toggle deleting Rythm's Now Playing message once it's read so the chat isn't flooded
