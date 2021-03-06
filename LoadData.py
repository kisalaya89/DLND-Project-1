import pandas as pd

def loadData():
	data_path = 'Bike-Sharing-Dataset/hour.csv'

	rides = pd.read_csv(data_path)

	rides[:24 * 10].plot(x='dteday', y='cnt')

	dummy_fields = ['season', 'weathersit', 'mnth', 'hr', 'weekday']
	for each in dummy_fields:
		dummies = pd.get_dummies(rides[each], prefix=each, drop_first=False)
		rides = pd.concat([rides, dummies], axis=1)

	fields_to_drop = ['instant', 'dteday', 'season', 'weathersit',
	                  'weekday', 'atemp', 'mnth', 'workingday', 'hr']
	data = rides.drop(fields_to_drop, axis=1)

	quant_features = ['casual', 'registered', 'cnt', 'temp', 'hum', 'windspeed']
	# Store scalings in a dictionary so we can convert back later
	scaled_features = {}
	for each in quant_features:
		mean, std = data[each].mean(), data[each].std()
		scaled_features[each] = [mean, std]
		data.loc[:, each] = (data[each] - mean) / std

	# Save the last 21 days
	test_data = data[-21 * 24:]
	data = data[:-21 * 24]

	return data,test_data