# VTA Transit Analytics & Delay Prediction

## What Is This Project?

This is a tool that helps predict how late buses and light rail trains in San Jose will be based on real time traffic conditions and weather. It works by collecting data about where buses are right now, checking the weather, and using that information to predict delays. Think of it like a weather forecast, but for bus delays instead of rain.

## Why Does This Matter?

When you take the bus or light rail in San Jose, you want to know if it will be late. This project helps answer that question by:
  Watching bus and train locations in real time
  Checking current weather conditions
  Using smart predictions to estimate how many minutes late each bus will be
  Showing you all this information on an easy to use dashboard

## How Does It Work?

The project follows a simple flow:

1. **Collect Data**   Gathers real time location data from VTA buses and trains, plus weather information
2. **Process Data**   Cleans and organizes the data to prepare it for analysis
3. **Train Model**   Uses machine learning to learn patterns between weather, traffic, and delays
4. **Show Dashboard**   Displays predictions and insights on an interactive webpage

## What Do I Need?

Before you start, you'll need:

  **Python 3.7 or higher**   A programming language (likely already on your computer)
  **API Keys**   Two keys that let you access real time data:
    `VTA_API_KEY`   For bus and train location data (from 511.org)
    `WEATHER_API_KEY`   For weather information (from OpenWeatherMap)

## Setup Instructions

Follow these steps to get everything running:

### Step 1: Get Your API Keys

1. **VTA API Key** (511.org)
     Go to https://511.org/developers
     Sign up for a free account
     Request an API key for vehicle positions
     Copy the key

2. **Weather API Key** (OpenWeatherMap)
     Go to https://openweathermap.org/api
     Create a free account
     Generate an API key
     Copy the key

### Step 2: Set Up the Project

1. **Download and open the project folder** in your terminal/command prompt

2. **Create a `.env` file** (a configuration file with your API keys)
     In the project folder, create a new file called `.env`
     Add these two lines:
     ```
     VTA_API_KEY=your_vta_key_here
     WEATHER_API_KEY=your_weather_key_here
     ```
     Replace `your_vta_key_here` and `your_weather_key_here` with the actual keys you got

3. **Install required software**
     Run this command in your terminal:
     ```
     python3  m pip install   break system packages  q streamlit pandas numpy scikit learn joblib matplotlib requests python dotenv gtfs realtime bindings streamlit folium folium
     ```

### Step 3: Collect Data

Run the data collection script to start gathering real time information:

```bash
python3 src/collect_vta_data.py
```

You should see a message like: "Successfully fetched VTA data. 408 vehicles found."

### Step 4: Process the Data

Clean and organize the collected data:

```bash
python3 src/clean_merge_data.py
```

### Step 5: Train the Prediction Model

Create the smart system that will predict delays:

```bash
python3 src/train_model.py
```

### Step 6: View the Dashboard

Launch the interactive dashboard where you can see all the predictions and data:

```bash
streamlit run dashboard/app.py
```

A browser window should open automatically. If not, go to:
**http://localhost:8501**

## What Can You Do With the Dashboard?

Once the dashboard is running, you can:

  **View Overview**   See summary statistics about current buses and delays
  **Check Predictions**   Understand how accurate our delay predictions are
  **Explore Data**   Look at the raw data we collected
  **See Maps**   Visualize bus locations on a map of San Jose
  **Analyze Patterns**   Understand how weather affects delays

## Running Regular Updates

To keep the predictions fresh and accurate:

1. **Collect new data**   Run the collection script every hour or so:
   ```bash
   python3 src/collect_vta_data.py
   ```

2. **Retrain the model**   Once you have enough new data:
   ```bash
   python3 src/train_model.py
   ```

3. **Keep the dashboard running**   The dashboard will automatically show updated information

## Project Files Explained

  **`src/`**   The scripts that do all the work
    `collect_vta_data.py`   Gets bus location data
    `collect_weather_data.py`   Gets weather information
    `clean_merge_data.py`   Prepares data for training
    `train_model.py`   Creates the prediction system
    `evaluate_model.py`   Tests how accurate our predictions are

  **`dashboard/`**   The interactive webpage
    `app.py`   Main dashboard application
    `components/`   Different parts of the dashboard

  **`data/`**   Storage for collected information
    `raw/`   Original, unprocessed data
    `processed/`   Cleaned and ready to use data

  **`models/`**   Saved prediction systems
    `delay_predictor.pkl`   The trained model

  **`notebooks/`**   Detailed analysis documents (for advanced users)

## Troubleshooting

**"API key not found" error**
  Make sure your `.env` file is in the project folder
  Double check your API keys are correct (no extra spaces)

**"No data to save" message**
  Your API key might not be activated yet (wait a few minutes after creating it)
  Or the API service might be temporarily down
  Try again in a few minutes

**Dashboard won't open**
  Make sure you see "You can now view your Streamlit app" in the terminal
  Try manually going to http://localhost:8501

**Python not found**
  Windows: You might need to use `python` instead of `python3`
  Make sure Python is installed: Run `python   version` or `python3   version` in your terminal

## Next Steps

Once you have the basic setup working:

1. **Collect more data**   Gather data for a few days to improve predictions
2. **Experiment**   Try different times of day and weather conditions
3. **Improve**   Look at the notebooks to understand the analysis better
4. **Share**   Show the dashboard to friends who take VTA transit

## Questions?

If something isn't working or you're confused:
  Check the error messages carefully   they usually explain what went wrong
  Make sure all files are in the right folders
  Verify your API keys are correct and activated
  Try running the scripts one at a time to find where the issue is

## License

This project is provided as is for educational and analytical purposes.

   

**Last Updated:** November 2025

**Current Status:** Fully operational with real time data collection and prediction capabilities
