import pytest
import pandas as pd

field_df = pd.read_csv('sampled_field_df.csv')
weather_df = pd.read_csv('sampled_weather_df.csv')


def test_read_weather_DataFrame_shape():
  shape = weather_df.shape
  assert shape == (1843, 4)

def test_read_field_DataFrame_shape():
  shape = field_df.shape
  assert shape == (5654, 19)

def test_weather_DataFrame_columns():
  expected_columns = ['Weather_station_ID', 'Message', 'Measurement', 'Value']
  assert list(weather_df.columns) == expected_columns

def test_field_DataFrame_columns():
  expected_columns = ['Field_ID', 'Elevation', 'Latitude', 'Longitude', 'Location', 'Slope',
      'Rainfall', 'Min_temperature_C', 'Max_temperature_C', 'Ave_temps',
      'Soil_fertility', 'Soil_type', 'pH', 'Pollution_level', 'Plot_size',
      'Annual_yield', 'Crop_type', 'Standard_yield', 'Weather_station']
  assert list(field_df.columns) == expected_columns

def test_field_DataFrame_non_negative_elevation():
  count = field_df[field_df['Elevation'] < 0]['Elevation'].count()
  assert count == 0

def test_crop_types_are_valid():
  count = field_df['Crop_type'].isin(['cassava', 'tea', 'wheat', 'potato', 'banana', 'coffee', 'rice', 'maize']).count()
  assert count == 5654

def test_positive_rainfall_values():
  count = field_df[field_df['Rainfall'] < 0]['Rainfall'].count()
  assert count == 0
