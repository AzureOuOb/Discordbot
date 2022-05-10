from discord.ext import commands 
import discord
import json
from jsonpath_ng.ext import parse
from command import command
from crawler import crawler

with open('items.json', "r", encoding = "utf8") as file:
    data = json.load(file)

with open('comics.json', 'r', encoding = 'utf8') as file:
    comics = json.load(file)

# jsonpath_expression = parse('$.comics[?(@.name=~"海賊王")].url')

# for match in jsonpath_expression.find(comics):
#     print(match.value)

bot = commands.Bot(command_prefix='!')

command = command()

my_headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
        'Content-Type' : 'text/html'
}

@bot.event
async def on_ready():
    print("bot in ready")
    game = discord.Game('Hearthstone')
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.event
async def on_message(message):
    if (str(message.content).startswith('!') and message.author != bot.user):
        jsonpath_expression = parse('$.comics[?(@.name=~"' + message.content[1:] + '")].url')
        resultList = jsonpath_expression.find(comics)
        if len(resultList) > 0:
            url = resultList[0].value
            await message.channel.send(url)
        else:
            await message.channel.send('找不到這本漫畫87')
    elif (str(message.content).startswith('$') and message.author != bot.user):
        if message.content[1:] in 'comiclist':
            print('if')
            jsonpath_expression = parse('$.comics[*].name')
            resultList = jsonpath_expression.find(comics)
            comiclist = '```\r\n'
            for match in jsonpath_expression.find(comics):
                comiclist += match.value + '\r\n'
            comiclist += '```'
            await message.channel.send(comiclist)
        elif message.content[1:] in 'help':
            await message.channel.send(command.help)
    elif (str(message.content).startswith('#') and message.author != bot.user):
        jsonpath_expression = parse('$.comics[?(@.name=~"' + message.content[1:] + '")].url')
        resultList = jsonpath_expression.find(comics)
        if len(resultList) > 0:
            url = resultList[0].value
            crawl = crawler()
            resultList = crawl.crawlNew(url, my_headers)
            print(resultList)
            
bot.run(data['token']) 