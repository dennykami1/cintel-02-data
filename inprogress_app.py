from shiny import App, Inputs, Outputs, Session, ui, render
import matplotlib.pyplot as plt
import numpy as np
import shinyswatch
import plotly.express as px
import palmerpenguins  # This Package Provides the Palmer Penguin Dataset

# Load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style(""" 
            .title-box {
                background-color: #A4C3B2;
                border: 1px solid #ccc;
                padding: 10px;
                text-align: center;
                font-family: 'Arial', sans-serif;
                font-size: 20px;
                color: #000000;
                margin-bottom: 20px;
                border-radius: 9px;
            }
        """)
    ),
    ui.div(
        ui.panel_title("Kami's take on the PyShiny App with Palmer Penguins Histograms"),
        class_="title-box"
    ),
    ui.page_fillable(
        ui.card(
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_slider("selected_number_of_bins1", "Number of Bins (Flipper Length)", 1, 50, 20),  # Adjusted range for better binning
                    ui.tags.hr(),
                    ui.input_checkbox_group(
                        "multi_choice_input",
                        "Select One or More Penguin Species to Display:", 
                        choices=["Adelie", "Chinstrap", "Gentoo"],  # Checkbox group for species
                        selected=["Adelie", "Chinstrap", "Gentoo"],
                        inline=False,
                    ),
                    bg="#F6FFF8"
                ),
                ui.output_plot("penguin_flipper_histogram")
            ),
            ui.card_header("Histogram of Flipper Length from Palmer Penguins Dataset"),
        ),
        ui.card(
            ui.layout_sidebar(
                ui.sidebar(
                    ui.input_slider("selected_number_of_bins2", "Number of Bins (Body Mass)", 1, 50, 20),  # Adjusted range for better binning
                    bg="#F6FFF8"
                ),
                ui.output_plot("penguin_body_mass_histogram")
            ),
            ui.card_header("Histogram of Body Mass from Palmer Penguins Dataset"),
        )
    ),
    theme=shinyswatch.theme.minty
)

def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.plot(alt="A histogram of flipper length from Palmer Penguins dataset")
    def penguin_flipper_histogram():
        # Clear previous plot
        plt.clf()  # Clear the current figure

        # Filter data based on selected species
        selected_species = input.multi_choice_input()
        filtered_data = penguins_df[penguins_df['species'].isin(selected_species)] if selected_species else penguins_df

        # Set unique colors for each species
        colors = {
            "Adelie": "#6B9080",
            "Chinstrap": "#D95B43",
            "Gentoo": "#F1C40F"
        }

        # Plot histogram for each selected species
        for species in selected_species:
            species_data = filtered_data[filtered_data['species'] == species]['flipper_length_mm'].dropna()
            plt.hist(species_data, bins=input.selected_number_of_bins1(), 
                     density=True, alpha=0.5, color=colors[species], 
                     label=species)  # Adjust alpha for transparency
        
        plt.xlabel("Flipper Length (mm)")
        plt.ylabel("Density")
        plt.title("Histogram of Flipper Length from Palmer Penguins Dataset")
        plt.legend(title="Penguin Species")
        
    @output
    @render.plot(alt="A histogram of body mass from Palmer Penguins dataset")
    def penguin_body_mass_histogram():
        # Clear previous plot
        plt.clf()  # Clear the current figure

        # Filter out rows based on selected species
        selected_species = input.multi_choice_input()
        filtered_data = penguins_df[penguins_df['species'].isin(selected_species)] if selected_species else penguins_df
        
        # Plot histogram for body mass
        plt.hist(filtered_data['body_mass_g'].dropna(), 
                 bins=input.selected_number_of_bins2(), density=True, 
                 color="#D95B43")  # Using a single color for the body mass histogram
        plt.xlabel("Body Mass (g)")
        plt.ylabel("Density")
        plt.title("Histogram of Body Mass from Palmer Penguins Dataset")

app = App(app_ui, server)
