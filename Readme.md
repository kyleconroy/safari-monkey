# Safari Monkey

Userscripts.org has thousands of scripts for turbo-charging your favorite websites. 

For the first time, Safari Monkey let's you unleash this power in Cuptertino's browser of choice.

## Creating Extensions

First, you will need to sign up for a Safari developer account and obtain a valid certificate. Start the process [here][1]. If anyone has a suggestion on how to make this process quicker, I would love to talk. 

[1]: http://theappleblog.com/2010/06/11/how-to-build-a-safari-extension/

Next, find a script at <http://www.userscripts.org> and copy the url (or code ID number).

Next, run 

    ./safari_monkey.py http://userscripts.org/scripts/show/NNNNN

or

    ./safari_monkey.py NNNNN

The scripts creates a new Safari extension scriptNNNNN.safariextension

Open up Safari and install! 

## Todo

I have only tested a handful of scripts, so more testing is always a good thing

It would be great to have the script create the .safariextz files, but I am not sure how to do the code signing

