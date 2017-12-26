---
layout: default
show_meta: false
title: "Django Recipes"
subheadline: "All you need to know to build a Django App"
header:
   image_fullwidth: "header_unsplash_5.jpg"
permalink: "/cookbook/django/"
---

<div id="blog-index" class="row">
	<div class="small-12 columns t30">
		<h1>{{ page.title }}</h1>
		{% if page.teaser %}<p class="teaser">{{ page.teaser }}</p>{% endif %}
		<dl class="accordion" data-accordion>
			{% assign counter = 1 %}
			{% assign cTags = site.categories.Django | sort:"tags" %}
			{% for post in cTags limit:1000 %}
			<dd class="accordion-navigation">
			<a href="#panel{{ counter }}"><span class="iconfont"></span> {% if post.tags %}{{ post.tags }} › {% endif %}<strong>{{ post.title }}</strong></a>
				<div id="panel{{ counter }}" class="content">
					{% if post.meta_description %}{{ post.meta_description | strip_html | escape }}{% elsif post.teaser %}{{ post.teaser | strip_html | escape }}{% endif %}
					<a href="{{ site.url }}{{ site.baseurl }}{{ post.url }}" title="Read {{ post.title | escape_once }}"><strong>{{ site.data.language.read_more }}</strong></a><br><br>
				</div>
			</dd>
			{% assign counter=counter | plus:1 %}
			{% endfor %}
		</dl>
	</div><!-- /.small-12.columns -->
</div><!-- /.row -->