import pickle
import numpy as np
from sklearnex import patch_sklearn,config_context
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
# Load data
data_dict = pickle.load(open(r"data_new.pickle", 'rb'))

data = data_dict['data']
labels = data_dict['labels']

# Ensure all data entries have the same length (e.g., 42 for 21 landmarks with x, y coordinates)
consistent_data = []
consistent_labels = []

for i, sample in enumerate(data):
    if len(sample) == 42:  # Expected number of features
        consistent_data.append(sample)
        consistent_labels.append(labels[i])

# Convert to NumPy arrays after filtering
data = np.asarray(consistent_data)
labels = np.asarray(consistent_labels)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Train the RandomForestClassifier
model = RandomForestClassifier()
model.fit(x_train, y_train)

# Make predictions and calculate accuracy
y_predict = model.predict(x_test)
score = accuracy_score(y_predict, y_test)
print('{}% of samples were classified correctly!'.format(score * 100))

# Save the trained model
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)