# Read the Code

I wrote this article at the request of the organizers specifically for the Software People conference website.

When I joined [CQG](https://www.cqg.com/?utm_source=chatgpt.com) at the end of 1999, I thought I already had solid experience in software development: three years of building custom enterprise database applications. I thought I knew a lot. I was very self-confident.

Then I ran into a small problem.

CQG was not a database application assembled from familiar off-the-shelf technologies like MS SQL Server, Visual Basic, Delphi, JavaScript, and 1C. It was a massive real-time trading platform written entirely in C++, with its own database server, its own embedded language, its own thick client, and hundreds of servers supporting thousands of simultaneous users.

The codebase alone was nearly 50 megabytes of source code — not counting utilities, infrastructure, and system components.

This was the first genuinely large software system I had ever seen.

The assignment I received looked deceptively simple: modify the data processing engine and server. In reality, it nearly drove me insane. I only completed it seven months later, after attending internal architecture lectures on the system. And after those lectures, I had to throw away almost everything I had written beforehand and redo the entire solution properly in two months.

This time, before writing code, I showed my preliminary design to Tal Korin, the author and chief architect of the system. He pointed me in the right direction in about five minutes.

That was the first time I voluntarily initiated what I later learned was called a design review, and the first time I was genuinely happy someone found flaws in my design.

After that project, I started working directly with Tal because, according to him — and much to my surprise — I turned out to be one of the few people who actually benefited from the architecture lectures.

By then, however, I had already lost most illusions about myself.

I realized that all my knowledge, university education, and experience were worth far less than I had imagined.

What shocked me was this: objectively speaking, I had a stronger formal Computer Science education than Tal did. I *knew* more theory. But I became absolutely certain that I could not have designed and implemented a system like that in a year the way Tal had done ten years earlier with just one assistant.

I would have drowned in details long before the project was finished.

And so it slowly dawned on me that there existed something critically important — something almost completely orthogonal to formal education, design patterns, and books on object-oriented design.

Tal had it. I didn’t.

If all my knowledge could not help me build such systems, then what exactly was it worth?

Knowledge exists for action. Otherwise it is just decorative porcelain.

From that moment on, I started carefully observing Tal, studying his decisions and methods, trying to understand what exactly I was missing.

In other words, I signed up as an apprentice. Tal gladly took on the role of mentor. Over the next several years, Tal turned me into an engineer by showing me, in practice, what engineering actually meant.

Most of it felt strangely similar to Zen. You would receive some mind-breaking assignment, wrestle with it for days, and then suddenly something would click.

One conversation especially stuck with me.

---

“Tal, can you explain how this thing works?”

“Honestly? I don’t know. Go read the code and figure it out.”

“Tal, are you screwing with me?! There are fifty megabytes of this undocumented crap! Everybody knows you know everything.”

“Okay, look,” Tal said calmly, without arguing. “I’m telling you — I don’t know. So I have to read the code myself to answer your question. Which means I open the code.”

Tal opened the correct file on the first try, navigated to roughly the correct place without any class browser, and found the right method.

“Here,” he said. “See? This guy calls this guy” — Tal always referred to classes and objects as “guys” — “then this happens, then that happens. Simple.”

“Thanks, Tal. Now it makes sense. And you said you didn’t know.”

“I keep telling you: read the damn code. You can do exactly the same thing yourself.”

“But without documentation none of this is understandable.”

“What kind of documentation?”

“Class diagrams, for example.”

“We had one a few years ago. It’s completely obsolete now. Fifty engineers, active development — you understand. But if you really think it’ll help, I can look for it.”

I thought for a moment.

“No. If it’s outdated, I’d still have to read all the code to know where I can trust the diagram and where I can’t.”

“Exactly,” Tal replied patiently. “That’s why code is the best documentation. It’s always current. It never becomes obsolete.”

Then I asked him to explain another subsystem.

“No,” Tal said. “You’ll explain it to me after you read it. I actually need to modify that code soon. Go read it.”

At the time, I was slightly offended. I thought Tal simply didn’t understand things as deeply as he pretended.

For years, I thought he was wrong.

---

Then, about three years later, a colleague approached me.

“Vlad, can you explain how this subsystem works?”

I was exhausted and barely functioning mentally, but I decided to help.

Without thinking, I navigated directly to the right file, found the correct method, read the code, reconstructed the subsystem’s logic in my head, and simultaneously explained it in plain language.

And then something suddenly clicked.

I remembered my conversation with Tal years earlier.

It was as if I were watching myself from the outside.

“See? It’s simple,” I concluded.

And then, to my own astonishment, I added:

“Really, though — read the code. Code is the best documentation. You think I already know this subsystem? I’m seeing this code for the first time too.”

“But the code is undocumented! At least some diagrams would help.”

I launched [Rational Rose](https://en.wikipedia.org/wiki/Rational_Rose?utm_source=chatgpt.com), reverse-engineered several classes into a diagram, and showed it to him.

“Here. Fresh, current diagram. But what’s the point of maintaining documentation that becomes obsolete in a year and can be regenerated in two minutes?”

My colleague stared at the diagram.

It clarified nothing.

And that was when I fully understood that Tal had been right all along.

The value was never in the diagrams themselves. The value was in the thought process required to reconstruct the system.

That is why code is the best documentation.

---

Of course, Tal was not merely trying to demonstrate the practical uselessness of project documentation.

The philosophy of “code is the best documentation” gives you something much more important.

It forces you to accept that code is the primary source of truth. You cannot avoid it, work around it, or substitute something else for it. Eventually, you must confront the code directly and rely on your own ability to understand it.

Only then do you begin to develop real reverse engineering skills.

Any fool can bolt a new abstraction onto the side of an existing system.

A real software engineer — emphasis on *engineer*, not “coder” — can analyze somebody else’s subsystem, reconstruct the author’s intent, continue that line of thought, and solve problems effectively within another engineer’s conceptual framework.

All of that while working directly with code.

That is one of the defining competencies of an architect.

Tal genuinely did not care whether documentation existed or not because he could move effortlessly between code and architecture entirely in his head.

When designing systems, he always clearly understood what kind of code his ideas would eventually become. That allowed him to mentally evaluate enormous numbers of alternatives and quickly discard bad ones.

In his view, an architect who cannot fluently read unfamiliar code — and no longer writes code personally — inevitably becomes a poor architect within a few years.

The second important aspect of this philosophy is understanding that code is written primarily for humans, and only secondarily for computers.

That brings us close to Donald Knuth’s ideas of Literate Programming.

Because if a person cannot clearly express a thought in natural language, how can they possibly express that same thought clearly in a far more formal programming language?

But that is another story.
