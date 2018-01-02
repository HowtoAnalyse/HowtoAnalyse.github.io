---
layout: page-fullwidth
title: "Web Scrapers to get an Affordable Studio"
subheadline: ""
teaser: "I built web scrapers to find an affordable studio in Hong Kong"
header: no
tags:
  - Scrapy
categories:
  - Toolbox
---
<div class="row">
<div class="medium-4 medium-push-8 columns" markdown="1">
<div class="panel radius" markdown="1">
**Table of Contents**
{: #toc }
*  TOC
{:toc}
</div>
</div><!-- /.medium-4.columns -->

<div class="medium-8 medium-pull-4 columns" markdown="1">
## Getting Started   {#start}
Make sure you have scrapy installed.
This time, I use Scrapy 1.3.3

```shell
scrapy startproject nextstudio

cd nextstudio
```
Firstly, I would like to gather available apartments with a single bedroom on craigslist Hong Kong. So I set the starting URL as [http://hongkong.craigslist.hk/search/apa?sort=date&availabilityMode=0&max_bedrooms=1](http://hongkong.craigslist.hk/search/apa?sort=date&availabilityMode=0&max_bedrooms=1)

```shell
scrapy genspider craigslist "hongkong.craigslist.hk/search/apa?sort=date&availabilityMode=0&max_bedrooms=1"
```

Here we used `genspider` command to create a spider named `craigslist`. The URL followed will be the one spider starts crawling.

Until now, you may find that a well-structured python project has been created. Our main class is located in a python file called `craigslist.py` under the `spiders` folder.

Scrapy automatically adds _http://_ at the beginning of the starting url we defined while creating the spider.

## Extract Data using `xpath`

To locate the specific information, we need its html tag and the class name or id.

For example, after you right-click on any apartment name, and choose "Inspect", you can see the HTML code as following:

```html
<a href="https://hongkong.craigslist.hk/apa/d/2-similar-size-bdr-close-to/6435622235.html" data-id="6435622235" class="result-title hdrlnk">2 similar size bdr close to PP 3</a>
```

Now we know that the apartment name is the text of an `<a>` tag distinguished by its class name _result-title hdrlnk_ .

Under the `parse()` function, let's add the following code:

```python
titles = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
```

### The rule of `XPath` are as following:
* `//` tells spider to start from the tag specified rather than <html>
* `/a` refers to <a> tag
* `[@class="result-title hdrlnk"]` tells spider which of the <a> tags we want
* `text()` extract the text in the <a> tag for us

### `extract()` vs. `extract_first()`

`extract()` extracts every instance on the web page that follows the same XPath rule into a list

`extract_first()` only extracts the first item

We've already finished a simplest spider, which should look like this:

```python
# -*- coding: utf-8 -*-
import scrapy

class CraigslistSpider(scrapy.Spider):
    name = "craigslist"
    allowed_domains = ["craigslist.hk"]
    start_urls = ['http://hongkong.craigslist.hk/search/apa?sort=date&availabilityMode=0&max_bedrooms=1']

    def parse(self, response):
    	names = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        print(names)
```

Feel free to move to your terminal and run your spider:

```shell
scrapy crawl craigslist
```

## Export data as CSV

Based on the simplest spider built earlier, we need 2 more steps to output data into a CSV file.

#### Step 1: Loop through output data and `yield` one name each time in the form of dictionary.

```python
for n in names:
	yield {"Name": n}
```

#### Step 2: Add arguments for output in terminal

```shell
scrapy crawl craigslist -o res.csv
```

Similarly, we can also store data as JSON or XML. 

## Scrape the next page, and the next, and the next ...

"Inspect" the _next_ button, we can find the HTML code:

```html
<a href="/search/apa?s=120" class="button next" title="next page">next &gt; </a>
```


## Scrape one more depth


<small markdown="1">[Up to table of contents](#toc)</small>
{: .text-right }
</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

 [1]: http://kramdown.gettalong.org/converter/html.html#toc
 [2]: {{ site.url }}/blog/
 [3]: http://srobbin.com/jquery-plugins/backstretch/
 [4]: #
 [5]: #
 [6]: #
 [7]: #
 [8]: #
 [9]: #
 [10]: #