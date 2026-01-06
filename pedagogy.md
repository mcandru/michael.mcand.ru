---
title: Pedagogy
date: "2025-08-07"
last_updated: "2025-08-07"
---

# Pedagogy

This file serves as a note to document everything that I learn about the practice of teaching.

> If you can't explain it simply, you don't understand it well enough

## Checks for Pedagogy

Adapted from Grant Sanderson's fantastic talk, ["Math's pedagogical curse"](https://www.youtube.com/watch?v=UOuxo6SA8Uc).

1. Does the lesson start with a motivating question?
2. Are new abstractions preceded with concrete examples?
3. Are core ideas given diagrams?

### 1. Does the lesson start with a motivating question?

In computer science, this could be framed as some problem to get a computer to do what you want it to.

### 2. Are new abstractions preceeded with concrete examples?

Start with the base case, and work _towards_ the general case.

### 3. Are core ideas given diagrams?

Describe, explain, visualise. The more angles you view a concept from, the greater the chance is of **raising the ceiling and lowering the floor** of your exposition.

## Tenets

Adapted from [Intellectual Mathematics manifesto of teaching](https://intellectualmathematics.com/manifesto/). While less actionable than the **Checks** above, I think they're still very useful.

1. Students pursue learning not because it is prescribed to them but rather out of a genuine desire to figure things out
2. We learn when we are challenged, when we push ourselves. If you're not stuck, you're not learning
3. The goal of teaching is independent thought

These axioms might seem a little antagonistic at first, so lets describe my interpretation of their meaning in some more detail.

### 1. Students pursue learning not because it is prescribed to them

In a practical sense, this means that if you're a teacher, and you simply prescribe your students something to learn, they will not learn it well. Therefore, as a teacher, it is partially your job to convince them that it is of interest to them.

I have frequently heard that some subjects most enjoyed in education were not specifically because of the content, but of the teacher. The teacher alone convinced them that an otherwise uninterested subject was worth studying.

### 2. We learn when we are challenged

Richard Feynman once said "You must not fool yourself and you are the easiest person to fool", when speaking of practicing science. The role of the teacher is to provide ways to test whether a student is fooling themselves in their understanding or not.

A teacher may provide clear lectures, and well thought-out tests, and these are important, and do help, but that does not mean that they are testing whether a student has fooled themselves or not.

I don't think that I necessarily agree entirely that you are not learning unless you're stuck though. Sometimes you're stuck because you're learning in the wrong way for you, and it could be much easier to learn from a different angle.

### 3. The goal of teaching is independent thought

Your students aren't going to be in college forever. They have come to learn how to gain knowledge, and apply it. Teaching should incentivise students to think independently. But, it should not necessarily require it. Some students may already be capable independent thinkers, other not quite.

## Course Design Process

1. Break the course topic into a section for each week of the course. For example, if the course is 12 weeks long, break it into 12 sections. A week is the atomic unit of time for a course.
2. For each week, split it into high-level headings and a set of bullet points for each heading of what should be covered.
3. Flesh out each high-level heading more with the help of LLMs. They can be particularly useful for adding "boilerplate" explanations, that don't really require difficult concepts, but are more just to empart relatively straightforward information. They can also be good at providing simple examples, although they often fall short for more complex topics. They are very good at taking a toy example, and consistently reusing it throughout for consistency.
4. Proof read your work for silly mistakes, and things the LLMs didn't do well.
5. Build _tests_ against each week of work. This will mostly be in the form of a lab. Labs should be quite guided generally, simple to follow, and complete. The goal here isn't really to challenge the student much, more just to familiarise them with the topic practically.
6. Write assignments. Once you have fleshed out the contents, and built small ways to test the student knowledge of the content, you need to build more complex tasks for them to complete. Ideally, they should mimic reality as closely as possible, and contain a mixture of concrete problems to solve, and open-ended, creative problems for bonus points. Ideally, there should be more than one, so that students can get interim feedback, and they should build on understanding from each other. Try to avoid several assignments with hard dependencies between each other to cater for students who do not complete one assignment.
7. Polish lecture materials. This will include building out high-fidelity explanations, examples, and analogies to help students build mental models of what they are learning. It should also include simplifying, demystifying, removing jargon, and general shortening the length of things. This is the most _nice to have_ step. The course can still go ahead without this.

## A Recipe for Lecturing

1. Write the agenda on the whiteboard at the start of the lecture - this can remain on the board through the lecture so that students can keep the high-level view of what's being discussed throughout
2. Keep introductions to topics brief - no need to give a boring history that nobody cares about
3. Show them how to use it first
4. Dig into specifics only after showing them how to use it first

## Assignments

There are certain properties that you should try to achieve with assignments that you set:

1. **Easy to Pass:** the assignment provide enough concrete guidance so that, unless you're lazy and just didn't bother, you can get a passing mark.
2. **Extra Mile:** for students who are interested, and want to challenge themselves, the assignment gives them the scope to do so. The extra mile should be purposefully vague, and not worth many marks. Typically, the students who are truly interested and have the time won't be motivated much by the extra marks anyway.
3. **Clear Marking Scheme:** it should be clear from the marking scheme what your assignment submission should do to get certain marks. Ideally, you should be able to accurately estimate the grade that you will get from your own submission just by looking at it. This also has the added benefit that I can easily explain a grade to a student if they wish to dispute it.
4. **No Overlap:** there should be sufficient novelty from other modules to make for a level playing field, and to keep things interesting for everyone
5. **Demonstrable Learning Objectives:** the assignments should be related to what is taught in the module, and should in turn require the use of what is taught in class to complete.

These properties are surprisingly difficult to achieve when setting assignments. If you set an open ended assignment to allow students to be creative, properties (3), (4) and sometimes (5) can be difficult to achieve. However, if you set an assignment that is too strict, you risk choosing something that isn't of interest to students, and may not have a sufficient (2).

## Grading

- Create a rigid, granular marking scheme. The more granular the marking scheme, the more reproducible a grade will be.
- Grade exams and some assignments by question or section. Grade larger projects with a broader scope by submission.
- The first few submissions graded will take four times longer than the average, this is normal.

## About Me

I have increasingly been asked "What do you do?", or more recently "What do you teach?". It's a good question. I could answer with something like: "Oh I teach computer programming" or "Computer stuff" or "Computer Science" if I want to sound fancy.

I have made up a couple of different job titles for myself over the years. When I started at Inscribe, my job title was "Detector Engineer". I got computers to detect fraud for me. Later, when my job became less clear-cut, I changed my title to "Prompt Engineer" in line with the fad at the time. I refused to change recently to "Context Engineer" though because it's far too serious.

So what job title should I come up with for this job? Well, there was a discussion recently about a name for a new 6th department in the Institute. My suggestion was "The Department of Computer Art", as a play on a "Department of Computer Science". Rather fitting, considering the Institutes position as a place of education I thought. I have always thought of "Computer Science" as much more of an art anyway, especially when you actually need to get computers to do what you want them to. Could I call myself a "Lecturer in Computer Art"? It sounds too much like I'm getting Computers to make art for me, rather than teaching the art of getting computers to do things for me.

Anyway, long ramble over, I lecture in "Getting computers to do what you ask them to", at the Institute of Art, Design and Technology Dún Laoighaire. And every year it keeps getting a little easier to get them to do what you want them to.
