import discord
from engine import top_stories,format_top_story,get_tag_stories,get_year_stories

from engine import (
    random_story,
    format_story_card,
    format_top_story,
    get_full_story,
    split_story
)

class StoryPaginator(discord.ui.View):

    def __init__(self, title, pages):
        super().__init__(timeout=300)

        self.title = title
        self.pages = pages
        self.current = 0

    def get_content(self):

        return (
            f"📖 **{self.title}**\n\n"
            f"Page {self.current + 1}/{len(self.pages)}\n\n"
            f"{self.pages[self.current]}"
        )

    @discord.ui.button(label="⬅ Previous")
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if self.current > 0:
            self.current -= 1

        await interaction.response.edit_message(
            content=self.get_content(),
            view=self
        )

    @discord.ui.button(label="➡ Next")
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if self.current < len(self.pages) - 1:
            self.current += 1

        await interaction.response.edit_message(
            content=self.get_content(),
            view=self
        )

    @discord.ui.button(label="❌ Close")
    async def close(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.message.delete()


class RandomStoryView(discord.ui.View):

    def __init__(self, story):
        super().__init__(timeout=300)

        self.story = story
        self.story_id = story["id"]

    @discord.ui.button(label="📖 Read Story")
    async def read_story(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        full_story = get_full_story(
            self.story_id
        )

        if not full_story:
            await interaction.response.send_message(
                "Story not found.",
                ephemeral=True
            )
            return

        pages = split_story(
            full_story["story"]
        )

        view = StoryPaginator(
            full_story["title"],
            pages
        )

        await interaction.response.edit_message(
            content=view.get_content(),
            view=view
        )

    @discord.ui.button(label="🎲 Another Random")
    async def another_random(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        story = random_story()

        self.story = story
        self.story_id = story["id"]

        await interaction.response.edit_message(
            content=format_story_card(story),
            view=self
        )

    @discord.ui.button(label="❌ Close")
    async def close(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.message.delete()

class TopStoriesView(discord.ui.View):

    def __init__(self, stories):
        super().__init__(timeout=300)

        self.stories = stories
        self.current = 0

    def current_story(self):
        return self.stories[self.current]
  	
    def content(self):
        story = self.current_story()

        return format_top_story(
            story,
            self.current + 1
        )

    @discord.ui.button(label="⬅ Previous")
    async def previous(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.current > 0:
            self.current -= 1

        await interaction.response.edit_message(
            content=self.content(),
            view=self
        )

    @discord.ui.button(label="➡ Next")
    async def next(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        if self.current < len(self.stories) - 1:
            self.current += 1

        await interaction.response.edit_message(
            content=self.content(),
            view=self
        )

    @discord.ui.button(label="📖 Read Story")
    async def read_story(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        story = self.current_story()

        full_story = get_full_story(
            story["id"]
        )

        pages = split_story(
            full_story["story"]
        )

        view = StoryPaginator(
            full_story["title"],
            pages
        )

        await interaction.response.edit_message(
            content=view.get_content(),
            view=view
        )

    @discord.ui.button(label="❌ Close")
    async def close(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.message.delete()


class TagBrowserView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

    async def show_tag(
        self,
        interaction,
        tag
    ):

        stories = sorted(
            get_tag_stories(tag),
            key=lambda x: x["score"],
            reverse=True
        )

        if not stories:
            await interaction.response.send_message(
                f"No stories found for {tag}.",
                ephemeral=True
            )
            return

        view = TopStoriesView(
            stories[:100]
        )

        await interaction.response.edit_message(
            content=view.content(),
            view=view
        )

    @discord.ui.button(label="Nonfiction", row=0)
    async def nonfiction(self, interaction, button):
        await self.show_tag(interaction, "Nonfiction")

    @discord.ui.button(label="Fiction", row=0)
    async def fiction(self, interaction, button):
        await self.show_tag(interaction, "Fiction")

    @discord.ui.button(label="Cheating", row=0)
    async def cheating(self, interaction, button):
        await self.show_tag(interaction, "Cheating")

    @discord.ui.button(label="Incest", row=0)
    async def incest(self, interaction, button):
        await self.show_tag(interaction, "Incest")

    @discord.ui.button(label="Oral", row=0)
    async def oral(self, interaction, button):
        await self.show_tag(interaction, "Oral")

    @discord.ui.button(label="Quickie", row=1)
    async def quickie(self, interaction, button):
        await self.show_tag(interaction, "Quickie")

    @discord.ui.button(label="Milf", row=1)
    async def milf(self, interaction, button):
        await self.show_tag(interaction, "Milf")

    @discord.ui.button(label="Anal", row=1)
    async def anal(self, interaction, button):
        await self.show_tag(interaction, "Anal")

    @discord.ui.button(label="Masturbation", row=1)
    async def masturbation(self, interaction, button):
        await self.show_tag(interaction, "Masturbation")

    @discord.ui.button(label="Fetish", row=1)
    async def fetish(self, interaction, button):
        await self.show_tag(interaction, "Fetish")

    @discord.ui.button(label="Bdsm", row=2)
    async def bdsm(self, interaction, button):
        await self.show_tag(interaction, "Bdsm")

    @discord.ui.button(label="Vanilla", row=2)
    async def vanilla(self, interaction, button):
        await self.show_tag(interaction, "Vanilla")

    @discord.ui.button(label="Lesbian", row=2)
    async def lesbian(self, interaction, button):
        await self.show_tag(interaction, "Lesbian")

    @discord.ui.button(label="Cock Tease", row=2)
    async def cock_tease(self, interaction, button):
        await self.show_tag(interaction, "Cock Tease")

    @discord.ui.button(label="Gay", row=2)
    async def gay(self, interaction, button):
        await self.show_tag(interaction, "Gay")

    @discord.ui.button(label="Femdom", row=3)
    async def femdom(self, interaction, button):
        await self.show_tag(interaction, "Femdom")

    @discord.ui.button(label="Cougar", row=3)
    async def cougar(self, interaction, button):
        await self.show_tag(interaction, "Cougar")

    @discord.ui.button(label="Roommate", row=3)
    async def roommate(self, interaction, button):
        await self.show_tag(interaction, "Roommate")

    @discord.ui.button(label="School", row=3)
    async def school(self, interaction, button):
        await self.show_tag(interaction, "School")

    @discord.ui.button(label="Handjob", row=3)
    async def handjob(self, interaction, button):
        await self.show_tag(interaction, "Handjob")

    @discord.ui.button(label="❌ Close", row=4)
    async def close(self, interaction, button):
        await interaction.message.delete()

class YearBrowserView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=300)

    async def show_year(
        self,
        interaction,
        year
    ):

        stories = sorted(
            get_year_stories(year),
            key=lambda x: x["score"],
            reverse=True
        )

        if not stories:
            await interaction.response.send_message(
                f"No stories found for {year}.",
                ephemeral=True
            )
            return

        view = TopStoriesView(
            stories[:100]
        )

        await interaction.response.edit_message(
            content=view.content(),
            view=view
        )

    @discord.ui.button(label="2010", row=0)
    async def y2010(self, interaction, button):
        await self.show_year(interaction, 2010)

    @discord.ui.button(label="2011", row=0)
    async def y2011(self, interaction, button):
        await self.show_year(interaction, 2011)

    @discord.ui.button(label="2012", row=0)
    async def y2012(self, interaction, button):
        await self.show_year(interaction, 2012)

    @discord.ui.button(label="2013", row=0)
    async def y2013(self, interaction, button):
        await self.show_year(interaction, 2013)

    @discord.ui.button(label="2014", row=0)
    async def y2014(self, interaction, button):
        await self.show_year(interaction, 2014)

    @discord.ui.button(label="2015", row=1)
    async def y2015(self, interaction, button):
        await self.show_year(interaction, 2015)

    @discord.ui.button(label="2016", row=1)
    async def y2016(self, interaction, button):
        await self.show_year(interaction, 2016)

    @discord.ui.button(label="2017", row=1)
    async def y2017(self, interaction, button):
        await self.show_year(interaction, 2017)

    @discord.ui.button(label="2018", row=1)
    async def y2018(self, interaction, button):
        await self.show_year(interaction, 2018)

    @discord.ui.button(label="2019", row=1)
    async def y2019(self, interaction, button):
        await self.show_year(interaction, 2019)

    @discord.ui.button(label="2020", row=2)
    async def y2020(self, interaction, button):
        await self.show_year(interaction, 2020)

    @discord.ui.button(label="2021", row=2)
    async def y2021(self, interaction, button):
        await self.show_year(interaction, 2021)

    @discord.ui.button(label="2022", row=2)
    async def y2022(self, interaction, button):
        await self.show_year(interaction, 2022)

    @discord.ui.button(label="2023", row=2)
    async def y2023(self, interaction, button):
        await self.show_year(interaction, 2023)

    @discord.ui.button(label="2024", row=2)
    async def y2024(self, interaction, button):
        await self.show_year(interaction, 2024)

    @discord.ui.button(label="❌ Close", row=4)
    async def close(self, interaction, button):
        await interaction.message.delete()
