import discord
import asyncio
import random

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.error import URLError


########################################################################
# BEGIN CONFIG
########################################################################

#######################
# SET DROP RATES HERE #
#######################
rate_common = "1/8"
rate_uncommon = "1/32"
rate_rare = "1/128"
rate_very_rare = "1/512"


#####################################
# ADD MOBS WITH MULTIPLE DROPS HERE #
# KEEP THEM LOWERCASE LETTERED      #
# DONT FORGET THE COMMAS AND QUOTES #
#####################################
multipleDropMobs = {"zulrah" : 2}
# example for ^ ---> ["zulrah" : 2, "cow" : 1, "elvarg" : 99]



#####################################
# PLACE YOUR TOKEN HERE             #
# LEAVE THE ' ' AROUND IT           #
#####################################
token = 'your_token_here'

########################################################################
# END CONFIG
########################################################################
baseUrl = 'http://oldschoolrunescape.wikia.com/wiki/'

# create a new client
client = discord.Client()


helpm = "Bot functions:\r\n```\r\n!slay MonsterName\r\nexample: !slay Zulrah```"

def queryPage(url):
    # the list to be returned
    returnList = []
    # create a client and grab the page
    try:
        uClient = uReq(url)
    except URLError as e:
        # return error if page not found
        print("Error, page not found.")
        return("Error")
    # read the page data to a var
    page_html = uClient.read().decode('utf-8', 'ignore')
    # close client
    uClient.close()
    # save the html data
    page_soup = soup(page_html, "html.parser") 
    # grabs each drop table
    tables = page_soup.findAll("table",{"class":"wikitable sortable dropstable"})
    if tables == []:
        print("Error, page has no drop table.")
        return "Error"
    else:
        for table in tables:
            alignLeft = table.findAll("td", {"style":"text-align:left;"})
            for AL in alignLeft:
                ##print(AL.a["title"])
                var = 1
        for table in tables:
            trs = table.findAll("tr", {"style":"text-align:center;"})
            for row in trs:
                data = row.findAll("td")
                itemDetails = []
                itemDetails.append(data[1].a.string.encode('utf-8').strip())
                itemDetails.append(data[2].string.encode('utf-8').strip())
                itemDetails.append(data[4].string.encode('utf-8').strip())
                # doing stuff to get drop % now
                drop_rate = data[3].find("small")
                if drop_rate:
                    # need to ignore anything besides just the string portion
                    unwanted = drop_rate.find('sup')
                    if unwanted:
                        unwanted.extract()
                    wanted = drop_rate.text.strip()
                    if "(" in wanted:
                        wanted = wanted[wanted.find("(")+1:wanted.find(")")]
                    itemDetails.append(wanted.encode('utf-8').strip())
                else:
                    unwanted = data[3].find('sup')
                    if unwanted:
                        unwanted.extract()
                    wanted = data[3].text.strip()
                    itemDetails.append(wanted.encode('utf-8').strip())
                returnList.append(itemDetails)
        return returnList

# runs when the client first connects
@client.event
async def on_ready():
    #print info to terminal
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #print connected servers
    for server in client.servers:
        print(server.name)
    print('------')

def calculateDrops(num_drops, dropList = []):
    results = dropList
    returnStuff = []
    always = []
    common = []
    uncommon = []
    rare = []
    very_rare = []
    drop_known = []
    _common = []
    _uncommon = []
    _rare = []
    _very_rare = []
    _drop_known = []
    for drop in results:
        # check if the loot quantity is a range
        # its drop[1] for each drop
        # if the search finds a '-' in quantity
        dash = '\u2013'.encode('utf-8').decode('utf-8')
        if (dash in drop[1].decode('utf-8')):
            hasNoted = 0
            if ("(noted)" in drop[1].decode('utf-8')):
                # remove the (noted) section, and add it back at the end
                hasNoted = 1
                drop[1] = drop[1].decode('utf-8').replace("(noted)", "").encode('utf-8')
            # generate a random number between the two values
            rangeQuantity = drop[1].decode('utf-8').split(dash)
            quanMinimum = rangeQuantity[0] # this could contain commas
            quanMaximum = rangeQuantity[1] # this could contain commas
            # get rid of commas when evaluating the our quantity
            ourQuan = random.randrange(eval(quanMinimum.replace(",", "")), eval(quanMaximum.replace(",", "")))
            # if the quantity isn't "Not sold" and has a "-"
            if (dash in drop[2].decode('utf-8')):
                rangePrice = drop[2].decode('utf-8').replace(',', "").split(dash)
                priceMinimum = rangePrice[0]
                # find the per-item price
                perItemPrice = int(priceMinimum) / int(quanMinimum)
                # set the price to our specific price
                drop[2] = format(int(perItemPrice*ourQuan), ",").encode('utf-8')
            # set the drop's quantity to our specific value
            drop[1] = format(int(ourQuan), ",").encode('utf-8')
            if hasNoted:
                drop[1] = drop[1] + " (noted)".encode('utf-8')
            # generate our specific quantity
        asc = drop[3].decode('utf-8').replace(",", "")
        if (asc == "Always"):
            always.append(drop)
        elif (asc == "Common"):
            _common.append(drop)
        elif (asc == "Uncommon"):
            _uncommon.append(drop)
        elif (asc == "Rare"):
            _rare.append(drop)
        elif (asc == "Very rare"):
            _very_rare.append(drop)
        else:
            _drop_known.append(drop)
    # we now have each drop sorted into its respective array
    # FOR KNOWN DROPRATES
    for drop in _drop_known:
        rate = drop[3].decode('utf-8').replace(',', "")
        pct_chance = float(eval(rate))
        rnd = random.random()
        # if we dont get the drop, remove it from list
        if (rnd < pct_chance):
            drop_known.append(drop)
    # FOR VERY RARE DROPS
    for drop in _very_rare:
        pct_chance = float(eval(rate_very_rare))
        rnd = random.random()
        if (rnd < pct_chance):
            very_rare.append(drop)
    # FOR RARE DROPS
    for drop in _rare:
        pct_chance = float(eval(rate_rare))
        rnd = random.random()
        if (rnd < pct_chance):
            rare.append(drop)
    # FOR UNCOMMON DROPS
    for drop in _uncommon:
        pct_chance = float(eval(rate_uncommon))
        rnd = random.random()
        if (rnd < pct_chance):
            uncommon.append(drop)
    # FOR COMMON DROPS
    for drop in _common:
        # shuffle common, grab something len(_common)/8 % of the time
        pct_chance = float(1.2/len(_common))
        rnd = random.random()
        if (rnd < pct_chance):
            common.append(drop)
    
    # the list of things to output
    output = []
    # add all of the drop arrays together
    finishedList = very_rare + rare + uncommon + common
    # if there's always drops
    if always:
        output = always
    if drop_known:
        # shuffle known drops
        random.shuffle(drop_known)
        output = output + drop_known[:1]
    random.shuffle(very_rare)
    random.shuffle(rare)
    random.shuffle(uncommon)
    random.shuffle(common)
    the_rest = very_rare + rare + uncommon + common
    output_finished = output + the_rest
    return(output_finished[:(len(always)+num_drops)])


# this runs when any message is sent in a connected channel
@client.event
async def on_message(message):
    if message.content.startswith('!help'):
        await client.send_message(message.channel, message.author.mention + helpm)
    if message.content.startswith('!slay'):
        var = 1
        name = message.content[6:]
        # mob_drop_amount defaults to 1 drop + always drops
        mob_drop_amount = 1
        # check if this monster is known to get multiple drops
        if name in list(multipleDropMobs.keys()):
            # then we should update the mob_drop_amount variable
            mob_drop_amount = multipleDropMobs.get(name)
        query = message.content[6:].replace(' ', '_')
        print("url queried : " + baseUrl + query)
        dropList_full = queryPage(baseUrl.lower() + query)
        if dropList_full == "Error":
            client.send_message(message.channel, "page not found")
            return
        em = discord.Embed(title = "**" + name.title() + "**")
        #em = discord.Embed(title = name, description = "Drop table is: ")
        # dropList format : [item name, quantity, value, rate]
        # make a function to handle this
        dropList = calculateDrops(mob_drop_amount, dropList_full)
        embed_field = ""
        for drop in dropList:
            if (drop[2].decode('utf-8') == "Not sold"):
                returnval = "\r\n"
            else:
                returnval = " worth " + drop[2].decode('utf-8') + "  gp\r\n"
            embed_field = embed_field + drop[0].decode('utf-8') + " x " + drop[1].decode('utf-8') + returnval
        em.add_field(name = "You received", value = embed_field, inline = "false")
        await client.send_message(message.channel, embed = em)
        #await client.send_message(message.channel, "__**" + name + "**__\r\n" + ''.join(dropList))

client.run(token)
#dropList = queryPage(baseUrl + "Bear")
#for item in dropList:
#    print(item)
