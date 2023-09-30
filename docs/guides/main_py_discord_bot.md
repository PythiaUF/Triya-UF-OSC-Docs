---
description: A guide that explains main.py in Al Bot 3.0.
---


# What is main.py doing in Al Bot 3.0?

## The Code
*This may be changed in the future, but the format should look similar regardless.* You can see the latest copy of the code at [the GitHub Repo](https://github.com/ufosc/Al-Bot-3.0/blob/main/main.py).

```python
import os
import contextlib
import asyncio

from interactions import Client, Intents, listen, slash_command, SlashContext
from dotenv import load_dotenv

load_dotenv()  # load the .env file

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine


@listen()  # this decorator tells interactions.py that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command()  # this decorator tells interactions.py to make a slash command with the corresponding name
async def ping(ctx: SlashContext):
    # slash commands are always passed a SlashContext object, used to actually respond to the command
    await ctx.send("Pong!")  # send a message to the channel the command was used in


async def main():
    bot.load_extensions("exts")
    await bot.astart(os.environ["BOT_TOKEN"])

if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
```

## Dotenv and Environmental Variables
Skipping over the imports (they're just imports, nothing too important, they're just pieces of code from other people that we're using), let's explain the first line of proper code: `load_dotenv()`

Environmental variables are variables stored either on your operating system or somewhere outside of a program. These variables store a lot of information, from the paths of every file that can be ran in a terminal to the current directory a user is in. If you know what you're doing, you can also use it to store your own variables in it - this basically allows you to have a configuration with variables to define without going through the process of making a whole config file, which is very useful for us. Setting your own variables is typically done in scenarios where the contents themselves are a bad idea to hardcode into your program - if you remember, a bot token is too powerful to be leaked onto the internet, so it works perfectly here!

In Python, these variables are stored in `os.environ`, in the `os` package. `os.environ`, in Python, a *dictionary* - essentially, *values* in a dictionary are tied to *keys*, IE `BOT_TOKEN` could be the key to get the value of your bot token. You use dictionaries by doing `a_dict["key"]`, similar to using a list's index to get a value, just with a key. In this case, `os.environ` uses the variable names that we or the operating system can define as *keys*, and the values they store as *values.*
If you're still confused by this, I highly suggest Googling "python dictionary" or the like - there are plenty of things that define and show examples of it better than I can explain here.

Anyways, you may have noticed that the setup instructions required you to make a file called `.env` and place some variables in there, like your bot token and the URL of the API you want to put. We don't want to hardcode either of these things directly into our Python code, after all (the bot token because that's secret, the URL of the API as that could change as needed). However, `.env` is... just a file at the end of the day. Your OS and Python aren't going to read it and make the values in there environmental files automagically, at least by itself.

`load_dotenv()` takes care of reading your `.env` file, parsing it, and making it into environmental files we can use through `os.environ`. It really is that simple.

## Client and a Touch of interactions.py
As you probably know, we're making a Discord bot that interacts with the Discord API. Hopefully you have some understanding of what a (web-based) API is already, so we won't discuss that too much, but Discord has made its own API that allows bots to interact with Discord through specialized web requests - for example, there are web requests to get a channel and its information, send a message to a channel, and so much more. These web requests can become quite complex for someone to write manually, and we aren't even going to touch on the headache of getting real time updates about things from Discord (it uses something called websockets, if you're interested), so instead we'll be leveraging a *Discord library* to do this.

Libraries aren't a new concept - they're essentially a bunch of code that other developers can find useful (often packaged up as *packages*). A Discord library, as you can imagine, contains a bunch of code that other developers can use to interact with the Discord API without doing it themselves - they handle the heavy work of getting real time updates and making web requests so that developers can actually focus on making something for their users.

We're using interactions.py here. I won't get into the nitty gritty about why we're picking this specific library, but it is a very easy to use library that works well for beginners and is very easy to develop fully featured bots with. interactions.py stores its code in `interactions`, so we pull code from it from time to time. In `main.py`, we're using direct object imports (`from interactions import X`) to import specific classes and functions from it, though you can also do something like:
```python
import interactions as ipy  # or any shorthand you want to use... or you can remove the "as ipy" part entirely and use "interactions"
ipy.X  # ie ipy.Client
```
Pick whatever style you prefer. For my own code, I prefer using `import interactions as ipy`, but `main.py` attempts to follow the code examples [in the guides it has](<https://interactions-py.github.io/interactions.py/Guides/>).

Anyways, back to the code itself: `bot = Client(...)` is a pretty important piece of code. `Client`, in interactions.py, is an important class that is sort of a container representing your DIscord bot - it's the Python equivalent to it, in a way. `Client` handles connecting to Discord, sending and receiving web requests, and more, and you'll be using `bot` frequently as a means to interact with all of that. We'll talk abou the `intents` later - they mean more for events than they do here particularly.

If you don't know what a class or object is... admittedly, that is a hard concept to explain. Google is your friend, but essentially, a *class* is a... thing in programming that defines a set of behaviors and properties that you can use in an *object*, an instance of that class. For example, a dog could be a class, and my own dog (unforunately back at my parents' home) is an instance/object of that class.
Here, our `bot` is an *instance*/*object* of `Client`. For more examples, `3` is an *instance* of `int` (integer), `"Hello!"` is an *instance* of `str` (string), and so on.

## `listen()` and Events
I mentioned how Discord sends real time data to your bot that interactions.py handles - these pieces of data come in *events*. Events get triggered whenever a lot of things happen in Discord - when the bot is declared "ready" by Discord, when a channel is updated, when a message is sent to a channel the bot can see, etc. interactions.py makes hooking into these events easy - you simply *listen* to them with the right format.

Here, we're listening to when the bot is declared to be "ready".[^1] Of course, we do that with `listen()`, which *listens* into the event being triggered and then runs the function[^2] underneath it, but how exactly does interactions.py know that you want the "ready" event specifically? Easy: here, it reads the function name (`on_ready`), ignores the `on_`, and sees `ready`, which corresponds to an event it knows about.

Well, actually, it corresponds to a `Ready` *event object*, which is an object that contains information about the event itself. For things like the "ready" event, they're basically placeholders for the event itself, but there are some events, like `ChannelCreate`, that contain information like the channel that was created in the first place or the like. These event objects are then passed to your function in most cases - in fact, even "ready" events can get an object, but since `Ready` has no useful information, interactions.py is smart enough to see our function, note that it has nowhere to accept an event object, and be like "well, the object is useless anyways, fair enough."

There are alternative ways of listening to an event. Perhaps the most intuitive of these alternate ways is using the event object itself in `listen()`:
```python
# other imports here
from interactions.api.events import Ready
# or ipy.events.Ready, if you did import interactions as ipy

@listen(Ready)
async def my_function():
    ...
```

Actually, I usually recommend the above method, but since this is a ready event, the one in `main.py` is fine.

Oh right, to explain what I mean, here's how an event function looks like if it actually has any data:
```python
from interactions.api.events import ChannelCreate

@listen(MessageCreate)
async def my_function(event: ChannelCreate):
    ... # channel is in event.channel

# or
@listen()
async def on_channel_create(event: ChannelCreate):
    ...
```

To circle back to that mysterious `intents` we passed into our bot earlier - that actually tells Discord what events we want to receive in the first place. Right now, we're just listening to all of the "default" events/intents, which all events except some weird special ones.

!!! note "Intents.DEFAULT"
    Using the default intents is fine (and in fact works really well for developmental purposes). However, you would narrow down the intents you are using for two reasons:
    1. Less intents means less events to process, reducing strain and/or traffic on your bot.
    2. Less intents means you don't see things you don't *need* to see, thus making your bot more secure and private.

## Slash Commands
Try typing in `/` in a bot channel command or the like. You'll see a series of *slash commands* - commands offered by bots that are triggered through this method. Slash commands allow you to define how you want users to interact with your bot in whatever way you want, and then get a result based on that. For example, `/8ball` will tell a bot like YAGPDB.xyz to run its 8 ball code and then send you the result back. Of course, we get to do this with our bot too, woo!

Slash commands, in interactions.py, are defined with the `@slash_command()`... thing[^3]. This *can* take in a whole host of options, but we don't need any of them right now. Using that will automatically make the function below it turn into a slash command - with no arguments passed to `@slash_command()`, it uses the function below it's name as the name of the slash command, and the function itself as the thing to run when the slash command is called.

The function below is mostly normal (once again, `async def` is just a fancy type of function for when `await` is used in Python code, don't think about it too much). This function takes in an argument, however. In this case, it only expects one argument, which is the *slash context*. This is the *context of the current run of the slash command* - it contains information about who's running the slash command and where, and also allows us to respond to this specific run of the slash command.

We take this in as a `ctx` argument, though it could be named anything[^4]. Here, we take that specific run and respond to it (via `ctx.send`) with a "Pong!" - hence, we've ponged the ping a la ping-pong[^5]. Running this code should show that result - the bot will send a message that has "Pong!" whenever you run `/ping`.

## The Rest of the Code
The rest of the code is perhaps a bit too complex to explain (and honestly, it doesn't matter too much), but just to note:
- We load all [extensions in a folder](<https://interactions-py.github.io/interactions.py/Guides/20%20Extensions/>) called `exts` right before we start the bot. You should *never* add your own code to `main.py` when contributing back to the project itself - instead, use extensions, as linked before, and as demonstrated [in the quotes example](<https://github.com/ufosc/Al-Bot-3.0/blob/main/exts/quotes.py>). This helps organize things.
- `bot.astart` actually starts the communication with Discord, establishing the stuff to receive events. We also tell Discord which bot we're running this code for with our token now, as retrieved earlier.
- We only start the bot if we're running the bot directly, instead of through an import. Ignore the `contextlib.suppress`, that isn't important.

[^1]: Not strictly true. Discord does indeed send a "READY" event when the bot is declared to have all of the basic requirements to start off getting real-time data, but this isn't strictly when the bot *has* the data it needs to be ready. Most critically, the bot doesn't know what servers it is in during the READY event - it actually receives information about each server its in on a rolling basis, getting data one by one around (but not necessarily before) the READY event. Many libraries, including interactions.py, wait for all of the guilds to come in and *then* dispatch the "ready" event, as to represent how the bot has all of the data it needs to get started.

[^2]: A function "are self contained modules of code that accomplish a specific task. Functions usually take in data, process it, and return a result." - from [University of Utah](https://users.cs.utah.edu/~germain/PPS/Topics/functions.html)
For example, you could have a function that takes in a list of numbers and returns the average of them. If you need better examples, Google is your friend.
These specifically are *coroutines*, which are asynchronous functions - you don't need to worry too much other than if you see something that uses `await`, you probably need a function that has `async def` instead of `def` to use it.

[^3]: This is a *decorator*, a function which either takes in another function or returns a function that takes another function (yes, I said that correctly). Python allows using this cool and convenient format to declare things, but it's equivalent to `slash_command()(ping)` at the end of the day.
As for why you would ever use this - interactions.py specifically is using this as a way of adding data to the function itself to let future interactions.py know it's a slash command and how it's defined.

[^4]: Event objects being passed in can also be named anything. Sorry for only telling you this now, but no, it doesn't *have* to be `event`.

[^5]: As for why Ping-pong... it's a programming joke. Don't worry about it.
