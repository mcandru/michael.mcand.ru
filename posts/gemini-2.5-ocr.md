---
title: Using Gemini 2.5 Pro for OCR with Bounding Boxes
date: 2025-03-28
---

There's quite a bit of hype around multi-modal LLMs OCR capabilities at the moment.
The benchmarks seem to conclude that they are in fact very good at extracting text
from images now. But there does seem to be an important missing piece of the puzzle
preventing some existing OCR use cases from making the switch, positional information.

I wanted to see if a multi-modal LLM could in fact return a bounding box for each word
it extracts. Gemini has to date, been the only family of multi-modal LLMs that successfully returns
bounding box information, so I decided to put their very recently released 2.5 Pro
model through its paces to see if it could, not only return the OCR text, but also
accurate bounding boxes.

For this incredibly unscientific test, I used a single image of one of my old shopping
receipts (please don't judge too hard). Here's what it came up with:

<figure>
    <div>
    <img src="../img/gemini-bounding-box.png" />
    <figcaption>The bounding boxes for every word found by Gemini 2.5 Pro</figcaption>
    </div>
</figure>

It's definitely far from perfect. Some bounding boxes miss the actual text entirely.
Are they good enough to actually use? Not really, but they're not too far off. I suspect
it won't be long before they're able to return very accurate postional information too.
I can't wait for that day to come.
