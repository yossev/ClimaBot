from dotenv import load_dotenv
import discord
import requests
import os

prefix = '?'
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
load_dotenv()

def run():

    # Embeds
    help_embed = discord.Embed(
        colour=discord.Colour.light_grey(),
        title="Help commands",
        description=f"`?whelp`: All commands\n`?weather city`: Get the Weather for the specific city\n",
    )
    help_embed.set_footer(text="@Synthatic on discord for any bugs")

    weather_embed = discord.Embed(
        colour=discord.Colour.dark_purple(),
        title=f"Weather in {location_name}, {country}",
        description=f"Temperature: {temperature}°C\n{description}"
    )
    weather_embed.set_thumbnail(url=f"http:{weather_img}")
    weather_embed.set_footer(text="prefix : ?")


    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith(prefix):
            args = message.content[len(prefix):].strip().split()
            command = args[0].lower()
        
            if command == 'weather':
                if len(args) < 2:
                    await message.channel.send('Please provide a location.')
                    return

                location = ' '.join(args[1:])  # after splitting the args we take the location arg
                API_URL = f"http://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q={location}"

                try:
                    res = requests.get(API_URL)
                    # Convert the call response to JSON Format
                    data = res.json()

                    if res.status_code != 200:
                        await message.channel.send("Error getting weather! please report any issues to @synthatic on discord!")
                        return

                    # Variables for the retrieved data
                    temperature = data['current']['temp_c']
                    weather_img = data['current']['condition']['icon']
                    location_name = data['location']['name']
                    country = data['location']['country']
                    description=data['current']['condition']['text']
                    

                    await message.channel.send(embed=weather_embed)
                except Exception as e:
                    print(f'Error fetching weather: {e}')
                    await message.channel.send('An error occurred while fetching weather data.')
            elif command == 'whelp':
                await message.channel.send(embed=help_embed)
    client.run(os.getenv('BOT_TOKEN'))

if __name__ == "__main__":
    run()
