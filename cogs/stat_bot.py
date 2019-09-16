import requests
from discord.ext import commands
import discord
import json
import datetime
import pytz
import math

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
husker_schedule = []
huskerbot_footer="Generated by HuskerBot"
statFullName = [
    dict(stat="possessionTime", longName="Time of Possession", homeStat="", awayStat=""),
    dict(stat="totalPenaltiesYards", longName="Total Penalties Yards", homeStat="", awayStat=""),
    dict(stat="completionAttempts", longName="Completion Attempts", homeStat="", awayStat=""),
    dict(stat="netPassingYards", longName="Net Passing Yards", homeStat="", awayStat=""),
    dict(stat="passingTDs", longName="Passing TDs", homeStat="", awayStat=""),
    dict(stat="rushingAttempts", longName="Rushing Attempts", homeStat="", awayStat=""),
    dict(stat="rushingYards", longName="Rushing Yards", homeStat="", awayStat=""),
    dict(stat="rushingTDs", longName="Rushing TDs", homeStat="", awayStat=""),
    dict(stat="yardsPerPass", longName="Yards Per Pass", homeStat="", awayStat=""),
    dict(stat="yardsPerRushAttempt", longName="Yards Per Rush Attempt", homeStat="", awayStat=""),
    dict(stat="totalYards", longName="Total Yards", homeStat="", awayStat=""),
    dict(stat="tacklesForLoss", longName="Tackles For Loss", homeStat="", awayStat=""),
    dict(stat="sacks", longName="Sacks", homeStat="", awayStat=""),
    dict(stat="qbHurries", longName="QB Hurries", homeStat="", awayStat=""),
    dict(stat="passesDeflected", longName="Passes Deflected", homeStat="", awayStat=""),
    dict(stat="passesIntercepted", longName="Passes Intercepted", homeStat="", awayStat=""),
    dict(stat="defensiveTDs", longName="Defensive TDs", homeStat="", awayStat=""),
    dict(stat="tackles", longName="Tackles", homeStat="", awayStat=""),
    dict(stat="fieldGoals", longName="Field Goals", homeStat="", awayStat=""),
    dict(stat="extraPoints", longName="Extra Points", homeStat="", awayStat=""),
    dict(stat="fieldGoalPct", longName="Field Goal Pct", homeStat="", awayStat=""),
    dict(stat="kickingPoints", longName="Kicking Points", homeStat="", awayStat=""),
    dict(stat="kickReturns", longName="Kick Returns", homeStat="", awayStat=""),
    dict(stat="kickReturnYards", longName="Kick Return Yards", homeStat="", awayStat=""),
    dict(stat="kickReturnTDs", longName="Kick Return TDs", homeStat="", awayStat=""),
    dict(stat="puntReturns", longName="Punt Returns", homeStat="", awayStat=""),
    dict(stat="puntReturnYards", longName="Punt Return Yards", homeStat="", awayStat=""),
    dict(stat="puntReturnTDs", longName="Punt Return TDs", homeStat="", awayStat=""),
    dict(stat="fumblesLost", longName="Fumbles Lost", homeStat="", awayStat=""),
    dict(stat="fumblesRecovered", longName="Fumbles Recovered", homeStat="", awayStat=""),
    dict(stat="totalFumbles", longName="Total Fumbles", homeStat="", awayStat=""),
    dict(stat="interceptions", longName="Interceptions", homeStat="", awayStat=""),
    dict(stat="interceptionYards", longName="Interception Yards", homeStat="", awayStat=""),
    dict(stat="interceptionTDs", longName="Interception TDs", homeStat="", awayStat=""),
    dict(stat="turnovers", longName="Turnovers", homeStat="", awayStat=""),
    dict(stat="firstDowns", longName="First Downs", homeStat="", awayStat=""),
    dict(stat="thirdDownEff", longName="Third Down Eff", homeStat="", awayStat=""),
    dict(stat="fourthDownEff", longName="Fourth Down Eff", homeStat="", awayStat="")
]


class StatBot(commands.Cog, name="CFB Stats"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["sznstats"])
    async def seasonstats(self, ctx, year=2019):
        """ Returns current season stats """

        msg = await ctx.send("Loading...")
        url = "https://api.collegefootballdata.com/stats/season?year={}&team=nebraska".format(year)

        try:
            r = requests.get(url)
            seasonstats_json = r.json()
        except:
            await ctx.send("An error occurred retrieving poll data.")
            return

        dump = True
        if dump:
            with open("seasonstats.json", "w") as fp:
                json.dump(seasonstats_json, fp, sort_keys=True, indent=4)
            fp.close()

        message_string = "```\n{} Season Stats for Nebraska\n".format(year)
        seasonstats_json = sorted(seasonstats_json, key=lambda i: i["statName"])

        for stat in seasonstats_json:
            if stat["statName"] == "possessionTime":
                message_string += "{:<22} : {}\n".format(stat["statName"], datetime.timedelta(seconds=math.floor(stat["statValue"] / 60)))
            else:
                message_string += "{:<22} : {}\n".format(stat["statName"], stat["statValue"])

        message_string += "\n```"
        await msg.edit(content=message_string)

    @commands.command(aliases=["mu",])
    async def matchup(self, ctx, *, team):
        """ Shows matchup history between Nebraska and another team. """
        url = "https://api.collegefootballdata.com/teams/matchup?team1=nebraska&team2={}".format(team)

        try:
            r = requests.get(url)
            matchup_json = r.json()
        except:
            await ctx.send("An error occurred retrieving poll data.")
            return

        if not matchup_json["games"]:
            await ctx.send("No games found between Nebraska and {}!".format(team))
            return

        dump = True
        if dump:
            with open("matchup_json.json", "w") as fp:
                json.dump(matchup_json, fp, sort_keys=True, indent=4)
            fp.close()

        msg = await ctx.send("Loading...")

        embed = discord.Embed(title="Match up history between Nebraska and {}".format(team.capitalize()), color=0xFF0000)
        embed.set_thumbnail(url="https://i.imgur.com/aaqkw35.png")

        embed.add_field(name="{} Wins".format(matchup_json["team1"]), value=matchup_json["team1Wins"], inline=False)
        embed.add_field(name="{} Wins".format(matchup_json["team2"]), value=matchup_json["team2Wins"], inline=False)
        if matchup_json["ties"]:
            embed.add_field(name="Ties", value=matchup_json["ties"], inline=False)

        gameHistLen = len(matchup_json["games"])
        gameHistLen -= 1

        game_datetime_raw = datetime.datetime.strptime(matchup_json["games"][gameHistLen]["date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        game_datetime_utc = pytz.utc.localize(game_datetime_raw)
        game_datetime_cst = game_datetime_utc.astimezone(pytz.timezone("America/Chicago"))

        embed.add_field(name="Most Recent Match Up", value="Date: {}\nLocation: {}\n{} : {} - {} : {}\n".format(
            str(game_datetime_cst)[:-15],
            matchup_json["games"][gameHistLen]["venue"],
            matchup_json["games"][gameHistLen]["homeTeam"],
            matchup_json["games"][gameHistLen]["homeScore"],
            matchup_json["games"][gameHistLen]["awayScore"],
            matchup_json["games"][gameHistLen]["awayTeam"]))
        await msg.edit(content="", embed=embed)

    @commands.command(aliases=["polls",])
    async def poll(self, ctx, year=2019, week=None, seasonType="regular"):
        """ Returns current Top 25 ranking from the Coach's Poll, AP Poll, and College Football Playoff ranking.
        Usage is: `$poll [year] [week] [seasonType=regular]` """

        url = "https://api.collegefootballdata.com/rankings?year={}".format(year)

        if seasonType == "regular":
            url = url + "&seasonType=regular"
        elif seasonType == "postseason":
            url = url + "&seasonType=postseason"
        else:
            await ctx.send("The season type is either `regular` or `postseason`. Try again!")
            return

        if week:
            url = url + "&week={}".format(week)

        try:
            r = requests.get(url)
            poll_json = r.json()
        except:
            await ctx.send("An error occurred retrieving poll data.")
            return

        dump = True
        if dump:
            with open("cfb_polls.json", "w") as fp:
                json.dump(poll_json, fp, sort_keys=True, indent=4)
            fp.close()

        try:
            embed = discord.Embed(title="{} {} Season Week {} Poll".format(poll_json[0]['season'], str(poll_json[0]['seasonType']).capitalize(), poll_json[0]['week']), color=0xFF0000)
        except IndexError:
            await ctx.send("Invalid week. Try again!")
            return

        ap_poll_raw = poll_json[0]['polls'][0]['ranks']
        last_rank = 1

        x = 0
        y = 0
        while x < len(ap_poll_raw):
            while y < len(ap_poll_raw):
                if ap_poll_raw[y]['rank'] == last_rank:
                    if ap_poll_raw[y]['firstPlaceVotes']:
                        embed.add_field(name="#{} {}".format(ap_poll_raw[y]['rank'], ap_poll_raw[y]['school']), value="{}\nPoints: {}\nFirst Place Votes: {}".format(ap_poll_raw[y]['conference'], ap_poll_raw[y]['points'], ap_poll_raw[y]['firstPlaceVotes']))
                    else:
                        embed.add_field(name="#{} {}".format(ap_poll_raw[y]['rank'], ap_poll_raw[y]['school']), value="{}\nPoints: {}".format(ap_poll_raw[y]['conference'], ap_poll_raw[y]['points']))
                    last_rank += 1
                    y = 0
                    break
                y += 1
            x += 1

        await ctx.send(embed=embed)

    @commands.command(aliases=["bs",])
    async def boxscore(self, ctx, year=None, week=None, *, team="Nebraska"):
        """ Returns the box score of the searched for game. """

        edit_msg = await ctx.send("Loading...")

        if not year or not week:
            await edit_msg.edit(content="A year and week are required.")
            return

        if int(year) < 2004:
            await edit_msg.edit(content="Data is not available prior to 2004.")
            return

        if not type(int(week)) is int:
            await edit_msg.edit(content="You must enter a numerical week.")
            return

        if team == "Nebraska":
            url = "https://api.collegefootballdata.com/games/teams?year={}&week={}&seasonType=regular&team=nebraska".format(year, week)
        else:
            url = "https://api.collegefootballdata.com/games/teams?year={}&week={}&seasonType=regular&team={}".format(year, week, team)

        try:
            r = requests.get(url)
            boxscore_json = r.json() # Actually imports a list
        except:
            await edit_msg.edit(content="An error occurred retrieving boxscore data.")
            return

        if not boxscore_json:
            await edit_msg.edit(content="This was a bye week. Try again.")
            return

        dump = True
        if dump:
            with open("boxscore_json.json", "w") as fp:
                json.dump(boxscore_json, fp, sort_keys=True, indent=4)
            fp.close()

        global statFullName

        home_stats = boxscore_json[0]["teams"][0]
        away_stats = boxscore_json[0]["teams"][1]

        boxscoreString = "```\nBoxscore for: {} ({}) vs {} ({})\n\n".format(home_stats["school"], home_stats["points"], away_stats["school"], away_stats["points"])

        for stats in statFullName:
            for homeStat in home_stats["stats"]:
                if stats["stat"] == homeStat["category"]:
                    stats.update(homeStat=homeStat["stat"])
                    break

            for awayStat in away_stats["stats"]:
                if stats["stat"] == awayStat["category"]:
                    stats.update(awayStat=awayStat["stat"])
                    break

            if not (stats["homeStat"] == "" and stats["awayStat"] == ""):
                boxscoreString += "{:>23}: {:<7} | {:>7}\n".format(stats["longName"], stats["homeStat"], stats["awayStat"])

        boxscoreString += "\n```"

        await edit_msg.edit(content=boxscoreString)


def setup(bot):
    bot.add_cog(StatBot(bot))