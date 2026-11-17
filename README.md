# Pokemon Showdown Bot

This is my very basic attempt at making my own Pokemon Showdown bot. Currently, it is quite rudamentry due to me being
shit at competitive pokemon and not having a lot of time to work on the bot itself. It only just selects the strongest 
move (not acocunting for things like stat drops) and a very basic weighting system for choosing the next pokemon to send
out.

## How to fight it

So you want to fight it? Just follow these simple steps:
 - Visit [Pokemon Showdown](https://play.pokemonshowdown.com/) as hyperlinked or copy paste https://play.pokemonshowdown.com/ into your browser of choice.
 - Make an account if you don't have one already or sign in.
 - Click "Find a User"
 - Enter "StuntsChild" into the "Username" textbox
 - Click the Challange Button
 - Make sure the format is Gen 9 Randoms Singles (I think this is the default)
 - Click Challange
 - NOTE: The bot will only accept challanges of the correct battle format. So no you can't so a metrenome battle against it.
 - The bot should auto accept the challange if it is not in 20 battles simultaneously, and it is challanged in the correct format.

## How to set it up for yourself
  So you want to run this shit ass bot your yourself? Follow these instructions to do so! (Tested on Debian 13)


    git clone https://github.com/Stu67nt/PokemonShowdownBot
    cd PokemonShowdownBot
    python3 -m venv venv
    source venv/bin/activate 
    pip install -r requirements.txt

  Make a .env file in the same directory as the python script as follows.

    SHOWDOWN_USERNAME=ACCOUNTNAMEHERE
    SHOWDOWN_PASSWORD=ACCOUNTPASSWORDHERE

  Once complete run the main python file with something like:

    python3 main.py
    
## How good is it?
Pretty bad tbh it doesn't have a lot of logic built into it just clicks the strong moves and prays. Not put it on the ladder and I feel like putting it on the ladder is an insult to whoever plays against it.