# define imports
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins
from shinyswatch import theme  # import shinyswatch to use bootswatch themes

# Define Dataframe
df = palmerpenguins.load_penguins()


# Page Title
ui.page_opts(title="Penguins dashboard", fillable=True, theme=theme.minty)


# Define Sidebar title
with ui.sidebar(title="Filter controls"):

    # input slider to define penguin mass
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)

    # input checkbox to select which specieis to display in outputs
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # Sidebar Links
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/andrea-shobe/cintel-07-cintel",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://andrea-shobe.github.io/cintel-07-cintel/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/andrea-shobe/cintel-07-cintel/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# -----------------------------------------
# Beginning of main page content
# -----------------------------------------
with ui.layout_column_wrap(fill=False):

    # Output of number of penguins based off of species selected
    with ui.value_box(showcase=icon_svg("earlybirds"),style="color:#56cc9d;"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    # output of average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="color: #fd7e14;"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # output of average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="color: #007bff;"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():

    # Bill Length and Depth scatterpolot based off of species selected-------------
    with ui.card(full_screen=True):
        ui.card_header(
            "Bill length and depth",
            style="font-weight: bold; color: #56cc9d;",
        )

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Filtered DataGrid based off of selected species----------------------------
    with ui.card(full_screen=True):
        ui.card_header(
            "Penguin data",
            style="font-weight: bold; color: #56cc9d;",
        )

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


# ui.include_css(app_dir / "styles.css")


# define reactive calc for filtered df
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
