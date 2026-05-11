# Read the Code

I wrote this article at the request of the organizers specifically for the Software People conference website. Originally published here: [Software People conference website](http://www.softwarepeople.ru/press/articles/09/?utm_source=chatgpt.com)

When I joined [CQG](https://www.cqg.com/?utm_source=chatgpt.com) at the end of 1999, I already had what I considered pretty solid experience in software development: three years of building custom enterprise database applications. I thought I knew a lot. I thought I was good. I was extremely self-confident.

There was just one small problem.

CQG was not a database application glued together from off-the-shelf technologies like MS SQL Server, Visual Basic, Delphi, JavaScript, and 1C — the stuff I was used to. I was stunned by the sheer size of the application: almost 50 megabytes of core source code alone, not counting all the bells and whistles, service utilities, and various system components which, for some reason, outweighed the main codebase itself.

This was a real, serious, successful software system. It had been under development for ten years by dozens of engineers. Entirely written in C++. With its own specialized database server, its own embedded programming language, its own thick client capable of doing everything a trader could possibly want — and a few things they probably shouldn’t. Fault-tolerant, real-time, deployed across farms of hundreds of servers, supporting something like ten thousand simultaneous users.

The assignment I was given involved modifying the data processing engine and server. It looked deceptively simple, and it nearly drove me insane. I only finished it seven months later — after attending internal lectures on the architecture of the system. And the funny part was that after those lectures, I had to throw away everything I had written before them and redo the whole thing properly in two months.

This time, before writing anything, I prudently showed my preliminary design — my approach to solving the problem — to Tal Korin, the author and chief architect of the system. He pointed me in the right direction. It took him five minutes.

That was the first time in my life I voluntarily initiated a design review — without even knowing the term — and was genuinely happy people found flaws in my design.

After I successfully completed the task, I ended up working directly under Tal, because, according to him — and much to my astonishment — I turned out to be one of the few people who actually benefited from the architecture lectures.

By that point, however, I had lost all illusions about myself.

I realized that all my knowledge, university education, and experience were worth next to nothing.

What amazed me was a very simple fact: objectively speaking, I had a much stronger formal Computer Science education than Tal did. I *knew* more. And yet, after working with him for a while, I became absolutely certain of one thing: I would never have been able to design and implement a system like that in a year the way Tal had done ten years earlier with just one assistant.

The system was simply beyond my cognitive limits. I would have drowned in details halfway through. And there was no way I could have made it flexible enough to survive ten years and still remain relevant.

That was when it slowly began to dawn on me that there existed something incredibly important — something completely orthogonal to university education. Something we were never even taught to notice.

It was orthogonal to design patterns. Orthogonal to books on object-oriented design.

And Tal had it. I didn’t.

If all my knowledge couldn’t help me build a system like that, then what exactly was it worth?

Understanding and knowledge exist for action. For nothing else. They are not decorative Chinese vases.

From that point on, I began carefully observing Tal, studying his decisions and methods, determined to figure out what this elusive thing was that I lacked.

In other words, I signed up as an apprentice. Tal gladly took on the role of mentor. Over several years, he turned me into an engineer by showing me, in practice, what engineering actually was. I will always be grateful to him for that.

Most of it felt like Zen Buddhism. You’d get some mind-shattering assignment — like the sound of one hand clapping — and then, at some unpredictable moment, enlightenment would suddenly hit you.

An astonishing experience.

Here’s one small example of what it was like.

---

“Tal, can you explain how this thing works?”

“Vlad, honestly, I don’t know. Go read the code and figure it out.”

“Tal, are you screwing with me?! There are fifty megabytes of this undocumented crap! Everybody knows you know everything.”

“Okay, look,” Tal said calmly, without arguing. “I’m telling you — I don’t know. So I have to read the code myself to answer your question. Which means I open the code.”

Tal opened the correct file on the first try, navigating through the filesystem without any class browser, scrolled directly to roughly the right place in the middle of the file.

“Right. You mean this thing? Okay, here it is. So… you need this method. Let’s read it. See? It calls this guy” — Tal referred to classes and objects as “guys”: *look, now this guy tells that guy to do this thing* — “See? Then this happens, then that happens. Simple.”

“Thanks, Tal! Now it all makes sense. And you said you didn’t know!”

“I’m telling you — read the damn code! You can do exactly the same thing yourself!”

“But there’s no way to understand any of this without documentation,” I said, fully convinced I could never do what he just did. The whole thing looked like sleight of hand.

“You need documentation to read code? What kind?”

“Well… class diagrams, for example.”

“We had one, I think. Made about five years ago. To put it mildly, it no longer reflects reality. We’ve got fifty engineers and active development going full speed. But if you really think it’ll help, I can go look for it,” Tal said, watching me sympathetically. “So? Want me to find it?”

“Nah,” I admitted after thinking for a second. “An outdated diagram probably won’t help. I’d still have to study all the code anyway just to know where I can trust the diagram and where I can’t.”

“Honestly, I’m not even sure a fresh one would help you that much,” Tal explained patiently. “That’s why I keep telling you: code is the best documentation. It’s *always* up to date. It *never* becomes obsolete. And it’s far more informative than a class diagram.”

“Okay, I get it. But maybe you could also explain how this part works…”

“Nope. *You* are going to explain it to *me* after you read it. I actually need to modify that section soon. Come on, kid — I’m counting on you. Go read the code.”

“Okay, Tal,” I said gloomily, and went off to read the code.

---

I should say: at the time, I was a little offended. I thought Tal didn’t actually understand anything. For a long time, I thought he was wrong.

Then, about three years later, a colleague came up to me with a question.

I was exhausted. My brain was barely functioning. By that point, I had thrown away all my class diagrams long ago — what was the point? The system already lived in my head.

“Hey Vlad, can you help me understand how this subsystem works?”

I slowly looked up, saw utter hopelessness in his eyes, sighed heavily, and decided to help. Even though I myself barely knew the subsystem — I’d just passed through nearby at some point.

“Okay, look,” I said, blindly navigating to the “right” file without any class browser, opening it, finding the correct method through search. “See what’s happening here?”

I read the code, effortlessly reconstructing the program’s logic and structure in my head while simultaneously explaining it to him in simple language.

And then something suddenly clicked in my brain.

I remembered my conversation with Tal from three years earlier. It was as if my consciousness split in two, and I was watching myself from the outside.

“See? It’s actually simple,” I concluded.

And then, to my own horror, I added the thing that had to be said — because it was true:

“And really — read the code. Code is the best documentation. You think I already know this subsystem? Nope. I’m seeing this code for the first time too.”

“But this code is completely undocumented! At least some diagrams would help!”

“Look,” I said, smiling as I fully realized that Tal, once again, had been right all along. “Here I launch [Rational Rose](https://en.wikipedia.org/wiki/Rational_Rose?utm_source=chatgpt.com), where I’ve reverse-engineered the entire system, and I drop these five classes onto a blank canvas. See? Fresh, up-to-date diagram. What’s the point of spending effort documenting something that becomes obsolete in a year and can be regenerated in two minutes? If it’ll really help you, I can print it out right now. Want me to?”

“Nah… probably not,” my colleague replied thoughtfully while staring at the diagram. It clarified absolutely nothing.

“Exactly. Diagrams themselves are worthless. What matters are the thought processes happening in your head while creating them. That’s why I’m telling you: code is the best documentation. Read the code.”

---

Of course, Tal wasn’t merely trying to show me the practical uselessness of project documentation, as it may have seemed at first glance.

The philosophy of “code is the best documentation” gives you something much greater than simply *not having documentation*.

It imposes a necessary constraint. Only after accepting it — truly understanding that code is the primary source of truth, that you cannot fear it, cannot avoid it, cannot sidestep it or jump over it, that sooner or later you must collide with it head-on and rely only on your own ability to understand it — only then can you achieve mastery in reverse engineering and begin to understand what reverse engineering actually is.

Any idiot can bolt their own structure onto the side of an existing system.

A qualified software engineer — emphasis on *engineer*, not “coder” — can analyze somebody else’s subsystem, reconstruct the author’s thinking and intent, continue and develop that line of thought, and solve problems effectively within somebody else’s conceptual framework.

All of that while working directly with code.

That is the defining competence of an architect. The highest level of engineering mastery.

And it has only distant relation to what people usually call “refactoring.”

Tal genuinely did not care whether documentation existed or not.

Because he had mastered reverse engineering so thoroughly that he could effortlessly move from code to architecture and back entirely in his head.

As a result, when designing systems, he always clearly visualized what kind of code his ideas would eventually turn into. That allowed him to mentally simulate huge numbers of alternatives very quickly, discarding bad ones almost immediately.

In his view, an architect who cannot read unfamiliar code fluently “off the page,” and who no longer writes code personally, is like a cripple trying to run on crutches. Within a few years, they inevitably become a very bad architect.

The second important aspect of this philosophy is understanding that code is written primarily for humans, and only secondarily for computers.

That leads directly toward ideas close in spirit to Donald Knuth’s concept of Literate Programming.

Because really — how can a person who cannot clearly express a thought in their own natural language, which they have spoken since childhood, possibly express that same thought clearly in a vastly more formal programming language?

But that’s another story.
