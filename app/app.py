import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguins dashboard", fillable=True)


with ui.sidebar(title="Filter controls"): # Create a sidebar panel titled "Filter controls".
    # The following creates fields where the user can provide input.#
    ui.input_slider("mass", "Mass", 2000, 6000, 6000) # Add a slider input for "mass" with a range from 2000 to 6000, with an initial value set to 6000.
    ui.input_checkbox_group( # Add a group of checkboxes for selecting species.
        "species", # Input ID for the checkbox group, which is required for retrieving the selected values in the app.
        "Species", # The label that will be displayed above the checkboxes.
        ["Adelie", "Gentoo", "Chinstrap"], # Options for the checkboxes.
        selected=["Adelie", "Gentoo", "Chinstrap"], # The default selected options (in this case, all species are checked off by default).
    )
    ui.hr() # Creates a horizontal rule (line) in the app, adding a clear dividing line between the input and the output.
    ui.h6("Links") # Creates a header (h).
    ui.a( # Creates text with a link.
        "GitHub Source", # The text.
        href="https://github.com/denisecase/cintel-07-tdash", # The link attacked to the text.
        target="_blank", # The target argument determines how the link will open when the text is clicked. "_blank" opens the link in a new browser tab or window.
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
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


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin da")

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


#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
