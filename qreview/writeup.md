![Imgur](https://imgur.com/qpnde9C.png)

Over this past summer, I worked on creating an online analytics application to provide insights into course reviews left by Harvard students from fall 2021 up to the spring semester of 2024. I am currently in the process of creating a full writeup of the results, but I wanted to get this post out first to have an outline of what the project entails.

You can access the website [here](https://qreview.streamlit.app/). If it asks to wake the website, just click the button.

You can view the collection and analysis code [here](https://github.com/njd87/qreport_review).

## Overview

On the title page is a breakdown of overall trends for a given academic year, providing distributions across the undergraduate school distinctions (SEAS, sciences, arts and humanities, social sciences, GENED, and "additional"), summaries of average hours spent by departments, and a ranking of the "gemmiest" classes, scored off of what I call the "GEM" index. The formula is a bit verbose, but it essentially weights hours spent on the class, prior knowledge needed, instructor scores, student reception, and recommendation liklihood.

## Department

On each department, I provide a barplot (or histogram with departments with enough classes) of each class with their hours sorted. For classes with multiple ranks on the GEM index, a KDE is provided of the approximate distribution. In addition, recommendations and instructor rating distributions are provided using KDE. The average sentiment of a given comment within the department, however, is an exention from the Bayesian model that will be discussed in the next section.

Below is an example of the distributions provided for COMPSCI in the 2023-2024 academic year:

![Imgur](https://imgur.com/DtW4nkp.png)


## Search a Class

Searching for a single class provides in-depth detail on what could be collected from the QReport website. It first provides some meta-data you could easily find just be looking up the QReport, but it also provides its GEM index and a wordcloud of the student comments.

For classes in the 2023-2024 academic year, pros/cons and suggestions (labeled feedback) were generated using Llama 3, 80b parameters. Take these with a grain of salt.

Then there are the student polarity scores. This was the most in-depth part of the project. I wanted to create an average of student polarity scores for each class; the issue is that classes have different amounts of comments. For example, if I told you a course was from COMPSCI but had no comments, a typical estimation would say that student sentiment polarity can't be determined. However, I instead took a Bayesian model to help mend this issue.

First, let's set up some notation.

Let $\xi_c$ represent the average polarity for a given "category," the term I used to label whether something was in SEAS, sciences, etc. Let $\varphi_d$ represent the average polarity within the department. Then, let $\mu_j$ finally be our average polarity for class $j$. Note the hierarchy here: each class $j$ belongs to department $d_j$, and each department $d$ belongs to category $c_j$.

However, we must also note that each class then has it's own "class effect" that deviates from the department. Label this average deviant as $\alpha_j$.

So, we can model this as:

$$\pi(\xi_c) \sim Unif\left(-1, 1\right)$$

$$\varphi_d | \xi_{c_d}, \sigma_{dep} \sim N\left(\xi_{c_d}, \sigma_{dep}^2\right)$$

$$\mu_j | \varphi_{d_j}, \alpha_j, \sigma_{class}, \sigma_{add} \sim N\left(\varphi_{d_j} + \alpha_j, \sigma_{class}^2 + \sigma_{add}^2 \right)$$

Then, using some MCMC, the crystalizations of the observed values can be used to inform our posteriors. These posteriors are plotted side by side (or as aggregate) to see how they deviate within the department and how they are distributed within the class.

This is interesting in classes that really stick out. Take, for example, CS 124:

![Imgur](https://imgur.com/Sm28CDD.png)

Despite the CS department as a whole having a pretty solid positive average, CS 124 is pretty negatively received, giving it a negative deviant from the department mean.


## Instructors

Something the QReport doesn't really focus on is how students rate the instructors. I've aggregated teh scores for each instrutor so that they can be searched. For now, feedback on the instructors is ommitted. Instead, I set up another Bayesian model to answer this question: how does each professor assign work?

Professors often teach multiple classes and classes usually have different professors. So, in capturing these trends, we may see if certain instructors tend to assign more work than others. This is done on a percentage basis: that is, we say professor A assigns x% more work than the natural average (the average number of hours the class requires by nature).

Doing this is similarly setup to the previous situation, instead that now instead of polarity we use hours, and instead of an additive additional effect it is a scalar on the mean.


$$\pi(\xi_c) \sim Unif\left(0, 23\right)$$

$$\varphi_d | \xi_{c_d}, \sigma_{dep} \sim N\left(\xi_{c_d}, \sigma_{dep}^2\right)$$

$$\mu_j | \varphi_{d_j}, \alpha_j, \sigma_{class} \sim N\left(\alpha_j \cdot \varphi_{d_j}, \sigma_{class}^2 + \sigma_{add}^2 \right)$$

And we are interested in $\alpha_j$. Most professors didn't have much information to go off of, so their scores centralize around 0% difference. However, there were some outliers out there. Feel free to take a look.