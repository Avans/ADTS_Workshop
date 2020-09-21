# Excercises for week 5 and 6 <!-- omit in toc -->

In this workshop you will learn how to retrieve your data and show it in a visualization environment and you will get your data in a python notebook in Google Colaboratory.
You will both use your Google Sheet and your No SQL database from the previous assignment.

You will:
 * Create Google Data Studio Dashboard using your Google Sheet
 * Link your NO SQL database to your Google Data Studio Dashboard
 * Create a Google Colaboratory python script
 * Link your data from both your Google Sheet and your NO SQL database to your python script.

**Table of contents**
- [1. Google Data Studio](#1-google-data-studio)
  - [1.1. Data sources](#11-data-sources)
  - [1.2. Adding a chart](#12-adding-a-chart)
  - [1.3. Filtering](#13-filtering)
    - [1.3.1. Report settings](#131-report-settings)
  - [1.4. Sharing and notifications](#14-sharing-and-notifications)
- [2. Using your RestDB NO-SQL data](#2-using-your-restdb-no-sql-data)
  - [2.1. Using your RestDB data](#21-using-your-restdb-data)
- [3. Google Colaboratory](#3-google-colaboratory)

# 1. Google Data Studio

We are going to create a dashboard using Google Data Studio. Google offers this service for free and it is a rich environment in which we can create dashboards using cloud services (Software as a Service). Google Data Studio integrates with all other Google products and various integrations for other providers are offered so that you can connect to your data.

We are going to create a simple report using our COVID-19 data.

* Start by navigating to https://datastudio.google.com/
* Create a new report by clicking on Blank Report.
* You will be prompted to add data to you report and we will do that by choosing Google Sheets.
  * Find your Google sheet containing your Things Network data.
  * Let the defaults, your sheet has headers in the first row and hidden and filtered cells can be included as we don't have them.
* As with all Google products, change the title of your document in the top left of the screen so that you will be able to find it again.
* You will see that a table has been added to a sheet of 'paper'. This is your report.
* On the right, you can configure your table. Start by selecting 'Active', 'Confirmed', 'Recovered' and 'Deaths' as metrics. You see that they are added as SUM, but our data is repeated over each row, so we need to select MAX in order to now how much people are affected. Change this by clicking on them and selecting MAX.
* Of course, the app_id is not the dimension we are interested in. Lets remove that and select 'dev_id' as the dimension.
* Click the blue View button in the top right and see that you have created your first dashboard item with a table on which you can sort the columns.

## 1.1. Data sources

In the following image you can see the data parts that you have in a Dashboard. The data set is the Google Sheet you have got, the connector you specified by selecting the Google Sheet connection to your sheet. The report we created and now we are going to enrich the Data Source by having better region names.
![Types of sources](https://www.holistics.io/blog/content/images/2019/01/gds-concepts.png)

* In the top menu, go to Resource -> Manage Added Data Sources.
* Click on edit on your data source.
* Again, in the top left rename your data source to 'The Things Network Google Sheet Source' for example.
* You can see that all fields can be metrics or dimensions with their default behaviour.
  * Remove (hide) the fields that aren't important such as payload_fields
  * Set the aggregation to the right values
  * Add descriptions if desired.
* Now we want a position field, so we add them by clicking on the Add A Field button
  * Name the field Geolocation
  * Set the following as the formula:
  ```
  CONCAT(lat, ",", long)
  ```
  * Go back and set the type of this field to Geo -> Latitude, Longitude. We will use it later.
* We also want two fields: Country and Region. These should be derived from dev_id. Can you do that? Tip: For country we can use the regex (for regions: replace the 0 with a 1). The regex splits a string based on underscores.
  ```
  ^(?:[^\\_]*\\_){0}([^\\_]*)
  ```

You can imagine that, with self service dashboarding, you need to do a lot of work here. Prepare your data source to be as helpfull as possible so that no incorrect conclusions will be made. At this point we created an embedded resource, but you can choose to make it reusable so that it is no longer embedded in this dashboard. Users will be able to choose your data source when creating new dashboards so that they no longer have to map their data set themselves anymore.
You typically would want to offer a set of data sources which you have preprocessed so that users can select from these and be self sufficient.
!['Make reusable](Images/MakeReusable.png)

## 1.2. Adding a chart
We have created a Geo field and called it Location. Lets use that in our dashboard by adding a Bubble Map.
* Click on add a chart and choose for bubble map.
* See that your data source is selected automatically and that your dimension is set to your geolocation.
* You should see bubbles on the map corresponding to your device locations.
* If you select 'active' as a metric, your bubbles will be of size corresponding to the number of active COVID-19 cases.
* Click view now, your report will be shown as you created it, and note that it does that quickly. Most dashboarding tools use caching to be efficient.
In the following picture you can see how those caches work. There is a query cache on each chart, therefore filters are applied on the data source and then charts are rendered and cached.
![Report caching](https://www.holistics.io/blog/content/images/2019/01/gds-filter-mechanism.png)

## 1.3. Filtering
There are two types of filtering that could be interesting. Filter controls and filters in charts/tables that affect other charts and tables. Lets go and see what we would like to do.
* First, add a third chart, a vertical bar chart for example. As dimension we can use 'Country' as a metric choose 'active'.
* Enable drill down and select 'Region'.
* View the report. If you select China and right click you can select drill down to see all of the regions.
* Now we want to have a filter. Add a control, for example a drop down list that uses Country as a filter.
* When you view your report again, you see that all of the report elements interact with this filter.

A second option is filtering within the charts/tables themselves. We can do that, by taking the following steps:
* Select your vertical bar chart.
* In the data tab, scroll all the way to the bottom and check Interactions -> Apply filter.
* The chart now functions as a filter. Click on view again and see what happens if you select an item.

Typically you want those items to interact with each other, but for all of the items this has to be enabled so be aware to do that if you'd prefer this option.

### 1.3.1. Report settings
Be aware that your report can have settings that overrule certain settings in your charts. If you go to file -> Report settings, you can see that your primary data source can be set and a date range dimension can be selected. If the date range dimension is set, you see that the Default Date Range can be set to Auto and Custom. If you don't see any data, it could be due to this setting. Our data is mostly located in the first months of 2020, and if the date range is set to the last 30 days for example, no data is to be shown.

On the other hand, this date range can be of use when having big data and only the last X days of data need to be shown. This increases performance and uses less data.

!["Custom date range"](Images/ReportCustomDateRange.png)

## 1.4. Sharing and notifications
A report isn't of use much if the right people cannot access it. Therefore, these reports (as all of Google's products) can be shared with the share button. You can also choose to embed the report in other pages for example.

Lastly, the report can be emailed daily. Other products often have notification or error warnings that can be set on KPI's, that would result in the best insights of course. Be aware of the sharing and notification settings for these kind of products.

# 2. Using your RestDB NO-SQL data
Your (big) data is often not stored in a Google Sheet. Luckily, other sources can be bound to dashboards. For Google Data Studio, you can choose (virtually) any Google product, including BigQuery. This means that you can embed data sources up to petabytes of scale into this product.
Additionally, third parties have built connectors so that you can embed other sources into a dashboard.

* Go to Resource -> Manage added data sources.
* Add a data source
  * Search for 'json' and select 'Custom JSON/CSV/XML'.
  Our NO-SQL database is filled with JSON documents so this connector is the one we need.
* You will be prompted to fill in your personalia, you can skip that by scrolling down and selecting next.
* Now fill in the form:
  * Data Type: JSON
  * Source URL: Your URL from your RestDB collection, mine is https://atdsmmaartijn-4b1e.restdb.io/rest/ttnraw for example.
  * As you can see, you don't have access to mine, neither has Google to yours without your API-key. Add it in the HTTP-headers field like so:
  ```javascript
  { "x-apikey": "<<your api-key here>>" }
  ```
  * Check both 'Convert numeric-looking values to numbers' and 'Convert date-looking values to dates'
  * Click Add in the right bottom
  * Now edit your connection, you will see that all of your fields are collected.
  * Again: You can change your connection name in the top. Name it something like 'JSON RestDB Source'.

## 2.1. Using your RestDB data
* Create a new page
* Add a table to the page and set the source to your new RestDB source.
* Now you see your empty table...

Remember the report settings that we mentioned earlier? This empty data has got to to with the default filter in the report.

* Go to report settings and set the default date range to 'This Year'. Now you will be able to see the data.
  *I don't know why it adds this filter, but with this range you will be able to see your data.*

Now we will combine our sources. Usually we combine sources such as weather data and moist data for example, but now we are going to combine our sources on exactly the same key, just to see if it works.

* Go to Resource -> Manage blended data
* Add a data view
* Select your JSON source and Google Sheet source.
* On join keys, in both, select dev_id and date (payload_fields: date in JSON).
* On metrics select active and payload_fields: active
  * Make sure both are selected to have MAX calculation.
  * Give both of them a different name so you can select them both in your report.
  * Give the blended data source a good name.<br />
!['Blend data summary'](Images/Blend_data.png)
* Now close your data manager and go back to your dashboard.
* Add a table, set its data source to your new blend.
* Use dev_id as your dimension
* Use both the active fields as a metric.

Now you can see that you succesfully have used both data sources. Your data in both sources is exactly the same, but you can imagine that you have other blends in other projects.

We have shown that we can use several types of data sources in our dashboards, that we can use it in our cloud environment and that we even can blend those data to become even more powerfull.

Next, we are going to use our data in a machine learning environment.

# 3. Google Colaboratory

To be created.