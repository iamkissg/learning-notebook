# How to write a great research paper

> Papers: communicate your ideas in the best and clearest possible way

## Simon Peyton Jones's 7 simple suggestions:

1. Don't wait: write
2. Identify your key idea
3. Tell **one** story
4. Nail your contributions to the mast (桅杆???)
5. Related work: later
6. Put your readers first
7. Listen to your readers

## A few thoughts from Ulrich

- Frame research problems
  - Do you have a clear problem statement in the abstract? It is clear from the paper? Can you write a research statement for your paper in a single sentence?
  - If a `reviewer` cannot form such a sentence for your paper after reading just the abstract, then your paper is usually doomed. (就是老师追求的简洁, 但是该有的都得有)
  - Clear framing helps `readers`
  - Your research statement should be `falsifiable` (可以被检验的)
  - Keep your reasons real (段子: "This was your one chance to convince me of the problem you’re working on. And now you told me you’re working on it because it is popular...,", 有点像裤子都脱了, 你给我看这个)
- Write to be understood
  - For *every line* in your paper, ask questions about your reader's **mental model**:
  	1. What does my reader understand up to this point?
  	2. What is my reader thinking at this point?
  	3. How will my next narrative (叙述/故事) change that?
- Keeping a flowing story line (保持流畅的故事情节)
    - Don't confuse or frustrate your readers, by
        - Switching context "mid way" / "mid flight"
        - Using undefined notation
        - Changing notation
    - When a concept requires specific notation, you may introduce the notation with the concept as early as possible. It helps shape your reader's mental model, and minimizes later context switching. (**下标**, **一致性**, 等等)
    - Do everything you can to not mess with the mind of your reader
- Be academically honest. Don't oversell

## A few thoughts from Stephan

- High-level thoughts
    - Writing IS research (IS ???). it is how we formulate, crystallize, and communicate our ideas. Make it a daily habit!
    - Good papers are written, great papers are re-written, so get the first draft done asap. Just do it.
    - Good papers leave the reader with one solution to solving a specific problem; great papers leave the reader with new ideas for their own problems.
        - Don't leave it up to your reader, always ask yourself "what have I learned" and make that explicit.
- Write to discover/understand (for yourself)
    - **Be precise in what you are trying to do**. Use simple language. If you cannot describe your idea in 2-3 simple sentences, maybe you don't understand it that well yourself. Work at it until you can. Read Strunk & White (The Elements of Style). It is a timeless classic.
    - State your hypotheses. Make them falsifiable. It is how science works.
    - I like to do a "blank slate" experiment once I have a first draft written: I start reading what I wrote as if I was a new reader reading this for the first time, and ask "why" or "why should I care" after every sentence. It forces you to be more explicit and get to the point.
    - Keep a daily "snippets" where you continually summarize your work, results, and ideas. It helps refine your thoughts. (和 Bestfitting 的先有一个 document, 在竞赛过程中持续更新的做法一致)
- Write to get accepted (for the reviewer)
    - Reviewers are the unpaid, overworked, gate-keepers of science. Don't waste their time.
    - Not all reviewers will be familiar with your work. It is up to you to bring your message across in the clearest way possible. Still, it's a very noisy process.
    - Reviewers usually have less than 1 hour per paper, sometimes only 30 minutes. They are basically trying to answer the question "How can I justify rejecting this?" Get to the point!
    - Do not write your personal journey. Science is a random walk, but we tell it like a shortest path.
- Write to enlighten (for the reader)
    - Academic writing is not like writing prose. There are not set ups, no surprises, and no punch lines. Doesn't mean it has to be dry, though.
    - Tell the reader (像总分总的结构)
        1. What you want to tell her
        2. Then tell her, and finally
        3. Tell her what you told her
    - This hour-glass (沙漏, general to specific to general) works very well at the level of paragraphs, sections, and papers.
- (One possible) ideal process
    - Write a rough 2-4 sentence abstract  first (what, why, how)
    - Write the Model description next. This is easy, it's the idea you're trying out.
    - Then write the experimental section (i.e. get the results). And your results tables, create your graphs.
    - Then write the Discussion and Conclusion sections (what did we learn from this?)
    - Finally write the Introduction (expand #1 by framing the research question, and introducing relevant background work)
    - Write the Abstract last.
- Low-level ideas
    - Learn LaTeX and use Sharelatex or some other collaborative editing platform with revision control
        - Split different sections into different files (easier to track, can export experiments directly to latex tables, etc)
        - Download the conference style sheet and use it from the beginning
        - Add colorized TODO notes (different color for each author) in the document using \newcommand. This way you can easily remove them to generate a draft for submission.

## A few thoughts from Martin

- Claims (声明?)
  - Never make a claim that is not directly validated by a theorem, an experiment, or a reference.
  - Make claims that are useful to tell the story. More claims is not always better.
  - It's important to write the paper first to know what claims you have to make, and what experiments / theory are needed to validate your claims.
- Highlight problems and negative results
  - People will run into them. Better to prepare them, and propose potential solutions.
  - These are avenues for further work. Other readers will often figure out how to solve them, and your algorithm will be even better later.
- Flow of the paper
  - You have to convince the reader to keep reading at every paragraph. Do not assume that the reader wants to read your paper, or that they will read all of it.
    - E.g. before switching sections, always have the last paragraph of the previous one introduce it. More importantly, explain why the next section is needed.
  - Only have theorems that improve your story.
    - E.g. you made a claim that your algorithm approximates some loss function -> prove a theorem quantifying this approximation.
  - Unless proofs are important for the story -> appendix.
  - Do not say "Here are some guarantees from our algorithm". Introduce and justify its existence first.
- A last note on theory
  - Have theorems that are meaningful
    - E.g. if your algorithm is meant for high dimensions, do not have bounds that depend exponentially in the number of dimensions.
  - Be honest
- Final tips
  - Make a bullet list with the core contributions at the end of your introduction. It will tell readers and reviewers concisely what claims to expect (and an idea of the experiments / results).
  - Figures and their captions are the first thing the reader will see! Make them self-contained, with extremely concise and clear captions, saying what they mean and their conclusion.
  - When there's a paper you like, take a literally notes, and try to understand why you liked reading it.
