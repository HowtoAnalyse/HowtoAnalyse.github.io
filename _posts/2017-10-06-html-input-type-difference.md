---
layout: page
title: "What is the difference between `<input type='button' />` and `<input type='submit' />`"
categories:
  - Programming
tags:
  - HTML
---

`<input type="button" />` buttons will not submit a form - they don't do anything by default. They're generally used in conjunction with JavaScript as part of an AJAX application.

`<input type="submit">`buttons will submit the form they are in when the user clicks on them, unless you specify otherwise with JavaScript.