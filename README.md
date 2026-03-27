Project: Predicting Tennis Match Outcomes Using Probability and Markov Chains

What is this project about?
In this project you will build a program that predicts the probability of a player winning a tennis match against another player. The key idea is that a tennis match is built up from individual points, and if you know the probability of winning a single point on serve, you can work out everything else mathematically. This is called a Markov chain model.
A Markov chain is a system where the next state depends only on the current state, not on the history of how you got there. A tennis game has this property. At deuce, it does not matter how you got to deuce. What matters is only who wins the next point.
This project will teach you probability theory, how to build mathematical models, how to write Python code, and how to extract real data from the internet. These are skills you will use throughout your engineering career.

The core idea
Every tennis match reduces to two numbers for any given matchup between player A and player B:
•	p = probability that player A wins a point when A is serving
•	q = probability that player B wins a point when B is serving

From just p and q you can compute, step by step:
1.	Probability that the server wins a single game
2.	Probability that a player wins a set, including a tiebreak at 6-6
3.	Probability that a player wins the match, for best of 3 or best of 5 sets

Each step uses the same logic. You work out the probability of moving between states until one player reaches a winning state. This is the Markov chain in action.

What you will build
You will write a Python program that does the following:
4.	Takes p and q as inputs
5.	Computes the probability that the server wins a game, using a formula you derive yourself
6.	Computes the probability that a player wins a set
7.	Computes the probability that player A wins a best-of-3 or best-of-5 match
8.	Validates the model against real historical match data scraped from the web

Steps to follow
9.	Learn the basics of probability. You should be comfortable with independent events, conditional probability, and expected value. Khan Academy has a good free course. Spend about a week on this before touching any code.
10.	Learn what a Markov chain is. Read the Wikipedia article on Markov chains. Focus on absorbing states and transition probabilities. You do not need advanced mathematics at this stage.
11.	Work out the game formula by hand. For a game starting at 0-0, draw out all possible score sequences on paper. At deuce, derive the formula for the probability of winning from deuce. This derivation is the heart of the whole model. Do not skip it.
12.	Implement the game model in Python. Write a function called game_win_prob(p) that returns the probability of the server winning a game. Test it: when p = 0.5 the answer should be exactly 0.5. When p = 0.6 the answer should be close to 0.736.
13.	Implement the set model. A set is won when one player reaches 6 games with a lead of at least 2, or wins a tiebreak at 6-6. Write set_win_prob(p, q) that returns the probability of the server winning the set.
14.	Implement the match model. For best of 3, player A needs to win 2 sets. Write match_win_prob(p, q, sets=3) and test it with a few example values.
15.	Learn basic web scraping in Python. Use the requests and BeautifulSoup libraries. Practice by extracting a simple table from any sports website. This is a skill in its own right and will take a few days to get comfortable with.
16.	Scrape real serve statistics. The website tennis-abstract.com has serve win percentage data for professional players. Extract p and q for several well-known matchups.
17.	Validate your model. Compare your predicted win probabilities against historical head-to-head records. How often does the player your model favours actually win?
18.	Write a short report describing your model, your results, and where the model succeeds and where it falls short.

Milestones
Use these milestones to track your progress. Show your supervisor the output for each milestone before moving to the next one.

Milestone 1: Understand the problem. You can explain in your own words what p and q are, why they are the right fundamental quantities, and what a Markov chain is. Write a one-page note summarising this in your own words.
Milestone 2: Game formula on paper. You have derived the formula for the probability of winning a game from scratch, working by hand. You can verify it gives 0.5 when p = 0.5 and you understand why.
Milestone 3: Python implementation working. Your functions game_win_prob and set_win_prob run correctly and you have tested them with several values including edge cases.
Milestone 4: Full match model complete. You can input p and q and get a match win probability for both best-of-3 and best-of-5 formats.
Milestone 5: Real data obtained. You have scraped serve statistics for at least three player pairs from a real website and you can show the raw numbers you extracted.
Milestone 6: Validation and report complete. You have compared predictions to real outcomes, computed a simple accuracy measure, and written a short analysis of the model's strengths and limitations.

References and resources
•	Newton, P.K. and Kovalchik, S.A. (2009). Probability of Winning at Tennis: Theory and Data. Studies in Applied Mathematics. This is the foundational paper for this kind of model. Read the introduction and the section on point-level models first.
•	Carter, W.H. and Crews, S.L. (1974). An Analysis of the Game of Tennis. The American Statistician. A short, readable early paper on the mathematics of tennis scoring.
•	Wikipedia article on Markov chains. Focus on the section on absorbing Markov chains.
•	tennis-abstract.com: A website with detailed match statistics including serve win percentages for professional players.
•	Python requests library documentation: docs.python-requests.org
•	BeautifulSoup documentation: beautiful-soup-4.readthedocs.io

A note on using AI
You are encouraged to use an AI assistant such as Claude throughout this project. Use it to explain concepts you do not understand, help you debug specific errors, or check whether your reasoning is correct.
Do not ask AI to write your code for you. When AI gives you a formula or derivation, verify it yourself. AI makes mathematical errors. Catching those errors is one of the most valuable parts of this project.
Keep a brief log of your conversations with AI, noting where it helped and where it was wrong. Include this log in your final report.
