Basic climate analysis and data exploration of a climate database using Python and SQLAlchemy

### Precipitation Analysis

Retrieved the last 12 months of precipitation data, loaded the query results into a Pandas DataFrame, sorted the DataFrame values,
and plotted the results. Then printed the summary statistics for the precipitation data.

### Station Analysis

Designed a query to calculate the total number of stations and  find the most active stations.
Designed a query to retrieve the last 12 months of temperature observation data (TOBS).

### Climate App

Flask API based on the queries that I developed developed to: 
Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

