## Secret Santa

![Family Picture](https://i.imgur.com/g6Eu3sx.jpg)

This Christmas, my extended family did a Secret Santa under the following rules:

- There are 4 family ties in total: Family A, Family B, Family C, and Family D
- Family A has 5, Family B has 5, Family C had 3, and Family D has 1
- Each member of a family is assigned a member of a family that is **not** of their own (i.e., a member of family A can't get another of Family A)

When we did our secret santa and revealed to each other who got whom, there was **exactly** one pair who got each other (i.e., person $i$ got person $j$ and vice versa). The question is: **what was the probability of this occuring?**

### The Setup

My first idea was to use a Poisson Approximation. With the setup described, there are:

$$25 + 15 + 5 + 15 + 5 + 3 = 68$$

distinct pairs, each with pretty low probability. So, we can assume that dependence is weak and that it is approximatley binomial. So, let's view the number of pairs as a random variable $X$, and an indicator of pair $i$ of its members getting each other. We can then represent:

$$X = I_1 + I_2 + \ldots + I_{68}$$

Cool! We can then use linearity to say that:

$$E[X] = E[I_1] + E[I_2] + \ldots + E[I_{68}]$$

Then, by the fundamental bridge of expectation and probability,

$$E[X] = P(I_1 = 1) + P(I_ 2 = 1) + \ldots + P(I_{68} = 1) $$

Now, we need to calculate this for each pair.

We can think about it in a pyramid structure. Let A, B, C, and D represent a member of those respective families, and let $r_{ij}$ represent the probability of a member of family i getting a vice versa match with a member from family j. We assume equally likeliness for each, and find:


$$r_{ij} = r_{ji} = \frac{1}{\text{ppl not in family j}} \cdot \frac{1}{\text{ppl not in family i}}$$

Then, we mutliply by the amount of people that can be chosen from family $i$ by the amount of people that can receive from family $j$. So, let:


$$a = \frac{1}{9 \cdot 9}$$
$$b = \frac{1}{9 \cdot 11}$$
$$c = \frac{1}{9 \cdot 13}$$
$$d = \frac{1}{11 * 13}$$

And we get:

$$E[X] = 25a + 15b + 5c + 15b + 5c + 3d \approx 0.718$$

Then, we get

$$X \overset{\cdot}{\sim} Pois(0.718)$$

So,

$$P(X = 1) \approx e^{-0.718} \approx \boxed{0.48}$$

### Simulation
We can further check our answer via simulation. First, we need to sample, let's say $10000$, possible arrangements. Please see the [simulation code](https://github.com/njd87/statarchive/blob/main/secret%20santa/simulation.py) for the full doc!

Here is the approximate distribution from 10000 samples:

![Secret Santa Simulations](https://i.imgur.com/XAfxFrY.png)

And we get than the approximate probability is $0.3426$. Not that close, but it was an approximation.
