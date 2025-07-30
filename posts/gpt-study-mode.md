---
title: I Cloned ChatGPT Study Mode
date: 2025-07-30
---

Kind of? Yesterday, OpenAI released [study mode](https://openai.com/index/chatgpt-study-mode/), what I would call a *persona* on top of ChatGPT that encourages learning.

I was very interested to investigate it in more details for a couple of reasons. I have used language models for learning for a while. I have found that the ability to ask question after question until I feel like I fully understand something is incredibly useful. I am also soon to be a college lecturer, so this seems like an important tool for me to understand in some detail.

In the release article, the authors hinted that they achieved this through a custom system prompt:

> Under the hood, study mode is powered by custom system instructions we’ve written in collaboration with teachers, scientists, and pedagogy experts to reflect a core set of behaviors that support deeper learning including: ​​encouraging active participation, managing cognitive load, proactively developing metacognition and self reflection, fostering curiosity, and providing actionable and supportive feedback. These behaviors are based on longstanding research in learning science and shape how study mode responds to students.

Simon Willison immediately [extracted the system prompt](https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode/). This got me thinking, I wonder if I gave that as a system prompt to any model, would it produce similar behaviour to OpenAI's new fancy ChatGPT "feature".

I added it as a custom system prompt option to [my own conversational AI tool, telegram-llm](https://github.com/mmcatcd/telegram-llm/blob/master/system_prompts/study_mode.md), and sure enough, created a conversation using Claude Sonnet 4, and sure enough it seemed to produce a pretty similar experience. [Here's](./study-mode-sonnet-4-messages.html) a conversation that I had with it about the event loop in Node.js.

## The Results

I definitely need to do some more testing, both with the real ChatGPT study mode, and my own concoction, but so far I've noticed some interesting things:

1. **Responses are much more concise.** LLMs tend to be very verbose. The adjustment to the system prompt seems to get the system prompt to provide information piece-by-piece, with shorter, easier to digest, messages. I like it. It's similar to how Claude Code makes changes to a codebase incrementally, asking for feedback at each step.
2. **It asks a lot of questions.** It almost tends to end every message with a question for you. I find this to be really annoying. It reminds me of the kind of teacher who doesn't teach you anything about a topic, and then asks you a question that there's no way for you to know the answer to, every time. It's the kind of teaching that makes me angry, and it actually made me feel a little bit bad about my lack of knowledge after a while. I would love to know if the interaction actually made me learn more or less though, despite the bad vibes I felt after a while. It also didn't really give me the chance to ask my own questions. I could ask my own question of course, but I felt like most of the time I was interrupting the model.
3. **It doesn't always match my level of understanding.** I have always liked how I felt that I was in control of a learning conversation with a language model in the past. It allowed me to nudge the conversation towards the things that I felt that I didn't understand. I found that with this system prompt, the model spoke with more of a teacher-like authority, and it tried to control the conversation instead. I can certainly see cases where this might be better. For example, if you're a student who doesn't know where to start with a topic, it might be more beneficial for the model to be opinionated. One downside that I found of this is that it often "mansplained" things to me that I already understood, even after I showed understanding of it further up in the conversation. Perhaps this is a side effect of [context window limits](https://github.com/mmcatcd/telegram-llm/blob/7c01d45e2410898643a9d4e4114b534dccaca1c8/handlers.py#L50) that I've imposed on `telegram-llm` to make sure I don't spend too much money on tokens. I'll have more of a play in ChatGPT to see if I experience the same.
4. **Quizes.** It would occasionally ask me to explain what we've learned so far, or produce some worked examples and ask me to answer them, correcting any mistakes that I made. I really liked this. It's a way for me to *verify* that what I think I've learned is actually correct, without having to explain it to another human being. It's definitely not perfect. Sometimes its corrections seemed akin to that of an interviewer who wanted a hyper-specific answer to a vague question that they asked during an interview in order to "test" me, which was a little annoying. Still though, I think this is probably the best part of the prompt.

## The Prompt

The prompt itself is an interesting read. It's also surprisingly short. A cynic might see this new feature as nothing but marketing up some pretty basic prompt engineering. Perhaps they're right, but I would hazard to say that quite a bit of work went into engineering this prompt so that it works well for OpenAI models.

### CAPITALISED LETTERS

The prompt certainly makes use of the caps lock:

> The user is currently STUDYING

> you MUST obey these rules

I know from my own prompt engineering experiments that using certain terms e.g. "step-by-step", or embolding text, does make a difference to behaviour. It would be really interesting to know what different kinds of hightlighting does. For example:

- `****`
- `**`
- `CAPS`
- "step-by-step"

and most importantly, what would happen if I said "The user is currently **STUDYING**!"? Would that be the equivalent of `!important` in CSS?

If you pop the word "STUDYING" into the GPT-4o tokeniser, it uses 4 separate tokens, whereas "studying" uses just 1.

<figure>
  <img src="../img/studying-caps.png">
</figure>

### How did they create the prompt?

I don't know how they engineered the prompt, but I'd love to know. Evaluating how well a prompt like this performs seems on-par with evaluating how well different methods of learning perform, that is to say, pretty damn hard. Still, I'd love to know what they did, how many iterations they had, how they tested it etc.
