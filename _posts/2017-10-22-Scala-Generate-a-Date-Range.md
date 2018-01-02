---
layout: page
sidebar: right
title: "Scala Generate a Date Range"
subheadline: ""
teaser: ""
tags:
  - Scala
categories:
  - Programming
---

## Problem
You need to create a list of dates.

## Solution
```Scala
scala> import org.joda.time.{DateTime, Period}
import org.joda.time.{DateTime, Period}

scala> def dateRange(from: DateTime, to: DateTime, step: Period) : Iterator[DateTime] = {
     | Iterator.iterate(from)(_.plus(step)).takeWhile(!_.isAfter(to))
     | }
dateRange: (from: org.joda.time.DateTime, to: org.joda.time.DateTime, step: org.joda.time.Period)Iterator[org.joda.time.DateTime]

scala> val from = new DateTime().withYear(2017).withMonthOfYear(8).withDayOfMonth(1)
from: org.joda.time.DateTime = 2017-08-01T21:17:22.183+08:00

scala> val to = new DateTime().withYear(2017).withMonthOfYear(8).withDayOfMonth(13)
to: org.joda.time.DateTime = 2017-08-13T21:17:22.353+08:00

scala> val step = new Period().withDays(1)
step: org.joda.time.Period = P1D

scala> val range = dateRange(from, to, step)
range: Iterator[org.joda.time.DateTime] = non-empty iterator

scala> val dateList = range.toList
dateList: List[org.joda.time.DateTime] = List(2017-08-01T21:17:22.183+08:00, 2017-08-02T21:17:22.183+08:00, 2017-08-03T21:17:22.183+08:00, 2017-08-04T21:17:22.183+08:00, 2017-08-05T21:17:22.183+08:00, 2017-08-06T21:17:22.183+08:00, 2017-08-07T21:17:22.183+08:00, 2017-08-08T21:17:22.183+08:00, 2017-08-09T21:17:22.183+08:00, 2017-08-10T21:17:22.183+08:00, 2017-08-11T21:17:22.183+08:00, 2017-08-12T21:17:22.183+08:00, 2017-08-13T21:17:22.183+08:00)

scala> dateList.foreach(println)
2017-08-01T21:17:22.183+08:00
2017-08-02T21:17:22.183+08:00
2017-08-03T21:17:22.183+08:00
2017-08-04T21:17:22.183+08:00
2017-08-05T21:17:22.183+08:00
2017-08-06T21:17:22.183+08:00
2017-08-07T21:17:22.183+08:00
2017-08-08T21:17:22.183+08:00
2017-08-09T21:17:22.183+08:00
2017-08-10T21:17:22.183+08:00
2017-08-11T21:17:22.183+08:00
2017-08-12T21:17:22.183+08:00
2017-08-13T21:17:22.183+08:00
```


## Problem 2

You need to convert dates into Strings with a target format.

## Solution

```Scala
scala> val dateString = dateList.map{p => p.toString("yyyy-MM-dd")}
dateString: List[String] = List(2017-08-01, 2017-08-02, 2017-08-03, 2017-08-04, 2017-08-05, 2017-08-06, 2017-08-07, 2017-08-08, 2017-08-09, 2017-08-10, 2017-08-11, 2017-08-12, 2017-08-13)
```


## Problem 3 
You have a list of files that are named by date. You need to concatenate three strings, prefix and suffix with dates, to generate a list of file names so that you can load those files at one time.



## Solution
```Scala
scala> val fileNames = dateList.map{p => "/path/to/"+p.toString("yyyy-MM-dd")+".csv"}
fileNames: List[String] = List(/path/to/2017-08-01.csv, /path/to/2017-08-02.csv, /path/to/2017-08-03.csv, /path/to/2017-08-04.csv, /path/to/2017-08-05.csv, /path/to/2017-08-06.csv, /path/to/2017-08-07.csv, /path/to/2017-08-08.csv, /path/to/2017-08-09.csv, /path/to/2017-08-10.csv, /path/to/2017-08-11.csv, /path/to/2017-08-12.csv, /path/to/2017-08-13.csv)

scala> fileNames.foreach(println)
/path/to/2017-08-01.csv
/path/to/2017-08-02.csv
/path/to/2017-08-03.csv
/path/to/2017-08-04.csv
/path/to/2017-08-05.csv
/path/to/2017-08-06.csv
/path/to/2017-08-07.csv
/path/to/2017-08-08.csv
/path/to/2017-08-09.csv
/path/to/2017-08-10.csv
/path/to/2017-08-11.csv
/path/to/2017-08-12.csv
/path/to/2017-08-13.csv
```