---
paginate: true
marp: true
author: Tim Mensinger
description: "Brown Bag Seminar"
theme: custom
math: mathjax
---

<!-- ===================================================================================
# TITLE PAGE
==================================================================================== -->
<!-- paginate: false -->

## CAUSAL INFERENCE WITH <br/> FUNCTIONAL DATA

<img src="figures/bgse_logo.jpg" width=200 style="position:absolute;bottom:2em;left:2em">

<p style="position:absolute;top:8em;left:2em;text-align:left;">
<b>BGSE Brown Bag Seminar</b>
<br>
December, 2022
</p>

<p style="position:absolute;top:15em;right:2em;text-align:right;">
<b>Tim Mensinger</b>
<br>
Institute of Finance & Statistics
</p>


---
### Contents

<span style="text-align:center;font-size:50px;position:relative;top:-0.5em;">

Introduction
<hr style="width:50%;margin-top:50px">

Theory
<hr style="width:50%;margin-top:50px">

Application

</span>


<!-- paginate: true -->
---
### Motivation

<img src="figures/running-footstrike-types.jpg" style="display:block;margin-left:auto;margin-right:auto;width:80%;margin-top:-1em;">

* ***What's the causal effect of forefoot running on the force acting on the ankle joint?***

---

### Data

Explain where the data is from, how I cleaned it, what the limitations of the data are,
how I could imagine to use the multivariate features, use knee joint loading, etc.


---

![bg contain](../../../bld/figures/presentation/data.png)

Make another slide with mean difference, and bullet points why this is not a good estimator of the causal effect.


---
### Data Structure

Make this two columnA

|                   |                      |                  |
|-------------------|----------------------|------------------|
|**Outcomes**       |**Controls**          |**Treatment**     |
|$Y_i \in C^1[0, 1]$|$X_i \in \mathbb{R}^p$|$W_i \in \{0, 1\}$|

* Random sample:
    - IID $\{(Y_i, X_i, W_i) : i = 1,\dots, n\}$

* Potential Outcomes:
    - $Y_i(1), Y_i(0) \in C^1[0, 1]$

    * $Y_i = W_i Y_i(1) + (1 - W_i) Y_i(0)$

    * SUTVA: $Y_i = Y_i(W_i)$


---
### Object of Interest

- Average treatment effect function:
    $$\tau(t) = \mathbb{E}[Y_i(1)(t) - Y_i(0)(t)]$$

    for $t \in [0, 1]$

* Identification under **unconfoundness**:

    - $(Y_i(1), Y_i(0)) \perp\hspace{-3mm}\perp W_i | X_i$

---
### Inference

- Simultaneous $\alpha$-confidence band:
    $$SCB_n : [0, 1] \to (\ell(t), u(t)) \subset \mathbb{R}$$
    such that
    $$\mathbb{P}[\, \forall t \in [0, 1]: \tau(t) \in SCB_n(t)] \geqslant 1 - \alpha$$

- Illustration of confidence band here

---
### Literature Review

Only if time.


---
### Augmented Inverse Propensity Score Weighting

$$
\begin{align}
    \hat{\tau}(t) &= \frac{1}{n} \sum_{i = 1}^n \hat{\mathbb{E}}[Y_i(t) | X_i, W_i=1] - \hat{\mathbb{E}}[Y_i(t) | X_i, W_i=0]\\
    &+ \frac{1}{n} \sum_{i = 1}^n W_i \frac{Y_i(t) - \hat{\mathbb{E}}[Y_i(t) | X_i, W_i=1]}{\hat{\mathbb{P}}[W_i = 1 | X_i]} - (1 - W_i) \frac{Y_i(t) - \hat{\mathbb{E}}[Y_i(t) | X_i, W_i=0]}{1 - \hat{\mathbb{P}}[W_i = 1 | X_i]}
\end{align}
$$

- (Non-)parametric estimators of nuisance functions:
    - $\small \hat{\mathbb{E}}[Y_i(t)|X_i, W_i=w]$
    - $\small \hat{\mathbb{P}}[W_i=1|X_i]$

---
### Requirements

- Cross-fitting: estimate nuisance functions on other sample than $\hat{\tau}$

- Nuisance functions are estimated uniformly at $o_{P}(n^{-1/4})$ rates


---
### Simultaneous Confidence Bands

- Liebl and Reimherr (2021):

    - Asymptotically Gaussian estimator of $\tau$

    - Uniformly consistent estimator of its covariance kernel $c$
    (and of its 1st and 2nd partial derivatives)

    - **Get:** Simultaneous confidence bands

---

**Lemma:** Assume process $X(t)$ and its derivative process $X'(t)$ fulfill
- wlog $\mathbb{E}[X(t)] = 0$
- $\mathbb{E}[\sup_t X(t)^2] < \infty$ and $\mathbb{E}[\sup_t X'(t)^2] < \infty$
- $X(t)$ has $C^2[0, 1]$ sample paths almost surely
- $X$ and $X'$ fulfill condition **IC**

**Then:** for a random sample $X_1, \dots, X_n \sim X$
- $n^{-1/2} \sum_i X_i \overset{d}{\to} \mathcal{GP}(0, c)$ in $C^1[0, 1]$
- $||\hat{c} - c ||_\infty \overset{a.e.}{\to} 0$ and $||\partial_{1, 2}\hat{c} - \partial_{1, 2}c||_\infty \overset{a.e.}{\to} 0$
- *Using Hahn (1977) and Davidson (2021)*

---
### Integral Condition

Require $f$ such that

$\mathbb{E}[(X(s) - X(t))^2] \leqslant f(|s-t|)$

for small $|s-t|$ and

$\int_0^\infty y^{-3/2} \sqrt{f(y)} \, \mathrm{d}y < \infty$

---
### Theorem

Under *regularity conditions* on the continuity and differentiability of functions and distributions of the functional errors


$$
\sqrt{n}(\hat{\tau}  - \tau) \overset{d}{\longrightarrow} \mathcal{GP}(0, c).
$$

And, we can construct an estimator of $c$ and its partial derivatives that is uniformly consistent.

---
### Proof Outline

* Define oracle estimator $\hat{\tau}^*$ that uses true nuisance functions $\mathbb{E}[Y_i(t)|X_i, W_i=w]$ and $\mathbb{P}[W_i = 1|X_i]$

* Show that $\hat{\tau}^*$ is asymptotically Gaussian with kernel $c$
    - Structure of $c$ can be derived from the structure of $\hat{\tau}^*$

* Show that $\sqrt{n}||\hat{\tau} - \hat{\tau}^*||_\infty\to_p 0$

* Construct sample analogue estimator $\hat{c}$ of $c$

* Show that $\hat{c}$ and its derivatives converge uniformly


---
### Simulations

Only if time.

---
### Result

Combine this plot with raw data.

![bg vertical 95%](../../../bld/figures/presentation/doubly_robust.png)

---
### Resources

<u>GitHub</u>

- **Project**: [timmens/functional-treatment-effects](https://github.com/timmens/functional-treatment-effects)
<span style="font-size:30px;">Contains: This presentation, the working paper, and code to reproduce the analysis.</span>


- **Package**: [timmens/fte](https://github.com/timmens/fte)
<span style="font-size:30px;">Python package that can be used to estimate functional treatment effects and corresponding simultaneous confidence bands.</span>
