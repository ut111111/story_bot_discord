import os
import discord

from story_view import (
    RandomStoryView,
    StoryPaginator,
    TopStoriesView,
    TagBrowserView,
    YearBrowserView
)

from dotenv import load_dotenv
from discord.ext import commands
from story_view import RandomStoryView,StoryPaginator


from engine import (
    random_story,
    get_full_story,
    split_story,
    format_story_card,
    top_stories,
    semantic_search,
    get_stats
)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def random(ctx):

    story = random_story()

    await ctx.send(
        format_story_card(story),
        view=RandomStoryView(story)
    )

@bot.command()
async def top(ctx):

    stories = top_stories(100)

    view = TopStoriesView(stories)

    await ctx.send(
        view.content(),
        view=view
    )

@bot.command()
async def tags(ctx):

    await ctx.send(
        "📂 Browse Stories by Tag",
        view=TagBrowserView()
    )

@bot.command()
async def years(ctx):

    await ctx.send(
        "📅 Browse Stories by Year",
        view=YearBrowserView()
    )

@bot.command()
async def search(ctx, *, query):

    results = semantic_search(
        query,
        limit=100
    )

    if not results:

        await ctx.send(
            "No results found."
        )

        return

    view = TopStoriesView(
        results
    )

    await ctx.send(
        f"🔎 Results for: {query}\n\n"
        f"{view.content()}",
        view=view
    )

@bot.command()
async def index(ctx):

    await ctx.send(
        "📚 **Story Explorer**\n\n"
        "📖 Stories: 228,274\n"
        "🏷️ Tags: 44\n"
        "📅 Years: 2010–2025\n\n"
        "🎲 !random\n"
        "🏆 !top\n"
        "📂 !tags\n"
        "📅 !years\n"
        "🔎 !search <query>\n\n"
	"📊 **!stats** - Dataset statistics\n\n"
        "Use buttons to browse and read stories."
    )
@bot.command()
async def stats(ctx):

    stats = get_stats()

    tags_text = "\n".join(
        f"{i+1}. {tag} ({count:,})"
        for i, (tag, count)
        in enumerate(stats["top_tags"])
    )

    await ctx.send(
        f"📚 **Story Explorer Statistics**\n\n"
        f"📖 Total Stories: {stats['total_stories']:,}\n"
        f"🏷️ Total Tags: {stats['total_tags']}\n"
        f"📅 Years Covered: "
        f"{stats['first_year']}–{stats['last_year']}\n\n"
        f"📝 Total Words: "
        f"{stats['total_words']:,}\n\n"
        f"📏 Longest Story:\n"
        f"{stats['longest_story']['word_count']:,} words\n\n"
        f"⭐ Highest Score:\n"
        f"{stats['highest_score']['score']:,}\n\n"
        f"🔥 **Top Tags**\n"
        f"{tags_text}"
    )

bot.run(TOKEN)
