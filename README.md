# TornadIO chat + clock

piece of crap, just a sandbox to learn socket.io


## install dependencies

    mkvirtualenv tornadio-chat
    pip install -Ur requirements.txt

## running

    python app/server.py


# user experience goals

### beyond the "emoticon" concept

nowadays people express themselves (emotionally) through *emoticons*,
the idea that the the person `A` will talk to the person `B` through 2
different windows (conceptually, since technically it could two
floating `<div>` elements)

#### moods

when any user sends a emoticon `X`, it will match the designed `color`, and `picture` for a mood `Y`

where:

`color` will bear role for expressing the mood `Y`

`picture` should be also a way to express the mood `Y`,
now through a creative-commons licensed picture of some person that mood


#### happy

valid emoticons: `>:]`, `:-)`, `:)`, `:o)`, `:]`, `:3`, `:c)`, `:>`, `=]`, `8)`, `=)`, `:}`, `:^)`
color: `yellow`


##### shy

valid emoticons: `:$`
color: `yellow` blushed with `pink`, like cheeks

... draft to be continued
