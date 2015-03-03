# FlightDelays

This is a project to predict the likelyhood that a flight will be delayed. 
The flight models are then chained together to make a model that can predict
the likelyhood that a connection will be missed.

Without the training data (much too large to store on github)
and API Keys for the Weather Underground and FlightStats.com this isn't particularly
usable.

The "Predictor" directory contains the code to generate my airport models (Gradient Boosting Machine)
and the "Frontend" directory contains my flask frontend.
