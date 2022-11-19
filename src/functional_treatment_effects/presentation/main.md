---
paginate: true
marp: true
author: Tim Mensinger and Dominik Liebl
description: "Statistische Woche 2022: FAIR CAUSAL INFERENCE FOR FUNCTIONAL DATA"
theme: custom
---

<!-- ===================================================================================
# TITLE PAGE
==================================================================================== -->
<!-- paginate: false -->

## CAUSAL INFERENCE FOR <br/> FUNCTIONAL DATA

#### Case Study

Statistische Woche; Muenster, 2022
<br/>

#### Tim Mensinger & Dominik Liebl
University of Bonn

---
<!-- paginate: true -->
### Motivation

![bg right 75%](../graphs/foot_side_view_red_nike.jpg)

- Foot striking patterns:
    - forefoot vs heel

* Consider one metric: Force on ankle joints

* ***What's the (causal) effect of forefoot running on ankle joint loading?***

---
### Data

<img src="../../../bld/figures/presentation/data.png" width=1100>

---
### Data Structure

|                   |                      |                  |
|-------------------|----------------------|------------------|
|**Outcomes**       |**Controls**          |**Treatment**     |
|$Y_i \in C^1[0, 1]$|$X_i \in \mathbb{R}^p$|$W_i \in \{0, 1\}$|

* Potential Outcomes:
    - $Y_i(1), Y_i(0) \in C^1[0, 1]$

    * $Y_i = W_i Y_i(1) + (1 - W_i) Y_i(0)$

    * SUTVA: $Y_i = Y_i(W_i)$

<!-- Say: Controls may be functionsl -->


---
### Object of Interest

- Average treatment effect function:
    <br/>
    $$\tau(t) = \mathbb{E}[Y_i(1)(t) - Y_i(0)(t)]$$

    for $t \in [0, 1]$

* Identification under **unconfoundness** (and **overlap**):
    - $(Y_i(1), Y_i(0)) \perp\hspace{-3mm}\perp W_i | X_i$
    * $\eta < \mathbb{P}[W_i = 1 | X_i] < 1 - \eta$

---
### Plan

1. **Find relevant control variables**
    - Utilize causal graphs from *causal inference* literature
2. **Choose a suitable estimator**
    - Utilize methods from *econometrics* literature
3. **Construct confidence bands**
    - Utilize results from *functional data* literature


---
<!-- _class: lead -->
# Find relevant control variables

---
<!-- _class: split -->
### Directed Acyclical Graph


<div class=leftcol>

<br/>
<img src="../../../bld/figures/presentation/dag.png" width=550>

</div>
<div class=rightcol>

<br/>

- For $t \in [0, 1]$

- Structure may change with $t$

- Set of variables used for prediction of outcome and treatment may differ

</div>

---
<!-- _class: lead -->
# Choose a suitable estimator

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
### Properties and Requirements

Properties of $\hat{\tau}(t)$:

- Consistent for $\tau(t)$
- Doubly robust
- Semiparametric efficient

Requirements:

- Cross-fitting
- Nuisance functions are estimated at $o_{P}(n^{-1/4})$ rates

---
<!-- _class: lead -->
# Construct Confidence Bands

---
### Simultaneous Confidence Bands

- **To Show:**
    - Asymptotically Gaussian estimator of $\tau$
    - Uniformly consistent estimator of its covariance kernel $c$
    (and its 1st and 2nd partial derivatives)

- Liebl and Reimherr (2022):
    - **Get:** Simultaneous confidence bands

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
### Application

<img src="../../../bld/figures/presentation/data.png" width=1100>

---
### Result

![bg vertical 95%](../../../bld/figures/presentation/doubly_robust.png)

---
### Contact

![bg right 75%](../graphs/functional-treatment-effects-repo-qr.png)

<br/>

- Email:<br/>[tmensinger@uni-bonn.de](mailto:tmensinger@uni-bonn.de)
<br/>
- GitHub:<br/>[timmens/functional-treatment-effects](https://github.com/timmens/functional-treatment-effects)
