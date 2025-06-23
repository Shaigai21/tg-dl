from .. import Bot, read_json_file

properties = read_json_file('config.json')
print(properties)
bot = Bot(properties["TOKEN"])
bot.run()
