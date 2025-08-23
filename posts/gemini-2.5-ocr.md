---
title: Using Gemini 2.5 Pro for OCR with Bounding Boxes
date: 2025-03-28
---

## Using Gemini 2.5 Pro for OCR with Bounding Boxes

There's quite a bit of hype around multi-modal LLMs OCR capabilities at the moment. The benchmarks seem to conclude that they're very good at extracting text from images now. But there does seem to be an important missing piece of the puzzle preventing some existing OCR use cases from making the switch: positional information. While LLMs can tell you _what_ text is in an image, they typically can't tell you _where_ that text is located—information that's essential for many real-world applications.

I wanted to see if a multi-modal LLM could return a bounding box for each word it extracts. Gemini has to date, been the only family of multi-modal LLMs that successfully returns bounding box information, so I decided to put their very recently released 2.5 Pro model through its paces to see if it could not only return the OCR text, but also accurate bounding boxes.

For this incredibly unscientific test, I used a single image of one of my old shopping receipts. Here's what it came up with:

<figure>
    <div>
    <img src="../img/gemini-bounding-box.png" />
    <figcaption>The bounding boxes for every word found by Gemini 2.5 Pro</figcaption>
    </div>
</figure>

I've had a little tool on my site for visualising bounding boxes for a while [here](https://michael.mcand.ru/tools/bbox.html), which I used to visualise the results.

It's definitely far from perfect. Some bounding boxes miss the actual text entirely.
Are they good enough to actually use? Not really, but they're not too far off.

To give the model another chance, I tried a couple of other strategies:

1. Increase the input image size. In the original I sent a 1024x1024 image, I then doubled
   it to 2048x2048. I have absolutely no idea if this affects how the image is embedded by
   Gemini.
2. Implement a second pass. The first pass just extracts the text, and the second pass is
   given the text from the first pass, and the image, and asked to get the bounding boxes
   from that.

<figure>
    <div>
    <img src="../img/gemini-bounding-box-bigger.png" />
    <figcaption>The results of approach (1)</figcaption>
    </div>
</figure>

<figure>
    <div>
    <img src="../img/gemini-bounding-box-two-pass.png" />
    <figcaption>The results of approach (2)</figcaption>
    </div>
</figure>

I _think_ example (2) in particular does have better results, but it's still far from
perfect. Both have what look like entirely hallucinated bounding boxes.

I suspect it won't be long before they're able to return very accurate postional information too.
I can't wait for that day to come.
