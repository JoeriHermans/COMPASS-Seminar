# Slide intro
> Estimated time: 30 seconds

In this talk we will introduce a natural and effective approach to tackle Bayesian inference
in the presence of simulation models with intractable likelihoods.
We will present a complete inference pipeline based on a novel ratio estimator
and provide a diagnostic to evaluate the quality of its approximation. We subsequently
demonstrate that
the ratio estimator can used to draw samples from the approximated posterior and apply
the technique on realistic problems with high-dimensional features spaces.

# Slide 1
> Estimated time: 1 minute

At the heart of most scientific disciplines we have complex computer simulations.
Feynman once said: "what I cannot recreate, I do not understand".
In that same spirit, scientists construct simulators in an attempt
to model the observed phenomenon(a). Besides nuissance parameters, the
simulator can typically be parameterized by a parameter of interest,
or the model parameter theta.

**Action**: Mark theta.

As an example, in a physics simulation theta might be the mass of a galaxy,
the gravitational constant, or in a setting we have all been affected by,
the reproduction number of a disease in an epidemic.

Now, since a simulator is essentially a computer program, we can easily generate
or sample new data x for given model parameters theta
because the simulator implements some
well-understood mechanistic model.

However, we can't simply calculate the likelihood of the data given model parameters theta.
The reason for this is that a simulator typically implements some random process.
This means that in order to compute the likelihood of the data given theta,
one would have to integrate over all possible execution paths z.
For most simulation models, this is intractable.

Therefore, in order to do inference, we have to rely on likelihood-free
surrogates to key components of your inference procedure.

# Slide 2
> Estimated time: 30 seconds

In Bayesian Inference for instance, we essentially want to know the set of model parameters
that are compatible with observation.
To achieve this, we compute the posterior density

**Action**: Mark p(theta|x)

using Bayes' rule. A key ingredient, is the likelihood of the data given a model parameter theta.
Since the likelihood is intracable in our scenario, we
can not realistically evaluate this.

We do however have access to the prior, the observation,
and a simulator (which is our assumed model) from which we can draw sample
for any model parameter we please.

The question at this point is, what part of Bayes'
rule do we design a surragate for in order to compute an
approximation to posterior?

# Slide 3
> Estimated time: 30 seconds

Unlike previous work, we do not intent to approximate a
density or use some variational approximation.
Instead, we note that Bayes' rule can be factorized into the product

**Action**: Mark p(theta)

of the prior, a tractable quantity, and the

**Action** Mark likelihood-to-evidence ratio

likelihood-to-evidence ratio, an intractable quantity.

# Slide 4
> Estimated time: 1 minute 30 seconds

At this point, I would like you to recall the fact that

**Action**: Highlight red message.

classification is essentially density ratio estimation. This has been known for quite some time,
but this idea was especially popularized by the GAN literature.

The method we propose relies on learning an amortized estimator
of the likelihood-to-evidence ratio.
The key ingredient is a classifier or discriminator, without any architectural restrictions,
which takes as inputs observations x
and model parameters theta.

The procedure to train this ratio estimator is quite straight forward.
You simply train the discriminator with the binary cross entropy criterion,
or some other criterion of your choosing,
to distinguish between samples from the dependent joint with class label 1,
and the independent joint with class label 0.

A batch of the independent joint can simply be created by
randomly shuffling a batch of data from the dependendent joint.
This implies that you simply have to presimulate a dataset of
samples from the dependent joint.

# Slide 5

Now, what you can show is that the optimal discrimator which minimizes
this loss yields the following decision function.

Subsequently, given some observation x and model parameter theta,
you can transform the output of the discriminator to obtain
the pointwise mutual information
which in turn is equivalent to the likelihood to evidence ratio

This is quite useful, because this means that
the
neural network will automatically learn a mapping from
high-dimensional feature space to likelihood-to-evidence ratios.

After training, the ratio estimator can be used to obtain
amortized estimates of the posterior density function
for an arbitrary observation x and model parameter theta.
This is computed by simply mutiplying the tractable prior
probability with the approximated ratio.

In general however, we recommend to compute the posterior using the log ratio.
This quantity can be extracted directly from the discriminator,
as the log ratio is the logit of the discriminator output.
That is, the quanity before the sigmoidal activation.

The usage of log ratio as compared to transforming the discriminator output,
has the desirable property that you will not have any numerical issues when the output of the
discriminator is close to 0 or 1. This implies that taking gradients with respect to
x or theta
using the log ratio will not suffer from vanishing gradients
in this same regime as you bypass the sigmoidal activation.

# Slide 5
> Estimated time: 10 seconds

So, given the simplicity of this approach,
and the fact that the neural surrogate is simply some classifier,
we can used to matured liturare surrounding classifiers, and apply these advances
to statistical inference.

# Slide 7
> Estimated time: 2 minutes

Another important aspect is that before making any scientific conclusion based
on the approximated posterior,
it is crucial to ask yourself the question: can we trust the results of these computations?

We note that the ratio estimator should satify

**Action**: Mark identity.

this identity. If it does not, the ratio estimator does not
properly approximate likelihood-to-evidence ratios.
The evaluation of this identity is obviously intractable
as it depends on the evaluation of the likelihood and marginal model.

However, we can use the simulator to sample from these densities.
The idea here is to reweigh samples
from the marginal model by the approximated ratio, and check if the reweighted samples resemble
samples produced by the simulation model at a specific test hypothesis.

The "resemblence" test can be done by training another classifier
tasked to distinguish between samples of the
reweighted marginal model, and samples from the test hypothesis.
The obtained Area Under Curve (AUC) can then be used
to assess if there are any flaws in the approximation.
This means that if the AUC = 0.5 (a diagonal ROC curve),
then the procedure could not find anything wrong with the
estimated likelihood-to-evidence ratios. If the AUC is larger than 0.5,
the the classifier could discrimate between these and the
ratio estimator did not satify the identity.

However, it is important to realize that if AUC = 0.5, it does not necessaraly mean
that the ratio estimator is correct.
In fact, it is simply possible that the classifier is not
powerful enough to discriminate between these cases.

# Slide 8
> Estimated time: 2 minutes

Having access to a well-tested ratio estimator
we can draw samples from the posterior by using the ratio estimator to
approximate the likelihood ratio between consequative states in the Markov chain.
This can be done because the acceptance
ratio in MCMC is essentially some form of the posterior ratios.

Now, since the discriminator is differentiable with respect to theta,
the gradient with respect to the likelihood
can be computed by taking the derrivate of the approximate likelihood-to-evidence ratio.
This allows our method to be applicable in HMC-like MCMC algorithms, if that is desired.

In the figure below we demonstrate the effectiveness of our approach
against existing sequential approaches. You can clearly see that the structure
with respect to the MCMC ground-truth is preserved.
For a more principled evaluation and discussion of the results
I would like to point you to the
paper. We would like to stress however that the other approaches
in this figure essentially deploy the full simulation budget
to optimize for a single posterior. While we tackle the harder task
of amortization.

# Slide 9
> Estimated time: 1 minute 30 seconds
We quantified this result by computing the AUC between samples of the approximated posterior and
the MCMC groundtruth. This gives us an indication of the quality of
the approximation for a given simulation budget.
Although the ratio estimator is used to amortize
the estimation of the posterior, it obtains
a significantly better approximation for the same number of simulations. This
is especially interesting since the sequential approaches focus their complete simulation
budget to optimize a single posterior.

This begs the question.
What does it mean to be simulation efficient?
ow many simulations do you require to properly
approximate the posterior?

Let's take the following perspective:
Ok, our approach might have a larger (offline) upfront cost,
although the figure shows otherwise, but at least we
can reuse these simulations to develop and tune the ratio estimator,
or even tackly a completely different problem if the data permits.

Because, let's be fair.
Do we really apply a training procedure only once to find
the right hyperparameters? We all show the
simulation budget of a single run, however,
we do not mention the simulation cost during model development,
and this is exactly what practicioners are really interested in.
So in that respect, our simulation cost remains constant.

# Slide 10
> Estimated time: 1 minute 30 seconds
Another advantage of our strategy is the fact that we can simply take existing high-performance
neural architectures and apply them to to inference problems.

In this particular instance we tackle
the problem of inferring the Einstein radius from an image of a strong gravitational lens.
This problem has a lot of nuissance parameters which need to be taken into account,
including several parameters describing the source galaxy, the mass and shape of the host galaxy,
and other parameters which can affect the structure of the lens.
In previous techniques, this would be quite difficult because there would be
architectural constraints.

However, since our approach only requires a discriminator, we can simply
leverage an existing architecture such as ResNet, and adapt the architecture to accomodate
for the model parameter theta.

In all of our work on images with a high-dimensional feature space,
we simply added the dependence on the model parameter theta in the fully connected trunk of
convolutional networks.
This has proven to be quite effective, other innovations in this area might help.

# Slide 11
> Estimated time: 1 minute

If you want to try it for yourself, we've written a Python package which provides you with all
the ingredients to tackle an inference problem.

Thank you.
